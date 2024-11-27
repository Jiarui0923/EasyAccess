from .iotypemodel.iotype_model import IOType
from .progress import LoadProgress
from .parameter import Parameter
from .parameter import meta_types
from . import docflow as doc

import time
import asyncio
  
class RemoteAlgorithm(object):
    
    def __init__(self, client, entry_name, io_lib={}, mode='websocket', progressor=LoadProgress):
        
        self._client = client
        self._entry_name = entry_name
        self._io_lib = io_lib
        
        self._load_algo_info()
        self._load_in_out_params()
        self._doc = self._build_doc()
        self.__doc__ = self._doc
        self._mode = mode
        self._progressor = progressor
        
    def __repr__(self): return self._doc
    def _repr_markdown_(self): return self._doc
    
    @property
    def source(self): return self._client._server_info.get("server")
        
    def _load_algo_info(self):
        _algo_info = self._client._get_entry(self._entry_name, io=True)
        self.id = _algo_info.get('id')
        self.name = _algo_info.get('name')
        self.description = _algo_info.get('description')
        self.version = _algo_info.get('version')
        self.references = _algo_info.get('references')
        self.raw_inputs = _algo_info.get('inputs')
        self.raw_outputs = _algo_info.get('outputs')
        self._task = None
        self._task_id = None
        
    def _load_io_info(self, io_name):
        if io_name not in self._io_lib:
            self._io_lib[io_name] = IOType(**self._client._get_io(io_name))
        return self._io_lib[io_name]
    
    def _load_in_out_params(self):
        self.inputs = {param:Parameter(name=io_obj.get('name'),
                                       io_type=self._load_io_info(io_obj.get('io')),
                                       desc=io_obj.get('desc'),
                                       default_value=io_obj.get('default'),
                                       optional=io_obj.get('optional'))
                       for param, io_obj
                       in self.raw_inputs.items()}
        self.outputs = {param:Parameter(name=io_obj.get('name'),
                                        io_type=self._load_io_info(io_obj.get('io')),
                                        desc=io_obj.get('desc'),
                                        default_value=io_obj.get('default'),
                                        optional=io_obj.get('optional'))
                        for param, io_obj
                        in self.raw_outputs.items()}
    
    def _build_doc(self):
        _doc = doc.Document(
            doc.Title(self.name, level=3),
            doc.Text(f'\n_source: {self.source}_  \n`{self.version}`  \n{self.description}  \n'),
            doc.Title('Parameters', level=4),
            doc.Sequence({param:f'({io_obj.iotype.meta}:**{io_obj.iotype.name}**){"_[OPTIONAL]_" if io_obj.optional else ""}=`{io_obj.default}`; {io_obj.desc}; (`{io_obj.iotype.condition}`) {io_obj.iotype.doc}'
                          for param, io_obj
                          in self.inputs.items()}),
            doc.Title('Returns', level=4),
            doc.Sequence({param:f'({io_obj.iotype.meta}:**{io_obj.iotype.name}**){"_[OPTIONAL]_" if io_obj.optional else ""}=`{io_obj.default}`; {io_obj.desc}; (`{io_obj.iotype.condition}`) {io_obj.iotype.doc}'
                          for param, io_obj
                          in self.outputs.items()}),
            doc.Title('References', level=4),
            doc.Sequence(self.references),
        )
        return _doc.markdown
    
    def cancel(self):
        self._cancel()
    
    def __call__(self, **kwargs):
        if   self._mode.lower() in ('http', 'https', ): return self.run_http(**kwargs)
        elif self._mode.lower() in ('socket', 'websocket', ): return self.run_websocket(**kwargs)
        else: raise ValueError(f'{self._mode} not support')
    
    def _build_params(self, **kwargs):
        _params = {}
        for arg_name, arg_regular in self.inputs.items():
            if arg_name not in kwargs:
                if arg_regular.optional: _params[arg_name] = arg_regular.default
                else: raise RuntimeError(f'{arg_name} Required.')
            else:
                _params[arg_name] = arg_regular.iotype(kwargs[arg_name])
        return _params
    
    def _cancel(self, _task_progress_bar=None):
        if self._task_id is None: return
        if self._client._cancel_task(self._task_id):
            if _task_progress_bar is not None: _task_progress_bar.done(self.name + ' cancelled')
        else:
            if _task_progress_bar is not None: _task_progress_bar.error(self.name + ' failed to be cancelled')
        self._task_id = None
    
    def run_http(self, **kwargs):
        _params = self._build_params(**kwargs)
        if self._progressor is not None:
            _task_progress_bar = self._progressor(f'Task {self.name} Submitted', timer=True)
        else: _task_progress_bar = None
        try:
            _task_id = self._client._submit_task(entry_name = self._entry_name, params = _params)
            self._task_id = _task_id
            time.sleep(0.1)
            _response = self._client._get_task_return(_task_id)
            while 'success' not in _response:
                if _task_progress_bar is not None: _task_progress_bar.update(self.name + ' ' + _response.get('status'))
                time.sleep(0.1)
                _response = self._client._get_task_return(_task_id)
        except KeyboardInterrupt:
            self._cancel(_task_progress_bar)
            raise KeyboardInterrupt
        if not _response['success']:
            if _task_progress_bar is not None: _task_progress_bar.error(self.name + ' ' +_response.get('output'))
            raise RuntimeError(_response.get('output'))
        else:
            if _task_progress_bar is not None: _task_progress_bar.done(f'Task {self.name} Finished.')
            return _response.get('output')
        
    def run_websocket(self, **kwargs):
        _params = self._build_params(**kwargs)
        
        if self._progressor is not None:
            _task_progress_bar = self._progressor(f'Task {self.name} Submitted', timer=True)
        else: _task_progress_bar = None
        try:
            _task_id = self._client._submit_task(entry_name = self._entry_name, params = _params)
            self._task_id = _task_id
            _task_socket = self._client._get_task_in_websocket(task_id = self._task_id)
            time.sleep(0.1)
            _response = _task_socket.query('get')
            while _task_socket.connected:
                if _task_progress_bar is not None: _task_progress_bar.update(self.name + ' ' + _response.get('status'))
                time.sleep(0.1)
                _response = _task_socket.query('get')
        except KeyboardInterrupt:
            self._cancel(_task_progress_bar)
            raise KeyboardInterrupt
        if not _response['success']:
            if _task_progress_bar is not None: _task_progress_bar.error(self.name + ' ' +_response.get('output'))
            raise RuntimeError(_response.get('output'))
        else:
            if _task_progress_bar is not None: _task_progress_bar.done(f'Task {self.name} Finished.')
            return _response.get('output')