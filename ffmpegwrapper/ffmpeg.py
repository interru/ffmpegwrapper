# -*- coding: utf-8 -*-
"""
    FFmpeg

    Your entrypoint for every Task you want to do with FFmpeg

    :copyright: (c) 2011 by Mathias Koehler.
    :license: BSD, see LICENSE for more details.
"""

from subprocess import Popen, PIPE
from itertools import chain

from .options import CombinedOptions, Options
        

class Input(CombinedOptions):
    
    def __init__(self, file, *args):
        self.file = file
        CombinedOptions.__init__(self, *args)

    def __iter__(self):
        return chain(CombinedOptions.__iter__(self), ['-i', self.file])


class Output(CombinedOptions):
    
    def __init__(self, file, *args):
        self.file = file
        CombinedOptions.__init__(self, *args)

    def __iter__(self):
        return chain(CombinedOptions.__iter__(self), [self.file])


class FFmpeg(CombinedOptions):

    def __init__(self, binary="ffmpeg", *args):
        self.binary = binary
        CombinedOptions.__init__(self, *args)

    def run(self):
        return Popen(self, executable=self.binary, stdin=PIPE,
            stdout=PIPE, stderr=PIPE)

    def add_option(self, key, value):
        self._list.insert(0, Options({key: value}))
