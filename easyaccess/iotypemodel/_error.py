from ..error.error import ErrorStack

class IOTypeMetaError(TypeError):
    def __init__(self, *args: object) -> None: super().__init__(*args)
class IOTypeConditionFormatError(ValueError):
    def __init__(self, *args: object) -> None: super().__init__(*args)
class IOTypeConditionMatchError(ValueError):
    def __init__(self, *args: object) -> None: super().__init__(*args)

_module_name = 'IO-META'
error_stack = ErrorStack({
    f'{_module_name}-NUM':        dict(type=IOTypeMetaError,            info='Not float data'),
    f'{_module_name}-NUM-MIN':    dict(type=IOTypeConditionMatchError,  info='Value smaller than min'),
    f'{_module_name}-NUM-MAX':    dict(type=IOTypeConditionMatchError,  info='Value larger than max'),
    f'{_module_name}-NUM-MINMAX': dict(type=IOTypeConditionFormatError, info='Min > Max'),
    f'{_module_name}-NUM-IRR':    dict(type=IOTypeConditionFormatError, info='Irregular conditional format'),
    f'{_module_name}-STR':        dict(type=IOTypeMetaError,            info='Not string data'),
    f'{_module_name}-STR-IRR':    dict(type=IOTypeConditionFormatError, info='Irregular conditional format'),
    f'{_module_name}-STR-NM':     dict(type=IOTypeConditionMatchError,  info='Regular expression not match'),
    f'{_module_name}-NUMARR':     dict(type=IOTypeMetaError,            info='Not float array'),
    f'{_module_name}-NUMARR-IRR': dict(type=IOTypeConditionFormatError, info='Float array not support condition'),
})