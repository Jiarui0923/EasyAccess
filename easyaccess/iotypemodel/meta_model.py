"""
IOMetaType module
-----------------

This module defines a set of classes to handle different types of input/output (I/O) meta types and perform validation checks
based on specified conditions. The primary purpose is to format and validate data for specific meta types such as numbers,
number arrays, and strings. Custom error handling is done using an external error stack.

Classes:
--------
IOMetaTypeModel
    The base class for all I/O meta types, providing methods to format and check data.

IOMetaTypeNumber
    A subclass of IOMetaTypeModel that handles 'float' type data, providing methods to format and validate numbers.

IOMetaTypeNumberArray
    A subclass of IOMetaTypeModel that handles arrays of 'float' values, providing methods to format and validate number arrays.

IOMetaTypeString
    A subclass of IOMetaTypeModel that handles 'string' type data, providing methods to format and validate strings.

Functions:
----------
None (Class-based module)
"""

import re
from ._error import error_stack


class IOMetaTypeModel(object):
    """
    A base class for handling I/O meta types, providing methods for formatting and checking data.

    Attributes:
    ----------
    _meta : str
        A string representing the meta type.
    data : any
        The formatted and validated data.

    Methods:
    -------
    __init__(data, condition=None)
        Initializes the meta type model with data and an optional condition.
    _format(data)
        A method to format the data according to the meta type. This method is not implemented in the base class.
    _check(meta_data, condition=None)
        A method to validate the formatted data based on the condition. This method is not implemented in the base class.
    """
    
    _meta = 'null'

    def __init__(self, data, condition=None):
        """
        Initializes the IOMetaTypeModel instance with formatted data and a condition for validation.

        Parameters:
        ----------
        data : any
            The data to be formatted and checked.
        condition : any, optional
            A condition to validate the data (default is None).
        """
        self._meta_data = self._format(data)
        self.data = self._check(self._meta_data, condition)

    def _format(self, data):
        """
        Formats the data according to the meta type. This method should be implemented in subclasses.

        Parameters:
        ----------
        data : any
            The data to be formatted.

        Raises:
        ------
        NotImplementedError
            This method should be implemented in subclasses.
        """
        raise NotImplementedError

    def _check(self, meta_data, condition=None):
        """
        Checks the formatted data according to the condition. This method should be implemented in subclasses.

        Parameters:
        ----------
        meta_data : any
            The formatted data to be checked.
        condition : any, optional
            A condition to validate the data (default is None).

        Raises:
        ------
        NotImplementedError
            This method should be implemented in subclasses.
        """
        raise NotImplementedError


class IOMetaTypeNumber(IOMetaTypeModel):
    """
    A class that handles 'float' type data, providing methods to format and validate numbers.

    Methods:
    -------
    _format(data)
        Formats the data as a float.
    _check(meta_data, condition=None)
        Checks if the formatted data meets the specified conditions, such as minimum and maximum values.
    """
    
    _meta = 'float'

    def _format(self, data):
        """
        Formats the data as a float.

        Parameters:
        ----------
        data : any
            The data to be formatted as a float.

        Returns:
        -------
        float
            The formatted float value.

        Raises:
        ------
        Calls error_stack['IO-META-NUM'] if data cannot be converted to a float.
        """
        try:
            return float(data)
        except:
            error_stack['IO-META-NUM']

    def _check(self, meta_data, condition=None):
        """
        Checks if the formatted number meets the specified conditions.

        Parameters:
        ----------
        meta_data : float
            The formatted float value to be checked.
        condition : dict, optional
            A dictionary containing 'min' and 'max' values for validation (default is None).

        Returns:
        -------
        float
            The validated float value.

        Raises:
        ------
        error_stack['IO-META-NUM-MINMAX'] if min >= max.
        error_stack['IO-META-NUM-MIN'] if meta_data < min.
        error_stack['IO-META-NUM-MAX'] if meta_data > max.
        error_stack['IO-META-NUM-IRR'] if the condition is not a dictionary.
        """
        if condition is None:
            return meta_data
        elif isinstance(condition, dict):
            _min = condition.get('min')
            _max = condition.get('max')
            if _min is not None and _max is not None and _min >= _max:
                error_stack['IO-META-NUM-MINMAX']
            if _min is not None and meta_data < float(_min):
                error_stack['IO-META-NUM-MIN']
            if _max is not None and meta_data > float(_max):
                error_stack['IO-META-NUM-MAX']
            return meta_data
        else:
            error_stack['IO-META-NUM-IRR']


class IOMetaTypeNumberArray(IOMetaTypeModel):
    """
    A class that handles arrays of 'float' values, providing methods to format and validate number arrays.

    Methods:
    -------
    _format(data)
        Formats the data as an array of floats.
    _check(meta_data, condition=None)
        Checks if the formatted number array meets the specified condition.
    """
    
    _meta = 'array(float)'

    def _format(self, data):
        """
        Formats the data as an array of floats.

        Parameters:
        ----------
        data : any
            The data to be formatted as an array of floats.

        Returns:
        -------
        list of float
            The formatted list of float values.

        Raises:
        ------
        Calls error_stack['IO-META-NUMARR'] if data cannot be converted to a list of floats.
        """
        try:
            return [float(item) for item in data]
        except:
            error_stack['IO-META-NUMARR']

    def _check(self, meta_data, condition=None):
        """
        Checks if the formatted number array meets the specified condition.

        Parameters:
        ----------
        meta_data : list of float
            The formatted number array to be checked.
        condition : any, optional
            The condition for validation (default is None).

        Returns:
        -------
        list of float
            The validated number array.

        Raises:
        ------
        error_stack['IO-META-NUMARR-IRR'] if the condition is not valid.
        """
        if condition is None:
            return meta_data
        else:
            error_stack['IO-META-NUMARR-IRR']


class IOMetaTypeString(IOMetaTypeModel):
    """
    A class that handles 'string' type data, providing methods to format and validate strings.

    Methods:
    -------
    _format(data)
        Formats the data as a string.
    _check(meta_data, condition=None)
        Checks if the formatted string matches the specified regular expression condition.
    """
    
    _meta = 'string'

    def _format(self, data):
        """
        Formats the data as a string.

        Parameters:
        ----------
        data : any
            The data to be formatted as a string.

        Returns:
        -------
        str
            The formatted string value.

        Raises:
        ------
        Calls error_stack['IO-META-STR'] if data cannot be converted to a string.
        """
        try:
            return str(data)
        except:
            error_stack['IO-META-STR']

    def _check(self, meta_data, condition=None):
        """
        Checks if the formatted string matches the specified regular expression condition.

        Parameters:
        ----------
        meta_data : str
            The formatted string value to be checked.
        condition : str, optional
            A regular expression pattern to validate the string (default is None).

        Returns:
        -------
        str
            The validated string value.

        Raises:
        ------
        error_stack['IO-META-STR-NM'] if the string does not match the regular expression.
        error_stack['IO-META-STR-IRR'] if the condition is not a string.
        """
        if condition is None:
            return meta_data
        elif isinstance(condition, str):
            if re.fullmatch(condition, meta_data) is None:
                error_stack['IO-META-STR-NM']
            else:
                return meta_data
        else:
            error_stack['IO-META-STR-IRR']
