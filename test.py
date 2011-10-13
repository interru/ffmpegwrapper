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


class VideoFilterTestCase(unittest.TestCase):

    def setUp(self):
        self.filter = VideoFilter()

    def prefix(self, *args):
        return ['-vf'] + list(args)

    def test_blackframe(self):
        self.filter.blackframe(10, 100)
        self.assertEqual(list(self.filter),
            self.prefix('blackframe=10:100'))

    def test_copy(self):
        self.filter.copy()
        self.assertEqual(list(self.filter),
            self.prefix('copy'))

    def test_crop(self):
        self.filter.crop(100, 100)
        self.assertEqual(list(self.filter),
            self.prefix('crop=100:100'))

    def test_cropdetect(self):
        self.filter.cropdetect(10)
        self.assertEqual(list(self.filter),
            self.prefix('cropdetect=10'))

    def test_drawbox(self):
        self.filter.drawbox(10, 10, 10, 10, 'red')
        self.assertEqual(list(self.filter),
            self.prefix('drawbox=10:10:10:10:red'))

    def test_drawtext(self):
        self.filter.drawtext(fontfile="./font.ttf", text="Title")
        self.assertEqual(list(self.filter),
            self.prefix('drawtext="fontfile=./font.ttf:text=Title"'))

    def test_fade(self):
        self.filter.fade(10, 10, 10)
        self.assertEqual(list(self.filter),
            self.prefix('fade=10:10:10'))

    def test_fieldorder(self):
        self.filter.fieldorder(1)
        self.assertEqual(list(self.filter),
            self.prefix('fieldorder=1'))

    def test_fifo(self):
        self.filter.fifo()
        self.assertEqual(list(self.filter),
            self.prefix('fifo'))

    def test_format(self):
        self.filter.format('yuv420p')
        self.assertEqual(list(self.filter),
            self.prefix('format=yuv420p'))

    def test_freior(self):
        self.filter.freior('distort0r', 0.5, 0.01)
        self.assertEqual(list(self.filter),
            self.prefix('frei0r=distort0r:0.5:0.01'))

    def test_gradfun(self):
        self.filter.gradfun(10, 100)
        self.assertEqual(list(self.filter),
            self.prefix('gradfun=10:100'))

    def test_hflip(self):
        self.filter.hflip()
        self.assertEqual(list(self.filter),
            self.prefix('hflip'))

    def test_hqdn3d(self):
        self.filter.hqdn3d(2)
        self.assertEqual(list(self.filter),
            self.prefix('hqdn3d=2'))

    def test_mp(self):
        self.filter.mp(delogo=None)
        self.assertEqual(list(self.filter),
            self.prefix('mp="delogo"'))

    def test_negate(self):
        self.filter.negate()
        self.assertEqual(list(self.filter),
            self.prefix('negate=1'))

    def test_noformat(self):
        self.filter.noformat('yuv420p')
        self.assertEqual(list(self.filter),
            self.prefix('noformat=yuv420p'))

    def test_null(self):
        self.filter.null()
        self.assertEqual(list(self.filter),
            self.prefix('null'))

    def test_overlay(self):
        self.filter.overlay(10, 10)
        self.assertEqual(list(self.filter),
            self.prefix('overlay=10:10'))

    def test_scale(self):
        self.filter.scale(792)
        self.assertEqual(list(self.filter),
            self.prefix('scale=792:-1'))

    def test_select(self):
        self.filter.select(1)
        self.assertEqual(list(self.filter),
            self.prefix('select=1'))

    def test_setdar(self):
        self.filter.setdar(16, 9)
        self.assertEqual(list(self.filter),
            self.prefix('setdar=16:9'))

    def test_setsar(self):
        self.filter.setsar(16, 9)
        self.assertEqual(list(self.filter),
            self.prefix('setsar=16:9'))

    def test_slicify(self):
        self.filter.slicify(20)
        self.assertEqual(list(self.filter),
            self.prefix('slicify=20'))

    def test_transpose(self):
        self.filter.transpose(2)
        self.assertEqual(list(self.filter),
            self.prefix('transpose=2'))

    def test_unsharp(self):
        self.filter.unsharp(1, 2, 3, 4, 5, 6)
        self.assertEqual(list(self.filter),
            self.prefix('unsharp=1:2:3:4:5:6'))

    def test_vflip(self):
        self.filter.vflip()
        self.assertEqual(list(self.filter),
            self.prefix('vflip'))

    def test_yadif(self):
        self.filter.yadif()
        self.assertEqual(list(self.filter),
            self.prefix('yadif=0:-1'))


if __name__ == '__main__':
    unittest.main()
