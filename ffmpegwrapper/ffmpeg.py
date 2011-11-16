# -*- coding: utf-8 -*-
"""
    FFmpeg

    Your entrypoint for every Task you want to do with FFmpeg

    :copyright: (c) 2011 by Mathias Koehler.
    :license: BSD, see LICENSE for more details.
"""


import os

from fcntl import fcntl, F_SETFL, F_GETFL
from select import select
from subprocess import Popen, PIPE
from itertools import chain

from .options import OptionStore, Option


class Input(OptionStore):

    def __init__(self, file, *args):
        self.file = file
        OptionStore.__init__(self, *args)

    def __iter__(self):
        return chain(OptionStore.__iter__(self), ['-i', self.file])

class Output(OptionStore):


    def __init__(self, file, *args):
        self.file = file
        OptionStore.__init__(self, *args)

    def overwrite(self):
        self.add_option('-y', None)
        return self

    def __iter__(self):
        return chain(OptionStore.__iter__(self), [self.file])


class FFmpeg(OptionStore):


    def __init__(self, binary="ffmpeg", *args):
        self.binary = binary
        OptionStore.__init__(self, *args)

    def run(self):
        """Execute through subprocess the :attr:`binary` with all Options
        that are appended in this Store as arguments.
        """
        self.pipe = Popen(list(self), stderr=PIPE)
        fcntl(self.pipe.stderr.fileno(), F_SETFL,
              fcntl(self.pipe.stderr.fileno(), F_GETFL) | os.O_NONBLOCK)
        return self

    def wait_for_data(self):
        """ As long as the :attr:`binary` is executed through :meth:`run`
        we process a syscall to check if ffmpeg has written to stderr. If
        ffmpeg has written to stderr we return true. If the binary isn't
        running any more we return False.

        This is a helper class to deal with the unbuffered output from ffmpeg
        """
        while self.pipe.poll() is None:
            ready = select([self.pipe.stderr.fileno()], [], [])[0]
            if ready:
                return True
        return False

    def poll(self):
        """Check if :attr:`binary` is running"""
        return self.pipe.poll()

    def add_option(self, key, value):
        self._list.insert(0, Option({key: value}))

    def __iter__(self):
        return chain([self.binary], OptionStore.__iter__(self))
