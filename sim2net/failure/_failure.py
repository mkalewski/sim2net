#!/usr/bin/env python
# -*- coding: utf-8 -*-


# (c) 2012-2013 Michal Kalewski  <mkalewski at cs.put.poznan.pl>
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
Contains an abstract class that should be implemented by all process failure
model classes.
"""


from abc import ABCMeta, abstractmethod

from sim2net.utility import logger
from sim2net.utility.randomness import get_random_generator


__docformat__ = 'reStructuredText'


#pylint: disable=R0921
class Failure(object):
    """
    This class is an abstract class that should be implemented by all process
    failure model classes.
    """

    __metaclass__ = ABCMeta

    def __init__(self, name):
        """
        *Parameters*:
            - **name** (`str`): a name of the implemented process failure
              model.
        """
        self.__random_generator = get_random_generator()
        assert self.__random_generator is not None, \
            'A random generator object expected but "None" value got!'
        self.__logger = logger.get_logger('failure.' + str(name))
        assert self.__logger is not None, \
            'A logger object expected but "None" value got!'

    @property
    def random_generator(self):
        """
        (*Property*)  An object representing the
        :class:`sim2net.utility.randomness._Randomness` pseudo-random number
        generator.
        """
        return self.__random_generator

    @property
    def logger(self):
        """
        (*Property*)  A logger object of the :class:`logging.Logger` class with
        an appropriate channel name.

        .. seealso::  :mod:`sim2net.utility.logger`
        """
        return self.__logger

    @abstractmethod
    def node_failure(self, failures):
        """
        Gives *in place* information about nodes which processes have failed
        according to the implemented process failure model.

        *Parameters*:
            - **failures** (`list`): a list of boolean values of the size equal
              to the total number of nodes in the simulated network; `True`
              value in position :math:`i` indicates that the process on node
              number :math:`i` has failed.
        """
        raise NotImplementedError('The abstract class "Failure" has no'
                                  ' implementation of the "node_failure()"'
                                  ' method!')
