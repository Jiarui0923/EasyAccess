class ErrorStack(object):
    
    _err_template = {
        'ERR-ID-TEMPLATE': {
            'info': 'error info',
            'type': NotImplemented,
        }
    }
    _err_unknown = ('ERR-UNKNOWN', 'Unknown error', RuntimeError)
    def __init__(self, errs):
        self.errs = errs
        
    def __len__(self): return self.errs
    def __getitem__(self, errid):
        if errid not in self.errs: raise self._err_unknown[2](f'[{self._err_unknown[0]}] {self._err_unknown[1]}')
        raise self.errs[errid]['type'](f'[{errid}] {self.errs[errid]["info"]}')