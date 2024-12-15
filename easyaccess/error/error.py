"""
ErrorStack module
-----------------

This module defines a class `ErrorStack` that manages a collection of errors, allowing for error retrieval
by ID, with customized error messages and types. If an error ID is not found, an unknown error is raised.

Classes:
--------
ErrorStack
    A class for storing and retrieving errors by ID, with predefined error templates and unknown error handling.

Functions:
----------
None (Class-based module)
"""

class ErrorStack(object):
    """
    A class for managing a collection of errors and handling them by error ID.

    Attributes:
    ----------
    _err_template : dict
        A dictionary containing a template for error IDs, each with associated information and error type.
    _err_unknown : tuple
        A tuple containing the default error ID, message, and error type for unknown errors.
    errs : dict
        A dictionary of errors, where each key is an error ID and the value is another dictionary containing
        'info' (error message) and 'type' (error type).

    Methods:
    -------
    __init__(self, errs)
        Initializes the ErrorStack with a set of errors.

    __len__(self)
        Returns the number of errors stored in the stack.

    __getitem__(self, errid)
        Retrieves the error associated with the given error ID and raises the corresponding error.
    """
    
    _err_template = {
        'ERR-ID-TEMPLATE': {
            'info': 'error info',
            'type': NotImplemented,
        }
    }
    _err_unknown = ('ERR-UNKNOWN', 'Unknown error', RuntimeError)

    def __init__(self, errs):
        """
        Initializes the ErrorStack with a set of errors.

        Parameters:
        ----------
        errs : dict
            A dictionary of errors, where each key is an error ID and each value is a dictionary containing 
            'info' (error message) and 'type' (error type).
        """
        self.errs = errs

    def __len__(self):
        """
        Returns the number of errors stored in the stack.

        Returns:
        -------
        int
            The number of stored errors.
        """
        return self.errs

    def __getitem__(self, errid):
        """
        Retrieves the error associated with the given error ID and raises the corresponding error.

        Parameters:
        ----------
        errid : str
            The error ID for which to retrieve the associated error message and type.

        Raises:
        ------
        RuntimeError
            If the error ID is not found in the stack, an unknown error is raised with a predefined message.
        The error type is determined by the error associated with the ID.
        """
        if errid not in self.errs:
            raise self._err_unknown[2](f'[{self._err_unknown[0]}] {self._err_unknown[1]}')
        raise self.errs[errid]['type'](f'[{errid}] {self.errs[errid]["info"]}')
