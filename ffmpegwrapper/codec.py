# -*- coding: utf8 -*-

from itertools import chain

from .options import OptionStore


NO_AUDIO = ['-an']
NO_VIDEO = ['-vn']


class Codec(OptionStore):

    def __init__(self, name, *args):
        self.name = name
        OptionStore.__init__(self, *args)


class VideoCodec(Codec):
    """This represent an video codec.
    
    You can append this class to an :class:`Output` object to tell
    which FFmpeg which codec you want."""

    def bitrate(self, bitrate):
        self.add_option('-b', str(bitrate))
        return self

    def frames(self, number):
        self.add_option('-vframes', str(number))
        return self

    def fps(self, fps):
        self.add_option('-r', str(fps))
        return self

    def size(self, x, y):
        filter = "{x}x{y}".format(x, y)
        self.add_option('-s', filter)
        return self

    def aspect(self, x, y):
        filter = self._format_parameter(x, y)
        self.add_option('-aspect', filter)
        return self

    def bitrate_tolerance(self, tolerance):
        self.add_option('-bt', str(tolerance))
        return self

    def max_bitrate(self, rate):
        self.add_option('-maxrate', str(rate))
        return self

    def min_bitrate(self, rate):
        self.add_option('-minrate', str(rate))
        return self

    def buffer_size(self, size):
        self.add_option('-bufsize', str(size))
        return self

    def pass_number(self, number):
        self.add_option('-pass', str(number))
        return self

    def language(self, lang):
        self.add_option('-vlang', str(lang))
        return self

    def same_quality(self):
        self.add_option('-sameq', None)
        return self

    def preset(self, preset):
        self.add_option('-vpre', str(preset))
        return self

    def __iter__(self):
        return chain(['-vcodec', self.name], Codec.__iter__(self))


class AudioCodec(Codec):
    """This represent an audio codec.
    
    You can append this class to an :class:`Output` object to tell
    which FFmpeg which codec you want."""

    def frames(self, number):
        self.add_option('-aframes', str(number))
        return self

    def frequence(self, freq):
        self.add_option('-ar', str(freq))
        return self

    def bitrate(self, rate):
        self.add_option('-ab', str(rate))
        return self

    def quality(self, number):
        self.add_option('-aq', str(number))
        return self

    def channels(self, number):
        self.add_option('-ac', str(number))
        return self

    def language(self, lang):
        self.add_option('-alang', str(lang))
        return self

    def preset(self, preset):
        """Load default presets from a preset file"""
        self.add_option('-apre', str(preset))
        return self

    def __iter__(self):
        return chain(['-acodec', self.name], Codec.__iter__(self))
