# -*- coding: utf8 -*-
"""
    ffmpegwrapper
    ~~~~~~~~~~~~~~~~~~~~

    Simple wrapper for the ffmpeg command.

    :copyright: (c) 2013 by Mathias Koehler.
    :license: BSD, see LICENSE for more details.
"""

__title__ = 'ffmpegwrapper'
__author__ = 'Mathias Koehler'
__version__ = '0.1-dev'


from .ffmpeg import FFmpeg, Input, Output
from .codec import VideoCodec, AudioCodec, NO_AUDIO, NO_VIDEO
from .filter import VideoFilter, AudioFilter
