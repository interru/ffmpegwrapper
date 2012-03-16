FFmpegWrapper
=============

.. module:: ffmpegwrapper

FFmpegWrapper is a small wrapper for the ffmpeg encoder. You can append
Codec, Filters and other ParameterContainer to the FFmpeg class and then
run the resulting command.

>>> from ffmpegwrapper import FFmpeg, Input, Output, VideoCodec, VideoFilter
>>> videofilter = VideoFilter().crop(300, 200)
>>> codec = VideoCodec('webm')
>>> input_video = Input('old')
>>> output_video = Output('new', videofilter, codec)
>>> FFmpeg('ffmpeg', input_video, output_video)
<FFmpeg ['ffmpeg', '-i', 'old', '-vf', 'crop=300:200', '-vcodec', 'webm', 'new']>



Parameter and Containers
---------------------

An Parameter is a namedtuple which represents parameters of the FFmpeg command.

Containers combines them. :class:`VideoFilter` is for example a subclassed
:class:`ParameterContainer` which can contain some filters. 

API
---

.. autoclass:: FFmpeg
    :members:

.. autoclass:: ffmpegwrapper.ffmpeg.FFmpegProcess
    :members:

Input/Output
~~~~~~~~~~~~

.. autoclass:: Input
    :members:

.. autoclass:: Output
    :members:

Codecs
~~~~~~

.. autoclass:: VideoCodec
    :members:
    :undoc-members:

.. autoclass:: AudioCodec
    :members:
    :undoc-members:

Filters
~~~~~~~

.. autoclass:: VideoFilter
    :members:
    :undoc-members:

.. autoclass:: AudioFilter
    :members:
    :undoc-members:

Container and Parameter
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ffmpegwrapper.parameters.Parameter
    :members:

.. autoclass:: ffmpegwrapper.parameters.ParameterContainer
    :members:

License
-------

Copyright (c) 2012 by Mathias Koehler.

Some rights reserved.

Redistribution and use in source and binary forms of the software as well
as documentation, with or without modification, are permitted provided
that the following conditions are met:

* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above
  copyright notice, this list of conditions and the following
  disclaimer in the documentation and/or other materials provided
  with the distribution.

* The names of the contributors may not be used to endorse or
  promote products derived from this software without specific
  prior written permission.

THIS SOFTWARE AND DOCUMENTATION IS PROVIDED BY THE COPYRIGHT HOLDERS AND
CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT
NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE AND DOCUMENTATION, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.