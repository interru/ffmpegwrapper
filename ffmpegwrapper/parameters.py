# -*- coding: utf-8 -*-
"""
    ffmpegwrapper.parameters
    ~~~~~~~~~~~~~~~~~~~~~

    Implements a basic structure for commandline
    arguments and some helpers to operate with them.

    :copyright: (c) 2013 by Mathias Koehler.
    :license: BSD, see LICENSE for more details.
"""
from itertools import chain
from collections import MutableSequence, namedtuple

try:
    from itertools import ifilter
except ImportError:
    ifilter = filter


def format_parameter(*args, **kwargs):
    """Format a parameter string

    >>> format_parameter(ex=['example', 'one'])
    '"ex=example:one"'
    >>> format_parameter('one', 'two', 'three')
    'one:two:three'

    You can mix the arguments und keyword arguments.
    """
    parameter_list = []
    for value in args:
        if value is not None:
            parameter_list.append(str(value))
    for key, value in kwargs.items():
        try:
            if not value:
                parameter_list.append(key)
            else:
                parameter_list.append("=".join([key, value]))
        except TypeError:
            values = ':'.join(kwargs[key])
            parameter_list.append("=".join([key, values]))
    result = ':'.join(parameter_list)
    if kwargs:
        return '"%s"' % result
    return result


Parameter = namedtuple('Parameter', ['name', 'value'])


class ParameterContainer(MutableSequence):

    def __init__(self, *containers):
        self.container_list = list(containers)

    def add_parameter(self, key, value):
        """Adds an parameter to the container."""
        self.container_list.append(Parameter(key, value))

    def add_formatparam(self, name, *args, **kwargs):
        """Format the value of an parameter from the *args **kwargs
        and append it to the container."""
        parameter = format_parameter(*args, **kwargs)
        self.add_parameter(name, parameter)

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
