from .iotypemodel.iotype_model import IOType

class Parameter(object):
    
    def __init__(self, name, io_type, desc='', default_value=None, optional=False):
        self.name = name
        self.desc = desc
        self.optional = optional
        self.default = default_value
        self.iotype = io_type if isinstance(io_type, IOType) else IOType(**io_type)
    
    def to_dict(self):
        return dict(
            name    = self.name,
            io_type = self.iotype.to_dict(),
            desc    = self.desc,
            default_value = self.default,
            optional      = self.optional
        )
    
    @property
    def property(self):
        return {
            'name': self.name,
            'io': self.iotype.id,
            'optional': self.optional,
            'default': self.default,
            'desc': self.desc
        }
    
    @staticmethod
    def string(name, desc='', default_value=None, optional=False):
        return Parameter(name, IOType(meta='string', id='string', name='string'),
                         desc, default_value, optional)
    
    @staticmethod
    def number(name, desc='', default_value=None, optional=False):
        return Parameter((name, IOType(meta='number', id='number', name='number'),
                          desc, default_value, optional))
    
    @staticmethod
    def numarray(name, desc='', default_value=None, optional=False):
        return Parameter((name, IOType(meta='numarray', id='numarray', name='numarray'),
                          desc, default_value, optional))
    
        
meta_types = {
    'string': IOType(meta='string', id='string', name='string'),
    'number': IOType(meta='number', id='number', name='number'),
    'numarray': IOType(meta='numarray', id='numarray', name='numarray'),
}  