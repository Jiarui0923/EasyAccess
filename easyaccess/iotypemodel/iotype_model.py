import pandas as pd
import json
import os

from .meta_model import IOMetaTypeString
from .meta_model import IOMetaTypeNumber
from .meta_model import IOMetaTypeNumberArray

class IOType(object):
    
    _accept_meta_types = {
        'string':   IOMetaTypeString,
        'number':   IOMetaTypeNumber,
        'numarray': IOMetaTypeNumberArray,
    }
    
    def __init__(self, meta='string', id='', name='', doc='', condition=None, version=''):
        self.meta      = meta
        self.id        = id
        self.name      = name
        self.doc       = doc
        self.condition = condition
        self.version   = version
        
    def to_dict(self):
        return dict(
            meta      = self.meta,
            id        = self.id,
            name      = self.name,
            doc       = self.doc,
            condition = self.condition,
            version   = self.version
        )
        
    def __repr__(self): return f'<{self.name}({self.meta}) {self.id}:{self.version}>'
        
    @property
    def schema(self): return {
        'meta':      self.meta,
        'id':        self.id,
        'name':      self.name,
        'doc':       self.doc,
        'condition': self.condition,
        'version':   self.version
    }
        
    def __call__(self, data):
        _data = self._accept_meta_types[self.meta]
        _data = _data(data, self.condition)
        return _data.data
    
class IOTypeStack(object):
    
    def __init__(self, path=None, **kwargs):
        self.iotypes = {}
        if path is None: self._load_dict(kwargs)
        else: self._load_file(path)
    
    def __setitem__(self, io_id, io_data):
        _required_properties = ['id', 'meta', 'name', 'doc', 'version', 'condition']
        _filtered_data = {}
        for item in _required_properties:
            if item not in io_data: raise SyntaxError(f'Line:{io_id} is irregular')
            _filtered_data[item] = io_data[item]
        self.iotypes[io_id] = IOType(**_filtered_data)
        
    def __getitem__(self, io_id): return self.iotypes[io_id]
    def __len__(self): return len(self.iotypes)
    def __contains__(self, io_id): return io_id in self.iotypes
    def _load_dict(self, dict_): 
        for io_id, io_data in dict_.items(): self[io_id] = io_data
    def get_records(self, skip=0, limit=10):
        _keys = list(self.iotypes.keys())
        if limit <= 0: return _keys[skip:]
        else: return _keys[skip:skip+limit]
    
    def _load_file(self, path):
        if   str(path[-3:]).lower() == 'csv':  self._load_csv(path)
        elif str(path[-4:]).lower() == 'json': self._load_json(path)
        else: raise TypeError('File type not support')
    def _load_csv(self, path): self._load_dict(pd.read_csv(path).to_dict())
    def _load_json(self, path):
        with open(path, 'r') as f_: self._load_dict(json.load(f_))
        
    def to_dict(self, keys=None):
        if keys is None: return {io_id:io_data.schema for io_id, io_data in self.iotypes.items()}
        else: return {io_id:self[io_id].schema for io_id in keys}
    def to_csv(self, path=None):
        if path is None: return pd.DataFrame(self.to_dict()).to_csv()
        else: pd.DataFrame(self.to_dict()).to_csv(path_or_buf=path)
    def to_json(self, path=None):
        if path is None: return json.dumps(self.to_dict())
        else:
            with open(path, 'w') as f_: f_.write(json.dumps(self.to_dict()))