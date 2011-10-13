# -*- coding: utf-8 -*-


class Options(dict):
    
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)

    def __iter__(self):
        for option, value in self.items():
            yield option
            if value:
                yield value

    def iteritems(self):
        for option, value in self.items():
            yield (option, value)

    def __repr__(self):
        return "<{cls} {opts}>".format(opts=list(self),
            cls=self.__class__.__name__)


class CombinedOptions(object):

    def __init__(self, *args):
        self._list = list(args)

    def __add__(self, other):
        self.append(other)

    def append(self, item):
        self._list.append(item)
    
    def insert(self, item):
        self._list.insert(item)

    def pop(self):
        return self._list.pop()

    def remove(self, item):
        self._list.remove()

    def count(self, items):
        return self._list.count()

    def index(self, item):
        return self._list.index(item)

    def add_option(self, key, value):
        self._list.append(Options({key: value}))

    @property
    def option_containers(self):
        return self._list

    def __iter__(self):
        for option in self._list:
            for item in option:
                yield item

    def iteritems(self):
        for option in self._list:
            for item in option.iteritems():
                yield item
    
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

    def __repr__(self):
        return "<{cls} {opts}>".format(opts=list(self),
            cls=self.__class__.__name__)
