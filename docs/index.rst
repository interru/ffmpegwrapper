FFmpegWrapper
=============

.. module:: ffmpegwrapper

FFmpegWrapper is a small wrapper for the ffmpeg encoder. You can append
Codec, Filters and other OptionStores to the FFmpeg class and then run the
resulting command.

>>> from ffmpegwrapper import FFmpeg, Input, Output, VideoCodec, VideoFilter
>>> videofilter = VideoFilter().crop(300, 200)
>>> codec = VideoCodec('webm')
>>> input_video = Input('old')
>>> output_video = Output('new', videofilter, codec)
>>> FFmpeg('ffmpeg', input_video, output_video)
<FFmpeg ['ffmpeg', '-i', 'old', '-vf', 'crop=300:200', '-vcodec', 'webm', 'new']>



Stores and Options
------------------

There are two kinds of classes in FFmpegwrapper. The Stores and Options.
A Store is a object where you can append an Option or even Stores which
then have their own Options. A Option represent one or more arguments for
FFmpeg. A Store is more likea bigger block of Options for a specific need.
For example: Everything that describe the Output can be appended to the
Output class.


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

Stores and Options
~~~~~~~~~~~~~~~~~~

.. autoclass:: ffmpegwrapper.options.Option
    :members:

.. autoclass:: ffmpegwrapper.options.OptionStore
    :members:

License
-------
