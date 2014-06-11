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
Provides functions which implement an event logging system with the use of the
:mod:`logging` module from the standard library.
"""


import logging


__docformat__ = 'reStructuredText'

#: Default logging level.
__DEFAULT_LOGGING_LEVEL = logging.DEBUG

#: Main logging channel used by the simulator.
__MAIN_LOGGING_CHANNEL = 'sim2net'

#: Indicates whether the main logger has been created (by a call to the
#: :func:`create_logger` function).
__CREATED = False


class Sim2NetFormatter(logging.Formatter):
    """
    Implements a custom :class:`logging.Formatter` that can also log
    simulation steps and time (see: :mod:`sim2net._time`).
    """

    #: Default logs format.
    __DEFAULT_LOGGING_FORMAT = \
        '%(asctime)s.%(msecs)03d [%(name)s] %(levelname)s - %(message)s'

    #: Default date and time format for logs.
    __DEFAULT_DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'


    def __init__(self, time=None):
        """
        *Parameters*:
            - **time**: a simulation time object of the
              :class:`sim2net._time.Time` class to log simulation steps and
              time.
        """
        self.__time = time
        logging.Formatter. \
            __init__(self,
                     fmt=Sim2NetFormatter.__DEFAULT_LOGGING_FORMAT,
                     datefmt = Sim2NetFormatter.__DEFAULT_DATETIME_FORMAT)

    def format(self, record):
        """
        Formats the specified record as text and adds the current simulations
        step and time if the time object is present.
        """
        msg = logging.Formatter.format(self, record)
        if self.__time is None:
            return msg[:24] + '%d %f ' % (0, 0.0) + msg[24:]
        else:
            return msg[:24] + '%s ' % self.__time + msg[24:]


def __channel_string(channel):
    """
    Returns a logging channel string for a given string.
    """
    return __MAIN_LOGGING_CHANNEL + '.' + str(channel).lower()

def create_logger(time=None, level=None, handler=None, formatter=None):
    """
    Creates and configures a logger for the main logging channel.

    If no *handler* is passed, the
    :class:`sim2net.utility.logger.Sim2NetFormatter` formatter is used.

    *Parameters*:
        - **time**: a simulation time object of the :class:`sim2net._time.Time`
          class to log simulation steps and time;
        - **level**: a logging level that will be set to the logger (and its
          handler if the handler is not passed as an argument);  the level can
          be passed as a string or a :mod:`logging` module's level;
        - **handler**: an object representing the handler to be used with the
          logger (see :mod:`logging.handlers` in the standard library);
        - **formatter**: an object representing the log format to be used with
          the logger's handler (see :class:`logging.Formatter` class in the
          standard library).

    *Returns*:
        A :class:`logging.Logger` object for a newly created logger.
    """
    logger = logging.getLogger()
    if level is None:
        logger.setLevel(__DEFAULT_LOGGING_LEVEL)
    elif isinstance(level, str):
        logger.setLevel(level.upper())
    else:
        logger.setLevel(level)
    if handler is None:
        handler = logging.StreamHandler()
        handler.setLevel(__DEFAULT_LOGGING_LEVEL)
    if formatter is None:
        formatter = Sim2NetFormatter(time)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    global __CREATED
    __CREATED = True
    return logging.getLogger(__MAIN_LOGGING_CHANNEL)

def get_logger(channel=None):
    """
    Returns a logger object.  Multiple calls to this function with the same
    channel string will return the same object.

    *Parameters*:
        - **channel** (`str`): a string that represents a logging channel.

    *Returns*:
        A :class:`logging.Logger` object for the given logging **channel** or
        the main channel logger if **channel** argument is `None`.

    *Examples*:

    .. testsetup::

        from sim2net.utility import logger

    .. doctest::

        >>> main_channel_logger = logger.create_logger()
        >>> main_channel_logger = logger.get_logger()
        >>> new_channel_logger = logger.get_logger('my_channel')
    """
    if channel is None and not __CREATED:
        return create_logger()
    if channel is None:
        return logging.getLogger(__MAIN_LOGGING_CHANNEL)
    if not __CREATED:
        create_logger()
    return logging.getLogger(__channel_string(channel))
