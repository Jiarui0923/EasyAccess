"""
Module: LoadProgress Indicator

This module provides a simple terminal-based progress indicator for tracking 
the progress of long-running operations. The `LoadProgress` class offers 
methods to display progress markers, elapsed time, and status updates.

Author: Jiarui Li
Email: jli78@tulane.edu
Institution: Computer Science Department, Tulane University
"""

import time
import sys


class LoadProgress:
    """
    A terminal-based progress indicator.

    Attributes:
        _desc (str): Description of the current task.
        _markers (list): List of markers to display in rotation.
        _marker_iter (iter): Iterator for rotating through markers.
        _this_marker (int): Current marker index.
        _time_start (float): Start time of the progress indicator.
        _timer (bool): Flag to display elapsed time.
        _last_write_len (int): Length of the last written line to the terminal.
    """

    def __init__(self, desc='', timer=False):
        """
        Initializes the LoadProgress instance.

        Args:
            desc (str): Description of the task. Default is an empty string.
            timer (bool): If True, displays elapsed time. Default is False.
        """
        self._desc = desc
        self._markers = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self._marker_iter = iter(self._markers)
        self._this_marker = 0
        self._time_start = time.perf_counter()
        self._timer = timer
        self._last_write_len = 0
        self.show()

    def update(self, desc=None, marker=None):
        """
        Updates the progress description and marker.

        Args:
            desc (str, optional): New description for the task. If None, retains the current description.
            marker (str, optional): Specific marker to display. If None, rotates to the next marker.
        """
        self._desc = self._desc if desc is None else desc
        self._this_marker = (self._this_marker + 1) % len(self._markers)
        self.show(marker=marker)

    def _build_time(self, seconds):
        """
        Formats elapsed time into a human-readable string.

        Args:
            seconds (float): Elapsed time in seconds.

        Returns:
            str: Formatted time string.
        """
        if seconds < 60:
            return f'{seconds:.1f}s'
        elif seconds <= 3600:
            return f'{int(seconds / 60)}m{seconds % 60:.1f}s'
        else:
            return f'{int(seconds / 3600)}h{int(seconds / 60) % 60}m{seconds % 60:.1f}s'

    def show(self, marker=None):
        """
        Displays the current progress marker, description, and elapsed time if enabled.

        Args:
            marker (str, optional): Specific marker to display. If None, uses the current marker.
        """
        _marker = self._markers[self._this_marker] if marker is None else marker
        if self._timer:
            _time_used = self._build_time(time.perf_counter() - self._time_start)
            _write_str = f'[{_time_used}] {_marker} {self._desc}'
        else:
            _write_str = f'{_marker} {self._desc}'

        # Clear the last written line
        sys.stdout.write('\r' + ' ' * self._last_write_len)
        # Write the new progress line
        sys.stdout.write('\r' + _write_str)
        sys.stdout.flush()
        self._last_write_len = len(_write_str)

    def done(self, desc=None):
        """
        Marks the progress as completed with a checkmark.

        Args:
            desc (str, optional): New description to display. If None, retains the current description.
        """
        self.update(desc=desc, marker='✓')

    def error(self, desc=None):
        """
        Marks the progress as errored with a cross.

        Args:
            desc (str, optional): New description to display. If None, retains the current description.
        """
        self.update(desc=desc, marker='✗')
