#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
FFmpegwrapper
~~~~~~~~~~~~~

FFmpegWrapper is a small wrapper for the ffmpeg encoder. You can append
Codec, Filters and other ParameterStores to the FFmpeg class and then run the
resulting command.

>>> from ffmpegwrapper import FFmpeg, Input, Output, VideoCodec, VideoFilter
>>> codec = VideoCodec('webm')
>>> input_video = Input('old')
>>> output_video = Output('new', videofilter, codec)
>>> FFmpeg('ffmpeg', input_video, output_video)
<FFmpeg ['ffmpeg', '-i', 'old', '-vcodec', 'webm', 'new']>


"""

from setuptools import setup

setup(
    name="ffmpegwrapper",
    version="0.1-dev",
    packages=['ffmpegwrapper'],
    author="Mathias Koehler",
    author_email="mail@mathias.im",
    url="http://github.com/interrupted/ffmpegwrapper",
    description='A simple wrapper for ffmpeg-cli',
    keywords='Video Convert Ffmpeg',
    long_description=__doc__,
    license="BSD",
    test_suite='test',
    tests_require='mock>=0.7.2',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Video',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
