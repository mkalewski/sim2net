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
This module provides an implementation of the crash model.

In the crash model ([CGR11]_), processes at some time may simply stop to
execute any steps, and if this is the case, the faulty processes never recover.
In this implementation, a failure for each process is determined randomly with
the use of the given *crash probability* that indicates the probability that a
process will crash during the total simulation time.  By the method used, times
at which processes crash will be distributed uniformly in the total simulation
time.  There is also a possibility to setup a *transient period* (at the
beginning of the simulation), during which process failures do not occur, and
the total number of faulty processes can also be limited to a given value.
"""


import operator

from sim2net.failure._failure import Failure
from sim2net.utility.validation import check_argument_type


__docformat__ = 'reStructuredText'


#pylint: disable=R0913
class Crash(Failure):
    """
    This class implements the process crash model.

    .. note::

        It is presumed that the :meth:`node_failure` method is called at each
        step of the simulation.
    """

    def __init__(self, time, nodes_number, crash_probability,
                 maximum_crash_number, total_simulation_steps,
                 transient_steps=0):
        """
        *Parameters*:
            - **time**: a simulation time object of the
              :class:`sim2net._time.Time` class;
            - **nodes_number** (`int`): the total number of nodes in the
              simulated network;
            - **crash_probability** (`float`): the probability that a single
              process will crash during the total simulation time;
            - **maximum_crash_number** (`int`): the maximum number of faulty
              processes;
            - **total_simulation_steps** (`int`): the total number of
              simulation steps;
            - **transient_steps** (`int`): a number of steps at the beginning
              of the simulation during which no crashes occur (default: `0`).

        *Raises*:
            - **ValueError**: raised when the given value of the *time* object
              is `None`; or when the given number of nodes is less than or
              equal to zero; or when the given crash probability is less than
              zero or grater than one; or when the given value of the maximum
              number of faulty processes or the given value of the total
              simulation steps is less than zero; or when the number of steps
              in the transient period is less than zero or greater than the
              given value of the total simulation steps.
        """
        super(Crash, self).__init__(Crash.__name__)
        if time is None:
            raise ValueError('Parameter "time": a time abstraction object'
                             ' expected but "None" value given!')
        check_argument_type(Crash.__name__, 'nodes_number', int, nodes_number,
                            self.logger)
        if nodes_number <= 0:
            raise ValueError('Parameter "nodes_number": the number of nodes'
                             ' cannot be less or equal to zero but %d given!'
                             % int(nodes_number))
        check_argument_type(Crash.__name__, 'crash_probability', float,
                            crash_probability, self.logger)
        if crash_probability < 0.0 or crash_probability > 1.0:
            raise ValueError('Parameter "crash_probability": a value of the'
                             ' crash probability parameter cannot be less'
                             ' than zero and greater than one but %f given!'
                             % float(crash_probability))
        check_argument_type(Crash.__name__, 'maximum_crash_number', int,
                            maximum_crash_number, self.logger)
        if maximum_crash_number < 0:
            raise ValueError('Parameter "maximum_crash_number": a value of'
                             ' the maximum number of crashes cannot be less'
                             ' than zero but %d given!'
                             % int(maximum_crash_number))
        check_argument_type(Crash.__name__, 'total_simulation_steps', int,
                            total_simulation_steps, self.logger)
        if total_simulation_steps < 0:
            raise ValueError('Parameter "total_simulation_steps": a value of'
                             ' the total number of simulation steps cannot be'
                             ' less than zero but %d given!'
                             % int(total_simulation_steps))
        check_argument_type(Crash.__name__, 'transient_steps', int,
                            transient_steps, self.logger)
        if transient_steps < 0 or transient_steps > total_simulation_steps:
            raise ValueError('Parameter "transient_steps": a number of the'
                             ' transient steps cannot be less than zero or'
                             ' greater than the total number of simulation'
                             ' steps but %d given!' % int(transient_steps))
        self.__time = time
        self.__crashed = \
            self.__crashes(int(nodes_number),
                           float(crash_probability), int(maximum_crash_number),
                           int(total_simulation_steps), int(transient_steps))

    def __crashes(self, nodes_number, crash_probability, maximum_crash_number,
                  total_simulation_steps, transient_steps):
        """
        Determines faulty processes and their times of crash with the use of
        the given *crash probability*.  There is also a possibility to setup a
        transient period (at the beginning of the simulation), during which
        process failures do not occur, and the total number of faulty processes
        can also be limited to a given value.

        *Parameters*:
            - **nodes_number** (`int`): the total number of nodes in the
              simulated network;
            - **crash_probability** (`float`): the probability that a single
              process will crash during the total simulation time;
            - **maximum_crash_number** (`int`): the maximum number of faulty
              processes;
            - **total_simulation_steps** (`int`): the total number of
              simulation steps;
            - **transient_steps** (`int`): a number of steps at the beginning
              of the simulation during which no crashes occur (default: `0`).

        *Returns*:
            A `list` of `tuples`; each tuple contains an identifier of the node
            with faulty process and its time of crash (in simulation steps).
            The list is sorted in ascending order by crash times.
        """
        if maximum_crash_number == 0:
            return []
        crashes = [-1] * nodes_number
        crashes_number = 0
        for node_id in xrange(nodes_number):
            crash = self.random_generator.uniform(0.0, 1.0)
            if crash <= crash_probability:
                crashes[node_id] = \
                    self.random_generator.uniform(0.0 + transient_steps,
                                                  total_simulation_steps)
                crashes_number = crashes_number + 1
                if crashes_number == maximum_crash_number:
                    break
        self.random_generator.random_order(crashes)
        crashed = dict()
        for node_id in xrange(nodes_number):
            if crashes[node_id] > 0:
                crashed[node_id] = int(crashes[node_id])
        assert len(crashed) <= maximum_crash_number, \
            'The number of faulty process (%d) is greater then the maximum' \
            ' value (%d)!' % (len(crashes), maximum_crash_number)
        return sorted(crashed.iteritems(), key=operator.itemgetter(1))

    def node_failure(self, failures):
        """
        Gives *in place* information about nodes which processes have failed
        according to the crash model.

        *Parameters*:
            - **failures** (`list`): a list of boolean values of the size equal
              to the total number of nodes in the simulated network; `True`
              value in position :math:`i` indicates that the process on node
              number :math:`i` has failed.

        *Returns*"
            A `list` of nodes which processes failed at the current simulation
            step.

        *Examples*:

        In order to avoid any process failures use this class with the
        *crash_probability* and/or *maximum_crash_number* parameters set to
        `0`, as in the examples below.

        .. testsetup::

            from sim2net._time import Time
            from sim2net.failure.crash import Crash

        .. doctest::

            >>> clock = Time()
            >>> clock.setup()
            >>> crash = Crash(clock, 4, 0.0, 0, 2)
            >>> failures = [False, False, False, False]
            >>> clock.tick()
            (0, 0.0)
            >>> crash.node_failure(failures)
            []
            >>> print failures
            [False, False, False, False]
            >>> clock.tick()
            (1, 1.0)
            >>> crash.node_failure(failures)
            []
            >>> print failures
            [False, False, False, False]

            >>> clock = Time()
            >>> clock.setup()
            >>> crash = Crash(clock, 4, 1.0, 0, 2)
            >>> failures = [False, False, False, False]
            >>> clock.tick()
            (0, 0.0)
            >>> crash.node_failure(failures)
            []
            >>> print failures
            [False, False, False, False]
            >>> clock.tick()
            (1, 1.0)
            >>> crash.node_failure(failures)
            []
            >>> print failures
            [False, False, False, False]

        """
        crashes = list()
        while self.__crashed:
            if self.__crashed[0][1] <= self.__time.simulation_step:
                failures[self.__crashed[0][0]] = True
                crashes.append(self.__crashed[0][0])
                self.logger.debug('In accordance with the node failure model'
                                  ' node #%d has failed'
                                  % self.__crashed[0][0])
                self.__crashed.pop(0)
            else:
                break
        return crashes
