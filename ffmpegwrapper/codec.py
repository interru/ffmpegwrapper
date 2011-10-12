# -*- coding: utf8 -*-

from itertools import chain

from .options import CombinedOptions


class Codec(CombinedOptions):

    def __init__(self, name, *args):
        self.name = name
        CombinedOptions.__init__(self, *args)


class VideoCodec(Codec):

    def __iter__(self):
        return chain(['-vcodec', self.name], Codec.__iter__(self))


class AudioCodec(Codec):

    def __iter__(self):
        return chain(['-acodec', self.name], Codec.__iter__(self))
