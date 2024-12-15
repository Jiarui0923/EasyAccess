"""
Module: Parameter Definition

This module defines the `Parameter` class for managing parameters with associated 
metadata in the EasyAccess project. Parameters include descriptions, default values, 
optionality, and input/output types (`IOType`). The module also provides static 
methods for creating specific parameter types (string, number, numarray).

Author: Jiarui Li
Email: jli78@tulane.edu
Institution: Computer Science Department, Tulane University
"""

from .iotypemodel.iotype_model import IOType


class Parameter:
    """
    Represents a parameter with metadata such as name, type, description, and default value.

    Attributes:
        name (str): Name of the parameter.
        desc (str): Description of the parameter.
        optional (bool): Whether the parameter is optional.
        default: Default value for the parameter.
        iotype (IOType): The input/output type of the parameter.
    """

    def __init__(self, name, io_type, desc='', default_value=None, optional=False):
        """
        Initializes a Parameter instance.

        Args:
            name (str): Name of the parameter.
            io_type (IOType or dict): IOType instance or dictionary defining the type.
            desc (str, optional): Description of the parameter. Default is an empty string.
            default_value (optional): Default value for the parameter. Default is None.
            optional (bool, optional): Whether the parameter is optional. Default is False.
        """
        self.name = name
        self.desc = desc
        self.optional = optional
        self.default = default_value
        self.iotype = io_type if isinstance(io_type, IOType) else IOType(**io_type)

    def to_dict(self):
        """
        Converts the parameter to a dictionary representation.

        Returns:
            dict: A dictionary containing the parameter's attributes.
        """
        return {
            'name': self.name,
            'io_type': self.iotype.to_dict(),
            'desc': self.desc,
            'default_value': self.default,
            'optional': self.optional,
        }

    @property
    def property(self):
        """
        Provides a simplified dictionary representation of the parameter.

        Returns:
            dict: Simplified parameter attributes.
        """
        return {
            'name': self.name,
            'io': self.iotype.id,
            'optional': self.optional,
            'default': self.default,
            'desc': self.desc,
        }

    @staticmethod
    def string(name, desc='', default_value=None, optional=False):
        """
        Creates a string-type parameter.

        Args:
            name (str): Name of the parameter.
            desc (str, optional): Description of the parameter. Default is an empty string.
            default_value (optional): Default value for the parameter. Default is None.
            optional (bool, optional): Whether the parameter is optional. Default is False.

        Returns:
            Parameter: A Parameter instance of string type.
        """
        return Parameter(
            name,
            IOType(meta='string', id='string', name='string'),
            desc,
            default_value,
            optional,
        )

    @staticmethod
    def number(name, desc='', default_value=None, optional=False):
        """
        Creates a number-type parameter.

        Args:
            name (str): Name of the parameter.
            desc (str, optional): Description of the parameter. Default is an empty string.
            default_value (optional): Default value for the parameter. Default is None.
            optional (bool, optional): Whether the parameter is optional. Default is False.

        Returns:
            Parameter: A Parameter instance of number type.
        """
        return Parameter(
            name,
            IOType(meta='number', id='number', name='number'),
            desc,
            default_value,
            optional,
        )

    @staticmethod
    def numarray(name, desc='', default_value=None, optional=False):
        """
        Creates a number array-type parameter.

        Args:
            name (str): Name of the parameter.
            desc (str, optional): Description of the parameter. Default is an empty string.
            default_value (optional): Default value for the parameter. Default is None.
            optional (bool, optional): Whether the parameter is optional. Default is False.

        Returns:
            Parameter: A Parameter instance of number array type.
        """
        return Parameter(
            name,
            IOType(meta='numarray', id='numarray', name='numarray'),
            desc,
            default_value,
            optional,
        )


# Predefined metadata types
meta_types = {
    'string': IOType(meta='string', id='string', name='string'),
    'number': IOType(meta='number', id='number', name='number'),
    'numarray': IOType(meta='numarray', id='numarray', name='numarray'),
}
