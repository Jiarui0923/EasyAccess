import re
from ._error import error_stack


class IOMetaTypeModel(object):
    _meta = 'null'
    def __init__(self, data, condition=None):
        self._meta_data = self._format(data)
        self.data = self._check(self._meta_data, condition)
    def _format(self, data): raise NotImplemented
    def _check(self, meta_data, condition=None): raise NotImplemented
    
class IOMetaTypeNumber(IOMetaTypeModel):
    _meta = 'float'
    def _format(self, data):
        try: return float(data)
        except: error_stack['IO-META-NUM']
    def _check(self, meta_data, condition=None):
        if condition is None: return meta_data
        else:
            if isinstance(condition, dict):
                _min = condition.get('min')
                _max = condition.get('max')
                if _min is not None and _max is not None and _min >= _max:
                    error_stack['IO-META-NUM-MINMAX']
                if _min is not None and meta_data < float(_min): error_stack['IO-META-NUM-MIN']
                if _max is not None and meta_data > float(_max): error_stack['IO-META-NUM-MAX']
                return meta_data
            else: error_stack['IO-META-NUM-IRR']
            
class IOMetaTypeNumberArray(IOMetaTypeModel):
    _meta = 'array(float)'
    def _format(self, data):
        try: return [float(item) for item in data]
        except: error_stack['IO-META-NUMARR']
    def _check(self, meta_data, condition=None):
        if condition is None: return meta_data
        else: error_stack['IO-META-NUMARR-IRR']
                
class IOMetaTypeString(IOMetaTypeModel):
    _meta = 'string'
    def _format(self, data):
        try: return str(data)
        except: error_stack['IO-META-STR']
    def _check(self, meta_data, condition=None):
        if condition is None: return meta_data
        else:
            if isinstance(condition, str):
                if re.fullmatch(condition, meta_data) is None: error_stack['IO-META-STR-NM']
                else: return meta_data
            else: error_stack['IO-META-STR-IRR']
