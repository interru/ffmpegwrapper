# -*- coding: utf8 -*-
"""
    ffmpegwrapper.filter
    ~~~~~~~~~~~~~~~~~~~~

    This module provides filter methods for video and audio.

    :copyright: (c) 2013 by Mathias Koehler.
    :license: BSD, see LICENSE for more details.
"""

from itertools import chain
from .parameters import ParameterContainer


class FilterContainer(ParameterContainer):
    """Contains filters which you can append to an output file."""

    def __str__(self):
        return ",".join(FilterContainer.__iter__(self))

    def __iter__(self):
        for key, value in ParameterContainer.iteritems(self):
            if value is not None:
                yield "=".join([key, str(value)])
            else:
                yield key


class VideoFilter(FilterContainer):
    """FilterContainer for Videofilters.

    .. seealso::

        `FFmpeg documentation, Videofilter`_
            Documentation of all filters and which effect they have.

    .. _FFmpeg documentation, Videofilter:
        http://ffmpeg.org/ffmpeg.html#Video-Filters
    """

    def blackframe(self, amount, threshold):
        self.add_formatparam('blackframe', amount, threshold)
        return self

    def copy(self):
        self.add_parameter('copy', None)
        return self

    def crop(self, out_w, out_h=None, x=None, y=None):
        self.add_formatparam('crop', out_w, out_h, x, y)
        return self

    def cropdetect(self, limit=None, round=None, reset=None):
        self.add_formatparam('cropdetect', limit, round, reset)
        return self

    def drawbox(self, x, y, width, height, color):
        self.add_formatparam('drawbox', x, y, width, height, color)
        return self

    def drawtext(self, **kwargs):
        self.add_formatparam('drawtext', **kwargs)
        return self

    def fade(self, type, start, number):
        self.add_formatparam('fade', type, start, number)
        return self

    def fieldorder(self, type):
        if str(type) not in ['0', '1', 'bff', 'tff']:
            raise ValueError('Invalid Parameter for fieldorder. '
                             'Read FFmpeg manual!')
        self.add_formatparam('fieldorder', type)
        return self

    def fifo(self):
        self.add_parameter('fifo', None)
        return self

    def format(self, *args):
        self.add_formatparam('format', *args)
        return self

    def freior(self, name, *args):
        self.add_formatparam('frei0r', name, *args)
        return self

    def gradfun(self, strength='', radius=''):
        self.add_formatparam('gradfun', strength, radius)
        return self

    def hflip(self):
        self.add_parameter('hflip', None)
        return self

    def hqdn3d(self, luma_sp=None, chroma_sp=None,
               luma_tmp=None, chroma_tmp=None):
        self.add_formatparam('hqdn3d',
            luma_sp, chroma_sp, luma_tmp, chroma_tmp)
        return self

    def mp(self, **kwargs):
        self.add_formatparam('mp', **kwargs)
        return self

    def negate(self):
        self.add_parameter('negate', 1)
        return self

    def noformat(self, *args):
        self.add_formatparam('noformat', *args)
        return self

    def null(self):
        self.add_parameter('null', None)
        return self

    def overlay(self, x, y):
        self.add_formatparam('overlay', x, y)
        return self

    def pad(self, width, height, x, y, color):
        self.add_formatparam('pad', width, height, x, y, color)
        return self

    def scale(self, width=-1, height=-1):
        self.add_formatparam('scale', width, height)
        return self

    def select(self, expression):
        self.add_formatparam('select', expression)
        return self

    def setdar(self, x, y):
        self.add_formatparam('setdar', x, y)
        return self

    def setpts(self, expression):
        self.add_formatparam('setpts', expression)
        return self

    def setsar(self, x, y):
        self.add_formatparam('setsar', x, y)
        return self

    def slicify(self, height=16):
        self.add_formatparam('slicify', height)
        return self

    def transpose(self, type):
        if str(type) not in ['0', '1', '2', '3']:
            raise ValueError('Invalid Parameter for transpose. '
                             'Read FFmpeg manual')
        self.add_formatparam('transpose', type)
        return self

    def unsharp(self, *args):
        if len(args) > 6:
            message = 'unsharp() takes exactly 6 positional arguments'
            raise TypeError(message)
        self.add_formatparam('unsharp', *args)
        return self

    def vflip(self):
        self.add_parameter('vflip', None)
        return self

    def yadif(self, mode=0, parity=-1):
        self.add_formatparam('yadif', mode, parity)
        return self

    def __iter__(self):
        return chain(['-vf', FilterContainer.__str__(self)])


class AudioFilter(FilterContainer):
    """FilterContainer for Audifilters.

    .. seealso::

        `FFmpeg documentation, Audiofilter`_
            Documentation of all filters and which effect they have.

    .. _FFmpeg documentation, Audiofilter:
        http://ffmpeg.org/ffmpeg.html#Audio-Filters
    """

    def null(self):
        """does nothing"""
        self.add_parameter('null', None)
        return self

    def __iter__(self):
        return chain(['-af', FilterContainer.__str__(self)])
