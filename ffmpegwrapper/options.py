# -*- coding: utf-8 -*-

from itertools import chain
from collections import MutableSequence, namedtuple

try:
    from itertools import ifilter
except ImportError:
    ifilter = filter


def format_parameter(*args, **kwargs):
    parameter_list = []
    for key, value in kwargs.items():
        try:
            if not value:
                parameter_list.append(key)
            else:
                parameter_list.append("=".join([key, value]))
        except TypeError:
            values = ':'.join(kwargs[key])
            parameter_list.append("=".join([key, values]))
    for value in args:
        if value is not None:
            parameter_list.append(str(value))
    result = ':'.join(parameter_list)
    if kwargs:
        return '"%s"' % result
    return result


Option = namedtuple('Option', ['name', 'value'])


class OptionStore(MutableSequence):

    def __init__(self, *containers):
        self.container_list = list(containers)

    def add_option(self, key, value):
        self.container_list.append(Option(key, value))

    def add_parameter(self, name, *args, **kwargs):
        parameter = format_parameter(*args, **kwargs)
        self.add_option(name, parameter)

    def insert(self, index, value):
        self.container_list.insert(index, value)

    def iteritems(self):
        return iter(self.container_list)

    def __iter__(self):
        return ifilter(None, chain.from_iterable(self.container_list))

    def __len__(self):
        return self.container_list.__len__()

    def __setitem__(self, index, value):
        self.container_list.__setitem__(index, value)

    def __getitem__(self, index):
        return self.container_list.__getitem__(index)

    def __delitem__(self, index):
        self.container_list.__delitem__(index)

    def __contains__(self, other):
        return self.container_list.__contains__(other)

    def __repr__(self):
        return "<{cls} {opts}>".format(
            opts=list(self), cls=self.__class__.__name__)
