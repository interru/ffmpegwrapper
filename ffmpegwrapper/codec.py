# -*- coding: utf8 -*-
"""
    ffmpegwrapper.codec
    ~~~~~~~~~~~~~~~~~~~

    This module provides an Audio and VideoCodec
    class with methods to change various settings.

    :copyright: (c) 2013 by Mathias Koehler.
    :license: BSD, see LICENSE for more details.
"""

from itertools import chain
from .parameters import ParameterContainer


NO_AUDIO = ('-an',)
NO_VIDEO = ('-vn',)


class Codec(ParameterContainer):
    """ Container for Codecs-Settings"""

    def __init__(self, name, *args):
        self.name = name
        ParameterContainer.__init__(self, *args)


class VideoCodec(Codec):
    """This represent an video codec.

    You can append this class to an :class:`Output` object to tell
    which FFmpeg which codec you want.
    """

    def bitrate(self, bitrate):
        self.add_formatparam('-b', str(bitrate))
        return self

    def frames(self, number):
        self.add_formatparam('-vframes', str(number))
        return self

    def fps(self, fps):
        self.add_formatparam('-r', str(fps))
        return self

    def size(self, x, y):
        filter = "{x}x{y}".format(x, y)
        self.add_formatparam('-s', filter)
        return self

    def aspect(self, x, y):
        self.add_formatparam('-aspect', x, y)
        return self

    def bitrate_tolerance(self, tolerance):
        self.add_formatparam('-bt', str(tolerance))
        return self

    def max_bitrate(self, rate):
        self.add_formatparam('-maxrate', str(rate))
        return self

    def min_bitrate(self, rate):
        self.add_formatparam('-minrate', str(rate))
        return self

    def buffer_size(self, size):
        self.add_formatparam('-bufsize', str(size))
        return self

    def pass_number(self, number):
        self.add_formatparam('-pass', str(number))
        return self

    def language(self, lang):
        self.add_formatparam('-vlang', str(lang))
        return self

    def same_quality(self):
        self.add_formatparam('-sameq', None)
        return self

    def preset(self, preset):
        self.add_formatparam('-vpre', str(preset))
        return self

    def __iter__(self):
        return chain(['-vcodec', self.name], Codec.__iter__(self))


class AudioCodec(Codec):
    """This represent an audio codec.

    You can append this class to an :class:`Output` object to tell
    which FFmpeg which codec you want.
    """

    def frames(self, number):
        self.add_formatparam('-aframes', str(number))
        return self

    def frequence(self, freq):
        self.add_formatparam('-ar', str(freq))
        return self

    def bitrate(self, rate):
        self.add_formatparam('-ab', str(rate))
        return self

    def quality(self, number):
        self.add_formatparam('-aq', str(number))
        return self

    def channels(self, number):
        self.add_formatparam('-ac', str(number))
        return self

    def language(self, lang):
        self.add_formatparam('-alang', str(lang))
        return self

    def preset(self, preset):
        """Load default presets from a preset file"""
        self.add_formatparam('-apre', str(preset))
        return self

    def __iter__(self):
        return chain(['-acodec', self.name], Codec.__iter__(self))
