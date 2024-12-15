"""
Module: IOType and IOTypeStack

This module provides classes to define and manage input-output types for the EasyAPI. 
It includes `IOType` for representing a single I/O type and `IOTypeStack` for managing 
a collection of I/O types.

Author: Jiarui Li
Email: jli78@tulane.edu
Institution: Computer Science Department, Tulane University
"""

import pandas as pd
import json

from .meta_model import IOMetaTypeString, IOMetaTypeNumber, IOMetaTypeNumberArray


class IOType:
    """
    Represents a single I/O type with metadata and validation capabilities.

    Attributes:
        meta (str): Metadata type ('string', 'number', or 'numarray').
        id (str): Unique identifier for the I/O type.
        name (str): Name of the I/O type.
        doc (str): Documentation string describing the I/O type.
        condition (optional): Validation condition for the data.
        version (str): Version of the I/O type definition.
    """

    _accept_meta_types = {
        'string': IOMetaTypeString,
        'number': IOMetaTypeNumber,
        'numarray': IOMetaTypeNumberArray,
    }

    def __init__(self, meta='string', id='', name='', doc='', condition=None, version=''):
        """
        Initializes an IOType instance.

        Args:
            meta (str): Metadata type. Default is 'string'.
            id (str): Unique identifier.
            name (str): Name of the I/O type.
            doc (str): Documentation string.
            condition: Optional validation condition.
            version (str): Version identifier.
        """
        self.meta = meta
        self.id = id
        self.name = name
        self.doc = doc
        self.condition = condition
        self.version = version

    def to_dict(self):
        """
        Converts the IOType instance to a dictionary.

        Returns:
            dict: Dictionary representation of the IOType instance.
        """
        return {
            'meta': self.meta,
            'id': self.id,
            'name': self.name,
            'doc': self.doc,
            'condition': self.condition,
            'version': self.version,
        }

    def __repr__(self):
        """
        Returns a string representation of the IOType instance.

        Returns:
            str: String representation.
        """
        return f'<{self.name}({self.meta}) {self.id}:{self.version}>'

    @property
    def schema(self):
        """
        Retrieves the schema of the IOType.

        Returns:
            dict: Schema representation.
        """
        return self.to_dict()

    def __call__(self, data):
        """
        Validates the data against the metadata type and condition.

        Args:
            data: Data to validate.

        Returns:
            Processed data after validation.
        """
        meta_type_class = self._accept_meta_types[self.meta]
        validated_data = meta_type_class(data, self.condition)
        return validated_data.data


class IOTypeStack:
    """
    Manages a collection of IOType instances.

    Attributes:
        iotypes (dict): Dictionary of IOType instances keyed by their IDs.
    """

    def __init__(self, path=None, **kwargs):
        """
        Initializes an IOTypeStack instance.

        Args:
            path (str, optional): Path to a file containing IOType definitions.
            **kwargs: Additional key-value pairs for IOType definitions.
        """
        self.iotypes = {}
        if path is None:
            self._load_dict(kwargs)
        else:
            self._load_file(path)

    def __setitem__(self, io_id, io_data):
        """
        Adds an IOType to the stack.

        Args:
            io_id (str): ID of the IOType.
            io_data (dict): Data defining the IOType.

        Raises:
            SyntaxError: If the IOType definition is invalid.
        """
        required_properties = ['id', 'meta', 'name', 'doc', 'version', 'condition']
        filtered_data = {key: io_data[key] for key in required_properties if key in io_data}
        if len(filtered_data) != len(required_properties):
            raise SyntaxError(f'Line:{io_id} is irregular')
        self.iotypes[io_id] = IOType(**filtered_data)

    def __getitem__(self, io_id):
        """Retrieves an IOType by its ID."""
        return self.iotypes[io_id]

    def __len__(self):
        """Returns the number of IOType instances."""
        return len(self.iotypes)

    def __contains__(self, io_id):
        """Checks if an IOType exists by its ID."""
        return io_id in self.iotypes

    def _load_dict(self, dict_):
        """Loads IOType definitions from a dictionary."""
        for io_id, io_data in dict_.items():
            self[io_id] = io_data

    def get_records(self, skip=0, limit=10):
        """
        Retrieves a subset of IOType IDs.

        Args:
            skip (int): Number of records to skip.
            limit (int): Number of records to retrieve. Use 0 for no limit.

        Returns:
            list: List of IOType IDs.
        """
        keys = list(self.iotypes.keys())
        return keys[skip:] if limit <= 0 else keys[skip:skip + limit]

    def _load_file(self, path):
        """
        Loads IOType definitions from a file.

        Args:
            path (str): Path to the file.

        Raises:
            TypeError: If the file type is unsupported.
        """
        if path.endswith('.csv'):
            self._load_csv(path)
        elif path.endswith('.json'):
            self._load_json(path)
        else:
            raise TypeError('File type not supported')

    def _load_csv(self, path):
        """Loads IOType definitions from a CSV file."""
        self._load_dict(pd.read_csv(path).to_dict())

    def _load_json(self, path):
        """Loads IOType definitions from a JSON file."""
        with open(path, 'r') as file:
            self._load_dict(json.load(file))

    def to_dict(self, keys=None):
        """
        Converts the IOTypeStack to a dictionary.

        Args:
            keys (list, optional): List of IOType IDs to include.

        Returns:
            dict: Dictionary representation of the stack.
        """
        if keys is None:
            return {io_id: io_data.schema for io_id, io_data in self.iotypes.items()}
        return {io_id: self[io_id].schema for io_id in keys}

    def to_csv(self, path=None):
        """
        Exports the IOTypeStack to a CSV file or returns a CSV string.

        Args:
            path (str, optional): File path to save the CSV.

        Returns:
            str: CSV string if no path is provided.
        """
        df = pd.DataFrame(self.to_dict())
        if path is None:
            return df.to_csv()
        df.to_csv(path_or_buf=path)

    def to_json(self, path=None):
        """
        Exports the IOTypeStack to a JSON file or returns a JSON string.

        Args:
            path (str, optional): File path to save the JSON.

        Returns:
            str: JSON string if no path is provided.
        """
        json_data = json.dumps(self.to_dict())
        if path is None:
            return json_data
        with open(path, 'w') as file:
            file.write(json_data)
