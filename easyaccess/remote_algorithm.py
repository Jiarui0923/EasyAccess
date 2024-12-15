"""
Module: Remote Algorithm for EasyAccess

This module provides the `RemoteAlgorithm` class, which serves as a client-side abstraction 
for interacting with algorithms hosted on EasyAPI. It includes functionality for managing 
inputs, outputs, documentation, and execution of remote algorithms.

Author: Jiarui Li
Email: jli78@tulane.edu
Institution: Computer Science Department, Tulane University
"""

import time
from .iotypemodel.iotype_model import IOType
from .progress import LoadProgress
from .parameter import Parameter, meta_types
from . import docflow as doc


class RemoteAlgorithm:
    """
    Represents a remote algorithm accessible via EasyAPI.

    Handles algorithm metadata, parameter management, and execution modes 
    (HTTP or WebSocket).
    """

    def __init__(self, client, entry_name, io_lib=None, mode='websocket', progressor=LoadProgress, entry_config=None):
        """
        Initializes the RemoteAlgorithm instance.

        Args:
            client: The EasyAccess client instance.
            entry_name (str): The name of the remote algorithm entry.
            io_lib (dict): A library of input/output types. Defaults to an empty dictionary.
            mode (str): The execution mode ('websocket' or 'http'). Defaults to 'websocket'.
            progressor: The progress reporting class. Defaults to LoadProgress.
            entry_config (dict, optional): Preloaded entry configuration.
        """
        self._client = client
        self._entry_name = entry_name
        self._io_lib = io_lib or {}

        if entry_config is None:
            algo_info = self._client._get_entry(self._entry_name, io=True)
        else:
            algo_info = entry_config

        self._load_algo_info(algo_info)
        self._load_in_out_params()
        self._doc = self._build_doc()
        self.__doc__ = self._doc
        self._mode = mode
        self._progressor = progressor

    def __repr__(self):
        return self._doc

    def _repr_markdown_(self):
        return self._doc

    @property
    def source(self):
        """
        Returns the source server information.

        Returns:
            str: The source server URL.
        """
        return self._client._server_info.get("server")

    def _load_algo_info(self, algo_info):
        """
        Loads algorithm metadata.

        Args:
            algo_info (dict): Algorithm metadata from the API.
        """
        self.id = algo_info.get('id')
        self.name = algo_info.get('name')
        self.description = algo_info.get('description')
        self.version = algo_info.get('version')
        self.references = algo_info.get('references')
        self.raw_inputs = algo_info.get('inputs')
        self.raw_outputs = algo_info.get('outputs')
        self._task = None
        self._task_id = None

    def _load_io_info(self, io_name):
        """
        Loads IOType information for a specific input/output.

        Args:
            io_name (str): The name of the IO type.

        Returns:
            IOType: The IOType object for the given name.
        """
        if io_name not in self._io_lib:
            self._io_lib[io_name] = IOType(**self._client._get_io(io_name))
        return self._io_lib[io_name]

    def _load_in_out_params(self):
        """
        Loads the input and output parameters for the algorithm.
        """
        self.inputs = {
            param: Parameter(
                name=io_obj.get('name'),
                io_type=self._load_io_info(io_obj.get('io')),
                desc=io_obj.get('desc'),
                default_value=io_obj.get('default'),
                optional=io_obj.get('optional'),
            )
            for param, io_obj in self.raw_inputs.items()
        }
        self.outputs = {
            param: Parameter(
                name=io_obj.get('name'),
                io_type=self._load_io_info(io_obj.get('io')),
                desc=io_obj.get('desc'),
                default_value=io_obj.get('default'),
                optional=io_obj.get('optional'),
            )
            for param, io_obj in self.raw_outputs.items()
        }

    def _build_doc(self):
        """
        Constructs documentation for the algorithm.

        Returns:
            str: The generated markdown documentation.
        """
        _doc = doc.Document(
            doc.Title(self.name, level=3),
            doc.Text(f'\n_source: {self.source}_  \n`{self.version}`  \n{self.description}  \n'),
            doc.Title('Parameters', level=4),
            doc.Sequence({
                param: f'({io_obj.iotype.meta}:**{io_obj.iotype.name}**){"_[OPTIONAL]_" if io_obj.optional else ""}=`{io_obj.default}`; {io_obj.desc}; (`{io_obj.iotype.condition}`) {io_obj.iotype.doc}'
                for param, io_obj in self.inputs.items()
            }),
            doc.Title('Returns', level=4),
            doc.Sequence({
                param: f'({io_obj.iotype.meta}:**{io_obj.iotype.name}**){"_[OPTIONAL]_" if io_obj.optional else ""}=`{io_obj.default}`; {io_obj.desc}; (`{io_obj.iotype.condition}`) {io_obj.iotype.doc}'
                for param, io_obj in self.outputs.items()
            }),
            doc.Title('References', level=4),
            doc.Sequence(self.references),
        )
        return _doc.markdown

    def cancel(self):
        """
        Cancels the current task if one is running.
        """
        self._cancel()

    def __call__(self, **kwargs):
        """
        Executes the algorithm using the specified mode.

        Args:
            **kwargs: Input parameters for the algorithm.

        Returns:
            The output of the algorithm execution.
        """
        if self._mode.lower() in ('http', 'https'):
            return self.run_http(**kwargs)
        elif self._mode.lower() in ('socket', 'websocket'):
            return self.run_websocket(**kwargs)
        else:
            raise ValueError(f'{self._mode} not supported')

    def _build_params(self, **kwargs):
        """
        Constructs the parameter dictionary for the API request.

        Args:
            **kwargs: Input parameters for the algorithm.

        Returns:
            dict: The constructed parameter dictionary.
        """
        params = {}
        for arg_name, arg_regular in self.inputs.items():
            if arg_name not in kwargs:
                if arg_regular.optional:
                    params[arg_name] = arg_regular.default
                else:
                    raise RuntimeError(f'{arg_name} is required.')
            else:
                params[arg_name] = arg_regular.iotype(kwargs[arg_name])
        return params

    def _cancel(self, task_progress_bar=None):
        """
        Cancels the task and updates the progress bar.

        Args:
            task_progress_bar: The progress bar instance.
        """
        if self._task_id is None:
            return
        if self._client._cancel_task(self._task_id):
            if task_progress_bar:
                task_progress_bar.done(self.name + ' cancelled')
        else:
            if task_progress_bar:
                task_progress_bar.error(self.name + ' failed to be cancelled')
        self._task_id = None

    def run_http(self, **kwargs):
        """
        Executes the algorithm using HTTP mode.

        Args:
            **kwargs: Input parameters for the algorithm.

        Returns:
            The output of the algorithm execution.
        """
        params = self._build_params(**kwargs)
        task_progress_bar = self._progressor(f'Task {self.name} Submitted', timer=True) if self._progressor else None
        try:
            task_id = self._client._submit_task(entry_name=self._entry_name, params=params)
            self._task_id = task_id
            time.sleep(0.1)
            response = self._client._get_task_return(task_id)
            while 'success' not in response:
                if task_progress_bar:
                    task_progress_bar.update(self.name + ' ' + response.get('status'))
                time.sleep(0.1)
                response = self._client._get_task_return(task_id)
        except KeyboardInterrupt:
            self._cancel(task_progress_bar)
            raise
        if not response['success']:
            if task_progress_bar:
                task_progress_bar.error(self.name + ' ' + response.get('output'))
            raise RuntimeError(response.get('output'))
        if task_progress_bar:
            task_progress_bar.done(f'Task {self.name} Finished.')
        return response.get('output')

    def run_websocket(self, **kwargs):
        """
        Executes the algorithm using WebSocket mode.

        Args:
            **kwargs: Input parameters for the algorithm.

        Returns:
            The output of the algorithm execution.
        """
        params = self._build_params(**kwargs)
        task_progress_bar = self._progressor(f'Task {self.name} Submitted', timer=True) if self._progressor else None
        try:
            task_id = self._client._submit_task(entry_name=self._entry_name, params=params)
            self._task_id = task_id
            task_socket = self._client._get_task_in_websocket(task_id=task_id)
            time.sleep(0.1)
            response = task_socket.query('get')
            while task_socket.connected:
                if task_progress_bar:
                    task_progress_bar.update(self.name + ' ' + response.get('status'))
                time.sleep(0.1)
                response = task_socket.query('get')
        except KeyboardInterrupt:
            self._cancel(task_progress_bar)
            raise
        if not response['success']:
            if task_progress_bar:
                task_progress_bar.error(self.name + ' ' + response.get('output'))
            raise RuntimeError(response.get('output'))
        if task_progress_bar:
            task_progress_bar.done(f'Task {self.name} Finished.')
        return response.get('output')
