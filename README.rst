FFmpegWrapper
=============

FFmpegWrapper is a small wrapper for the ffmpeg encoder. You can append
Codec, Filters and other parameterStores to the FFmpeg class and then run the
resulting command.

>>> from ffmpegwrapper import FFmpeg, Input, Output, VideoCodec, VideoFilter
>>> videofilter = VideoFilter().crop(300, 200)
>>> codec = VideoCodec('webm')
>>> input_video = Input('old')
>>> output_video = Output('new', videofilter, codec)
>>> FFmpeg('ffmpeg', input_video, output_video)
<FFmpeg ['ffmpeg', '-i', 'old', '-vf', 'crop=300:200', '-vcodec', 'webm', 'new']>