# -*- coding: utf-8 -*-
"""
    FFmpeg

    Your entrypoint for every Task you want to do with FFmpeg

    :copyright: (c) 2011 by Mathias Koehler.
    :license: BSD, see LICENSE for more details.
"""


from subprocess import Popen, PIPE, STDOUT
from itertools import chain
from threading import Thread

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty

from .options import OptionStore, Option


class Input(OptionStore):
    """Store for a input file.

    :param file: Path to the input file
    :param args: A list of Stores that should be appended
    """

    def __init__(self, file, *args):
        self.file = file
        OptionStore.__init__(self, *args)

    def __iter__(self):
        return chain(OptionStore.__iter__(self), ['-i', self.file])


class Output(OptionStore):
    """Store for a output file.

    :param file: Path in which the file should be saved
    :param args: A list of Stores that should be appended
    """

    def __init__(self, file, *args):
        self.file = file
        OptionStore.__init__(self, *args)

    def overwrite(self):
        """Overwrite the file if it already exist"""
        self.add_option('-y', None)
        return self

    def __iter__(self):
        return chain(OptionStore.__iter__(self), [self.file])


class FFmpegProcess(object):
    """Class to exectute FFmpeg.

    :param command: a sequence of the binary and it arguments
    """

    def __init__(self, command):
        self.command = list(command)
        self.queue = Queue()
        self.process = None

    def _queue_output(self, out, queue):
        """Read the output from the command bytewise. On every newline
        the line is put to the queue."""
        line = ''
        while self.process.poll() is None:
            chunk = out.read(1).decode('utf-8')
            if chunk == '':
                continue
            line += chunk
            if chunk in ('\n', '\r'):
                queue.put(line)
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
        while self.process.poll() is None:
            try:
                line = self.queue.get(timeout=0.1)
                if keepends:
                    yield line
                else:
                    yield line.rstrip('\r\n')
            except Empty:
                pass

    def __getattr__(self, name):
        if self.process:
            return getattr(self.process, name)
        raise AttributeError

    def __iter__(self):
        return self.readlines()



class FFmpeg(OptionStore):
    """This class represent the FFmpeg command.

    It behaves like a list. If you iterate over the object it will yield
    small parts from the ffmpeg command with it arguments. The arguments
    for the command are in the Option classes. They can be appended directly
    or through one or more Stores.

    :param binary: The binary subprocess should execute at the :meth:`run`
    :param args: A list of Stores that should be appended
    """

    def __init__(self, binary="ffmpeg", *args):
        self.binary = binary
        self.process = None
        OptionStore.__init__(self, *args)

    def add_option(self, key, value):
        self._list.insert(0, Option({key: value}))

    def run(self):
        """Executes the command of this object. Return a
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
        return chain([self.binary], OptionStore.__iter__(self))
