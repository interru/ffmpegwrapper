# -*- coding: utf8 -*-

from itertools import chain

from .options import CombinedOptions


class CombinedFilter(CombinedOptions):

    def __str__(self):
        return ",".join(CombinedFilter.__iter__(self))

    def __iter__(self):
        for key, value in CombinedOptions.iteritems(self):
            if value is not None:
                yield "=".join([key, str(value)])            
            else:
                yield key

class VideoFilter(CombinedFilter):

    def blackframe(self, amount, threshold):
        filter = self._format_parameter(amount, threshold)
        self.add_option('blackframe', filter)
        return self

    def copy(self):
        self.add_option('copy', None)
        return self

    def crop(self, out_w, out_h=None, x=None, y=None):
        filter = self._format_parameter(out_w, out_h, x, y)
        self.add_option('crop', filter)
        return self

    def cropdetect(self, limit=None, round=None, reset=None):
        filter = self._format_parameter(limit, round, reset)
        self.add_option('cropdetect', filter)
        return self

    def drawbox(self, x, y, width, height, color):
        filter = self._format_parameter(x, y, width, height, color)
        self.add_option('drawbox', filter)
        return self

    def drawtext(self, **kwargs):
        filter = self._format_keyword_parameter(**kwargs)
        self.add_option('drawtext', filter)
        return self

    def fade(self, type, start, number):
        filter = self._format_parameter(type, start, number)
        self.add_option('fade', filter)
        return self

    def fieldorder(self, type):
        if str(type) not in ['0', '1', 'bff', 'tff']:
            raise ValueError('Invalid Option for fieldorder. '
                             'Read FFmpeg manual!')
        self.add_option('fieldorder', type)
        return self

    def fifo(self):
        self.add_option('fifo', None)
        return self

    def format(self, *args):
        filter = self._format_parameter(*args)
        self.add_option('format', filter)
        return self

    def freior(self, name, *args):
        filter = self._format_parameter(name, *args)
        self.add_option('frei0r', filter)
        return self

    def gradfun(self, strength='', radius=''):
        filter = self._format_parameter(strength, radius)
        self.add_option('gradfun', filter)
        return self

    def hflip(self):
        self.add_option('hflip', None)
        return self

    def hqdn3d(self, luma_sp=None, chroma_sp=None,
               luma_tmp=None, chroma_tmp=None):
        filter = self._format_parameter(
            luma_sp, chroma_sp, luma_tmp, chroma_tmp)
        self.add_option('hqdn3d', filter)
        return self

    def mp(self, **kwargs):
        filter = self._format_keyword_parameter(**kwargs)
        self.add_option('mp', filter)
        return self

    def negate(self):
        self.add_option('negate', 1)
        return self

    def noformat(self, *args):
        filter = self._format_parameter(*args)
        self.add_option('noformat', filter)
        return self

    def null(self):
        self.add_option('null', None)
        return self

    def overlay(self, x, y):
        filter = self._format_parameter(x, y)
        self.add_option('overlay', filter)
        return self

    def pad(self, width, height, x, y, color):
        filter = self._format_parameter(width, height, x, y, color)
        self.add_option('pad', filter)
        return self

    def scale(self, width=-1, height=-1):
        filter = self._format_parameter(width, height)
        self.add_option('scale', filter)
        return self

    def select(self, expression):
        self.add_option('select', expression)
        return self

    def setdar(self, x, y):
        filter = self._format_parameter(x, y)
        self.add_option('setdar', filter)
        return self

    def setpts(self, expression):
        self.add_option('setpts', expression)
        return self

    def setsar(self, x, y):
        filter = self._format_parameter(x, y)
        self.add_option('setsar', filter)
        return self

    def slicify(self, height=16):
        self.add_option("slicify", height)
        return self

    def transpose(self, type):
        if str(type) not in ['0', '1','2', '3']:
            raise ValueError('Invalid Option for transpose. '
                             'Read FFmpeg manual')
        self.add_option('transpose', type)
        return self

    def vflip(self):
        self.add_option('vflip', None)
        return self

    def yadif(self, mode=0, parity=-1):
        filter = self._format_parameter(mode, parity)
        self.add_option('yadif', filter)
        return self

    def _format_parameter(self, *args):
        parameter = filter(lambda x: x is not None, args)
        return ':'.join(map(str, parameter))

    def _format_keyword_parameter(self, **kwargs):
        parameter_list = []
        print(kwargs)
        for key, value in kwargs.items():
            try:
                if not value:
                    parameter_list.append(key)
                else:
                    parameter_list.append("=".join([key, value]))
            except TypeError:
                values = ':'.join(kwargs[key])
                parameter_list.append("=".join([key, values]))
        return '"' + ':'.join(parameter_list) + '"'

    def __iter__(self):
        return chain(['-vf', CombinedFilter.__str__(self)])


class AudioFilter(CombinedFilter):

    def __iter__(self):
        return chain(['-af', CombinedFilter.__str__(self)])
