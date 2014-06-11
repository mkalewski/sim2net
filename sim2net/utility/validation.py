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
Contains a collection of source code validation functions.
"""


__docformat__ = 'reStructuredText'


def check_argument_type(function, parameter, expected_type, argument,
                        logger=None):
    """
    Checks whether a given argument is of a given type and raises an exception
    or reports a log message if the argument's type is inappropriate.

    Checks whether a value of the *argument* parameter is of the
    *expected_type* type.  If not, it raises an exception (if *logger* object
    is `None`) or reports a log message (if *logger* object is passed)
    indicating an inappropriate type of the *parameter* parameter in the
    *function* function (or method).

    *Parameters*:
        - **function** (`str`): a name of the function which argument is to be
          checked;
        - **parameter** (`str`): a name of the parameter which argument is to
          be checked;
        - **expected_type**: an expected type of the *argument* parameter;
        - **argument**: a value of the argument that is to be checked;
        - **logger** (:mod:`logging.Logger`): a logger object that will be used
          to write the log message.

    *Raises*:
        - **TypeError**: raised when the value of *argument* is not of the
          *expected_type* type and *logger* object is not passed.

    *Example*:

    .. testsetup::

        from sim2net.utility.validation import check_argument_type

    .. doctest::

        >>> check_argument_type('function_name', 'parameter_name', str, 'argument')
    """
    if __debug__:
        obj = type(function)
    assert isinstance(function, str), \
           'In "check_argument_type()": an inappropriate type of the' \
           ' "function_name" argument, "str" expected but "%s" provided!' \
           % obj.__name__
    if __debug__:
        obj = type(parameter)
    assert isinstance(parameter, str), \
           'In "check_argument_type()": an inappropriate type of the' \
           ' "parameter" argument, "str" expected but "%s" provided!' \
           % obj.__name__
    assert expected_type is not None, \
           'In "check_argument_type()": the "expected_type" argument' \
           ' cannot be "None"!'
    if not isinstance(argument, expected_type):
        obj = type(argument)
        if logger is not None:
            logger.warning('In "%s()": an inappropriate type of the "%s"' \
                           ' argument, "%s" expected but "%s" provided' %
                           (function, parameter, expected_type.__name__,
                            obj.__name__))
        else:
            raise TypeError('In "%s()": an inappropriate type of the "%s"' \
                            ' argument, "%s" expected but "%s" provided' %
                           (function, parameter, expected_type.__name__,
                            obj.__name__))
