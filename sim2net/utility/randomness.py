#!/usr/bin/env python
# -*- coding: utf-8 -*-


# (c) 2012 Michal Kalewski  <mkalewski at cs.put.poznan.pl>
#
# This file is a part of the Simple Network Simulator (sim2net) project.
# USE, MODIFICATION, COPYING AND DISTRIBUTION OF THIS SOFTWARE IS SUBJECT TO
# THE TERMS AND CONDITIONS OF THE MIT LICENSE.  YOU SHOULD HAVE RECEIVED A COPY
# OF THE MIT LICENSE ALONG WITH THIS SOFTWARE; IF NOT, YOU CAN DOWNLOAD A COPY
# FROM HTTP://WWW.OPENSOURCE.ORG/.
#
# For bug reports, feature and support requests please visit
# <https://github.com/mkalewski/sim2net/issues>.

"""
Provides a pseudo-random number generator.
"""


import random


__docformat__ = 'reStructuredText'

#: A random generator object of the :class:`_Randomness` class -- to create the
#: object a call to the :func:`get_random_generator` function is necessary.
__RANDOM_GENERATOR = None


class _Randomness(object):
    """
    This class provides a pseudo-random number generator with the use of the
    :mod:`random` module from the standard library that produces a sequence of
    numbers that meet certain statistical requirements for randomness.
    """

    def __init__(self):
        self.__random = random.Random()

    def set_state(self, generator_state):
        """
        Sets a new internal state of the generator.

        The state can be obtained from a call to :meth:`get_state` method.

        *Parameters*:
            - **generator_state**: an internal state of the generator to set.

        *Raises*:
            - **ValueError**: raised when a given value of the
              *generator_state* parameter is `None`.
        """
        if generator_state is None:
            raise ValueError('Parameter "generator_state": a random' \
                             ' generator state object expected but "None"' \
                             ' value given!')
        self.__random.setstate(generator_state)

    def get_state(self):
        """
        Returns an object capturing the current internal state of the
        generator.

        This object can be passed to :meth:`set_state` to restore the state.
        """
        return self.__random.getstate()

    def uniform(self, begin, end):
        """
        Returns a random floating point number :math:`N` such that
        :math:`begin\\leqslant N\\leqslant end` for :math:`begin\\leqslant end`
        and :math:`end\\leqslant N\\leqslant begin` for :math:`end < begin`.
        """
        return self.__random.uniform(begin, end)

    def normal(self, mikro, sigma):
        """
        Returns a random floating point number with the normal (i.e. Gaussian)
        distribution.

        *Parameters*:
            - **mikro** (`float`): a value of the mean to be used by the
              generator;
            - **sigma** (`float`): a value of the standard deviation to be used
              by the generator.
        """
        return self.__random.gauss(mikro, sigma)

    def random_order(self, sequence):
        """
        Shuffles the given **sequence** *in place*.
        """
        self.__random.shuffle(sequence)


def get_random_generator():
    """
    Returns an object representing the :class:`_Randomness` pseudo-random
    number generator.  Multiple calls to this function will return the same
    object.
    """
    global __RANDOM_GENERATOR
    if __RANDOM_GENERATOR is None:
        __RANDOM_GENERATOR = _Randomness()
    return __RANDOM_GENERATOR
