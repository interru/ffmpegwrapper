# -*- coding: utf-8 -*-

from itertools import chain


class Options(dict):
    
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)

    def __iter__(self):
        return self.iteritems()

    def iteritems(self):
        for option, value in self.items():
            yield option
            if value:
                yield value

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
        for item in self._list:
            for option in item:
                yield option

    def __repr__(self):
        return "<{cls} {opts}>".format(opts=list(self),
            cls=self.__class__.__name__)
