"""
Module: WebSocket Utilities for EasyAccess

This module provides WebSocket classes to facilitate communication with the EasyAPI platform. 
It includes a base `WebSocket` class and a specialized `EasyAccessWebSocket` class for 
handling EasyAPI-specific responses.

Author: Jiarui Li
Email: jli78@tulane.edu
Institution: Computer Science Department, Tulane University
"""

import websocket
import json


class WebSocket:
    """
    A generic WebSocket client for establishing and managing WebSocket connections.

    Attributes:
        _client (websocket.WebSocket): The underlying WebSocket client instance.
    """

    def __init__(self, host, header):
        """
        Initializes a WebSocket connection.

        Args:
            host (str): The WebSocket server URL.
            header (list): Headers for the WebSocket connection.
        """
        self._client = websocket.WebSocket()
        self._client.connect(url=host, header=header)

    def close(self):
        """
        Closes the WebSocket connection.
        """
        self._client.close()

    def send(self, text):
        """
        Sends a message through the WebSocket connection.

        Args:
            text (str): The message to send.
        """
        self._client.send(text)

    def recv(self):
        """
        Receives a message from the WebSocket connection.

        Returns:
            str: The received message.
        """
        return self._client.recv()

    def query(self, text):
        """
        Sends a message and waits for the response.

        Args:
            text (str): The message to send.

        Returns:
            str: The response message.
        """
        self.send(text=text)
        return self.recv()

    @property
    def connected(self):
        """
        Checks if the WebSocket connection is active.

        Returns:
            bool: True if connected, False otherwise.
        """
        return self._client.connected


class EasyAccessWebSocket(WebSocket):
    """
    A specialized WebSocket client for interacting with EasyAPI.

    Inherits from the base `WebSocket` class and adds support for parsing EasyAPI-specific 
    responses, including automatic connection closure on success.
    """

    def query(self, text):
        """
        Sends a message and processes the JSON response.

        Args:
            text (str): The message to send.

        Returns:
            dict: The parsed JSON response.
        """
        self.send(text=text)
        data = json.loads(self.recv())
        if 'success' in data:
            self.close()
        return data
