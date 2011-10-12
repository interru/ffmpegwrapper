# -*- coding: utf8 -*-

import unittest

from ffmpegwrapper import FFmpeg, Input, Output
from ffmpegwrapper.codec import VideoCodec, AudioCodec
from ffmpegwrapper.filter import VideoFilter
from ffmpegwrapper.options import Options


class FFmpegTestCase(unittest.TestCase):

    def test_input_interface(self):
        input = Input('/old')
        self.assertEqual(list(input), ['-i', '/old'])
        self.assertEqual(input.file, '/old')

        option = Options({'-vf': 'x11grab'})
        input.append(option)
        self.assertEqual(list(input), ['-vf', 'x11grab', '-i', '/old'])
        self.assertEqual(input.pop(), option)

        input.add_option('-vf', 'x11grab')
        self.assertEqual(input.option_containers, [option])

    def test_output_interface(self):
        output = Output('/new')
        self.assertEqual(list(output), ['/new'])
        self.assertEqual(output.file, '/new')

        option = Options({'-vcodec': 'libx264'})
        output.append(option)
        self.assertEqual(list(output), ['-vcodec', 'libx264', '/new'])
        self.assertEqual(output.pop(), option)

        output.add_option('-vcodec', 'libx264')
        self.assertEqual(output.option_containers, [option])

    def test_codec_interface(self):
        codec = VideoCodec('libx264')
        self.assertEqual(list(codec), ['-vcodec', 'libx264'])

        codec = AudioCodec('ac3')
        self.assertEqual(list(codec), ['-acodec', 'ac3'])

    def test_filter_interface(self):
        filter = VideoFilter()
        filter.blackframe(1, 2).crop(792)
        self.assertEqual(list(filter), ['-vf',
            'blackframe=1:2,crop=792'])

        output = Output('/new', filter)
        self.assertEqual(list(output), ['-vf',
            'blackframe=1:2,crop=792', '/new'])

    def test_ffmpeg_interface(self):
        input = Input('/old')
        output = Output('/new')

        ffmpeg = FFmpeg('ffmpeg', input, output)
        self.assertEqual(list(ffmpeg), ['-i', '/old', '/new'])


class VideoFilter(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
