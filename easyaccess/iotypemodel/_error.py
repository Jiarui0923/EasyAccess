"""
IO Type Error Handling Module
-----------------------------

This module defines custom error classes and an error stack to manage errors related to I/O types in the system.
These errors are specifically related to data validation, conditional checks, and format errors in I/O data processing.

Classes:
--------
IOTypeMetaError
    A custom error class for meta type errors (e.g., incorrect data type).
IOTypeConditionFormatError
    A custom error class for condition format errors (e.g., invalid format).
IOTypeConditionMatchError
    A custom error class for condition match errors (e.g., value not matching specified conditions).

Error Handling:
---------------
ErrorStack is instantiated to manage and track various I/O type errors with custom messages.
"""

from ..error.error import ErrorStack


class IOTypeMetaError(TypeError):
    """
    Exception raised for errors related to meta type validation.

    Inherits from the built-in TypeError.
    """

    def __init__(self, *args: object) -> None:
        """
        Initializes the IOTypeMetaError with provided arguments.

        Parameters:
        ----------
        *args : object
            The arguments to pass to the base TypeError class.
        """
        super().__init__(*args)


class IOTypeConditionFormatError(ValueError):
    """
    Exception raised for errors related to condition format validation.

    Inherits from the built-in ValueError.
    """

    def __init__(self, *args: object) -> None:
        """
        Initializes the IOTypeConditionFormatError with provided arguments.

        Parameters:
        ----------
        *args : object
            The arguments to pass to the base ValueError class.
        """
        super().__init__(*args)


class IOTypeConditionMatchError(ValueError):
    """
    Exception raised for errors related to condition match validation.

    Inherits from the built-in ValueError.
    """

    def __init__(self, *args: object) -> None:
        """
        Initializes the IOTypeConditionMatchError with provided arguments.

        Parameters:
        ----------
        *args : object
            The arguments to pass to the base ValueError class.
        """
        super().__init__(*args)


# Define module name for error identification
_module_name = 'IO-META'

# Initialize the error stack with specific error types and messages
error_stack = ErrorStack({
    f'{_module_name}-NUM': dict(type=IOTypeMetaError, info='Not float data'),
    f'{_module_name}-NUM-MIN': dict(type=IOTypeConditionMatchError, info='Value smaller than min'),
    f'{_module_name}-NUM-MAX': dict(type=IOTypeConditionMatchError, info='Value larger than max'),
    f'{_module_name}-NUM-MINMAX': dict(type=IOTypeConditionFormatError, info='Min > Max'),
    f'{_module_name}-NUM-IRR': dict(type=IOTypeConditionFormatError, info='Irregular conditional format'),
    f'{_module_name}-STR': dict(type=IOTypeMetaError, info='Not string data'),
    f'{_module_name}-STR-IRR': dict(type=IOTypeConditionFormatError, info='Irregular conditional format'),
    f'{_module_name}-STR-NM': dict(type=IOTypeConditionMatchError, info='Regular expression not match'),
    f'{_module_name}-NUMARR': dict(type=IOTypeMetaError, info='Not float array'),
    f'{_module_name}-NUMARR-IRR': dict(type=IOTypeConditionFormatError, info='Float array not support condition'),
})
