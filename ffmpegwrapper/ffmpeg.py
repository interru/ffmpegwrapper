# -*- coding: utf-8 -*-
"""
    ffmpegwrapper.ffmpeg
    ~~~~~~~~~~~~~~~~~~~~

    Your entrypoint for every Task you want to do with FFmpeg

    :copyright: (c) 2013 by Mathias Koehler.
    :license: BSD, see LICENSE for more details.
"""


from subprocess import Popen, PIPE, STDOUT
from itertools import chain
from threading import Thread

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty

from .parameters import ParameterContainer, Parameter


class Input(ParameterContainer):
    """Container for an input file.

    :param file_path: Path to the input file
    :param args: A list of Containers that should be appended
    """

    def __init__(self, file_path, *args):
        self.file_path = file_path
        ParameterContainer.__init__(self, *args)

    def __iter__(self):
        return chain(ParameterContainer.__iter__(self),
                     ['-i', self.file_path])


class Output(ParameterContainer):
    """Container for an output file.

    :param file_path: Path in which the file should be saved
    :param args: A list of Containers that should be appended
    """

    def __init__(self, file_path, *args):
        self.file_path = file_path
        ParameterContainer.__init__(self, *args)

    def overwrite(self):
        """Overwrite the file if it already exist"""
        self.add_parameter('-y', None)
        return self

    def __iter__(self):
        return chain(ParameterContainer.__iter__(self), [self.file_path])


class FFmpegProcess(object):
    """Class to exectute FFmpeg.

    :param command: a sequence of the binary and it arguments
    """

    def __init__(self, command):
        self.command = list(command)
        self.queue = Queue(maxsize=2000)
        self.process = None

    def _queue_output(self, out, queue):
        """Read the output from the command bytewise. On every newline
        the line is put to the queue."""
        line = ''
        running = self.process.poll() is None

        while running:
            chunk = out.read(1).decode('utf-8')
            if chunk == '':
                running = self.process.poll() is None
                continue
            line += chunk
            if chunk in ('\n', '\r'):
                queue.put(line, timeout=0.4)
                line = ''
        out.close()

    def run(self, daemon=True):
        """Executes the command. A thread will be started to collect
        the outputs (stderr and stdout) from that command.
        The outputs will be written to the queue.

        :return: self
        """
        self.process = Popen(self.command, bufsize=1,
                             stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        thread = Thread(target=self._queue_output,
                        args=(self.process.stdout, self.queue))
        thread.deamon = daemon
        thread.start()
        return self

    def readlines(self, keepends=False):
        """Yield lines from the queue that were collected from the
        command. You can specify if you want to keep newlines at the ends.
        Default is to drop them.

        :param keepends: keep the newlines at the end. Default=False
        """
        running = self.process.poll() is None
        while running or self.queue.qsize():
            try:
                line = self.queue.get(timeout=0.05)
                if keepends:
                    yield line
                else:
                    yield line.rstrip('\r\n')
            except Empty:
                running = self.process.poll() is None

    def __getattr__(self, name):
        if self.process:
            return getattr(self.process, name)
        raise AttributeError

    def __iter__(self):
        return self.readlines()


class FFmpeg(ParameterContainer):
    """This class represents the FFmpeg command.

    It behaves like a list. If you iterate over the object it will yield
    small parts from the ffmpeg command with it arguments. The arguments
    for the command are in the Parameter classes. They can be appended
    directly or through one or more Containers.

    :param binary: The binary subprocess should execute at the :meth:`run`
    :param args: A list of Containers that should be appended
    """

    def __init__(self, binary='ffmaeg', *args):
        self.binary = binary
        self.process = None
        ParameterContainer.__init__(self, *args)

    def add_parameter(self, key, value):
        self.container_list.insert(0, Parameter(key, value))

    def run(self):
        """Executes the command of this object. Returns a
        :class:`FFmpegProcess` object which have already the
        :meth:`FFmpegProcess.run` invoked.

        :return: :class:`FFmpegProcess` object with `run()` invoked
        """
        return FFmpegProcess(self).run()

    def __enter__(self):
        self.process = self.run()
        return self.process

    def __exit__(self, exc_type, exc_value, traceback):
        if self.process.poll() is None:
            self.process.terminate()
        self.process = None

    def __iter__(self):
        return chain([self.binary], ParameterContainer.__iter__(self))
