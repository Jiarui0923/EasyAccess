"""
Module: EasyAccess for EasyAPI Connection and Management

This module provides the `EasyAccess` class, which facilitates the connection to EasyAPI, 
enabling algorithm discovery, task submission, and input/output management. The module 
supports both HTTP and WebSocket communication methods for efficient interaction with the API.

Author: Jiarui Li
Email: jli78@tulane.edu
Institution: Computer Science Department, Tulane University
"""

from urllib.parse import urljoin
import requests
import json
from . import docflow as doc
from .remote_algorithm import RemoteAlgorithm
from .iotypemodel.iotype_model import IOType
from .websocket import EasyAccessWebSocket
from .progress import LoadProgress


class EasyAccess:
    """
    Provides an interface to interact with the EasyAPI server, including retrieving 
    algorithm metadata, submitting tasks, and managing inputs/outputs.

    Attributes:
        host (str): The base URL of the EasyAPI server.
        api_id (str): The API ID for authentication.
        api_key (str): The API key for authentication.
        _server_info (dict): Information about the connected server.
        _entries_pair (list): List of algorithms and their IDs available on the server.
        _entries (list): List of algorithm names available on the server.
        _io_lib (dict): Cached IOType objects.
        _mode (str): The execution mode ('http' or 'websocket').
        _progressor (class): The progress reporting class.
    """

    def __init__(self, host, api_id, api_key, mode='websocket', progressor=LoadProgress):
        """
        Initializes the EasyAccess instance with server details and authentication.

        Args:
            host (str): The API server's host URL.
            api_id (str): The API ID for authentication.
            api_key (str): The API key for authentication.
            mode (str): The default communication mode ('websocket' or 'http'). Defaults to 'websocket'.
            progressor (class): A class to report task progress. Defaults to LoadProgress.
        """
        self.host = host
        self.api_id = api_id
        self.api_key = api_key
        self._server_info = self._get_server_info()
        self._entries_pair = self._get_entries(name=True)
        self._entries = [entry[0] for entry in self._entries_pair]
        self._io_lib = {
            io_id: IOType(**io_type)
            for io_id, io_type in self._get_ios(full=True).items()
        }
        self._mode = mode
        self._progressor = progressor

    def __len__(self):
        """Returns the number of available algorithms."""
        return len(self._entries)

    def __getitem__(self, entry):
        """
        Retrieves the algorithm or algorithms based on the input.

        Args:
            entry (str or list/tuple): The name of the algorithm or a list of algorithm names.

        Returns:
            RemoteAlgorithm or dict: A RemoteAlgorithm instance or a dictionary of RemoteAlgorithm instances.

        Raises:
            ModuleNotFoundError: If the specified algorithm(s) do not exist.
        """
        if isinstance(entry, str):
            if entry not in self._entries:
                raise ModuleNotFoundError(f'Algorithm {entry} does not exist.')
            return RemoteAlgorithm(self, entry, self._io_lib, mode=self._mode, progressor=self._progressor)
        if isinstance(entry, (list, tuple)):
            for _entry in entry:
                if _entry not in self._entries:
                    raise ModuleNotFoundError(f'Algorithm {_entry} does not exist.')
            entry_data = self._get_entry_inbatch(entry, io=True)
            return {
                name: RemoteAlgorithm(
                    self, name, self._io_lib, mode=self._mode, progressor=self._progressor, entry_config=config
                )
                for name, config in entry_data.items()
            }
        raise IndexError("Unsupported index type.")

    def __repr__(self):
        """Returns a string representation of the server and available algorithms."""
        return f'{self._server_info.get("server")}: {str(self._entries)}'

    def _repr_markdown_(self):
        """Returns a markdown representation of the server and algorithms."""
        server_info = self._server_info
        return doc.Document(
            doc.Title(server_info.get("server"), level=3),
            doc.Text(f'Authenticated as {server_info.get("id")}'),
            doc.Sequence({algo_id: algo_name for algo_id, algo_name in self._entries_pair}),
        ).markdown

    @property
    def algorithms(self):
        """Returns the list of available algorithms."""
        return self._entries

    def _request(self, entry='', method='GET', data=None, timeout=None):
        """
        Sends an HTTP request to the API server.

        Args:
            entry (str): The API endpoint path.
            method (str): The HTTP method ('GET' or 'POST'). Defaults to 'GET'.
            data (dict): The data to send in the request. Defaults to None.
            timeout (float): The request timeout in seconds. Defaults to None.

        Returns:
            dict: The JSON-decoded response from the server.

        Raises:
            RuntimeError: If the HTTP method is not supported.
            ConnectionError: If the response status code is not 200.
        """
        headers = {'easyapi-id': self.api_id, 'easyapi-key': self.api_key}
        full_url = urljoin(self.host, entry)
        if method.upper() == 'GET':
            response = requests.get(full_url, params=data, headers=headers, timeout=timeout)
        elif method.upper() == 'POST':
            response = requests.post(full_url, data=json.dumps(data), headers=headers, timeout=timeout)
        else:
            raise RuntimeError('Method Not Allowed')
        if response.status_code != 200:
            raise ConnectionError(f'{response.content.decode()}')
        return json.loads(response.content)

    def _websocket(self, entry=''):
        """
        Initializes a WebSocket connection.

        Args:
            entry (str): The WebSocket endpoint path.

        Returns:
            EasyAccessWebSocket: A WebSocket connection instance.
        """
        full_url = urljoin(self.host, entry).replace('http', 'ws', 1)
        headers = {'easyapi-id': self.api_id, 'easyapi-key': self.api_key}
        return EasyAccessWebSocket(host=full_url, header=headers)

    def _get_server_info(self):
        """Retrieves server information."""
        return self._request(entry='./', method='GET', timeout=0.25)

    def _get_entries(self, name=False):
        """Retrieves available algorithms."""
        data = self._request(entry='./entries/', method='GET', data={'skip': 0, 'limit': -1, 'name': name})
        return data.get('records')

    def _get_entry(self, entry_name, io=False):
        """Retrieves metadata for a specific algorithm."""
        return self._request(entry=f'./entries/{entry_name}', method='GET', data={'io': io})

    def _get_entry_inbatch(self, entry_names=None, io=False):
        """Retrieves metadata for multiple algorithms."""
        if entry_names is None:
            entry_names = []
        return self._request(entry=f'./entries/{",".join(entry_names)}', method='GET', data={'io': io})

    def _get_ios(self, full=False):
        """Retrieves input/output definitions."""
        data = self._request(entry='./io/', method='GET', data={'skip': 0, 'limit': -1, 'full': full})
        return data.get('records')

    def _submit_task(self, entry_name, params):
        """Submits a task to the API."""
        data = self._request(entry=f'./entries/{entry_name}', method='POST', data=params)
        return data.get('task_id')

    def _get_task_return(self, task_id):
        """Retrieves the result of a submitted task."""
        return self._request(entry=f'./tasks/{task_id}', method='GET')

    def _get_task_in_websocket(self, task_id):
        """Initializes a WebSocket connection for a task."""
        return self._websocket(entry=f'./tasks/{task_id}/ws')

    def _cancel_task(self, task_id):
        """Cancels a running task."""
        data = self._request(entry=f'./tasks/{task_id}/cancel', method='POST')
        return data.get('success')
