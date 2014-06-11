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
Supplies time-related functionality for simulations.

In this module the following terminology is used:

    *Simulation step*, :math:`s`:
        takes successive discrete values stating from 0 before each simulation
        iteration.

    *Simulation time*, :math:`t_s`:
        keeps track of the current time for the system being simulated; it
        advances to the next value in accordance with a given *simulation
        frequency* before each simulation iteration.

    *Simulation frequency*, :math:`f_s`:
        a constant that describes the relationship between the *simulation
        step* and the *simulation time* in the following manner:
        :math:`t_s=\\frac{s}{f_s}`.

    *Simulation period*, :math:`T_s`:
        a constant such that: :math:`T_s=\\frac{1}{f_s}`.
"""

from sim2net.utility import logger
from sim2net.utility.validation import check_argument_type


__docformat__ = 'reStructuredText'


class Time(object):
    """
    This class provides time abstractions for simulations.

    Class :class:`Time` keeps track of simulation steps and time in accordance
    with a given simulation frequency value.
    """

    #: A value by which the simulation step advances.
    __SIMULATION_TICK = 1

    def __init__(self):
        """
        .. warning::

            The class must be set up by calling the :meth:`setup` method.
        """
        pass

    def setup(self, simulation_frequency=1):
        """
        Initializes time abstractions for simulations.

        *Parameters*:
            - **simulation_frequency** (`int`): a value of the
              simulation frequency (greater than 0).

        *Raises*:
            - **ValueError**: raised when a given value of the simulation
              frequency is less or equal to 0.

        *Examples*:

        .. testsetup::

            from sim2net._time import Time

        .. doctest::

            >>> clock = Time()
            >>> clock.setup()
            >>> clock.tick()
            (0, 0.0)
            >>> clock.tick()
            (1, 1.0)
            >>> clock.tick()
            (2, 2.0)
            >>> clock.simulation_period
            1.0

            >>> clock = Time()
            >>> clock.setup(4)
            >>> clock.tick()
            (0, 0.0)
            >>> clock.tick()
            (1, 0.25)
            >>> clock.tick()
            (2, 0.5)
            >>> clock.tick()
            (3, 0.75)
            >>> clock.tick()
            (4, 1.0)
            >>> clock.simulation_period
            0.25
        """
        self.__logger = logger.get_logger(Time.__name__)
        assert self.__logger is not None, \
               'A logger object expected but "None" value got!'
        self.__simulation_step = int(-1)
        self.__simulation_time = float(-1.0)
        check_argument_type(Time.__name__, 'simulation_frequency', int,
                            simulation_frequency, self.__logger)
        if simulation_frequency <= 0:
            raise ValueError('Parameter "simulation_frequency": a value of' \
                             ' the simulation frequency parameter cannot be' \
                             ' less or equal to zero, but %d given!' %
                             int(simulation_frequency))
        self.__simulation_frequency = float(simulation_frequency)
        self.__simulation_period = 1.0 / self.__simulation_frequency
        self.__logger.debug('The simulation time has been initialized with' \
                            ' the simulation frequency set to %d and the' \
                            ' simulation period equal to %f' %
                            (self.__simulation_frequency,
                             self.__simulation_period))

    def __str__(self):
        """
        String representation of the class which value has the following form:
        ``current simulation step<space>current simulation time``.  Useful for
        logging purposes.
        """
        try:
            if self.__simulation_step < 0:
                return '%d %.3f' % (0, 0.0)
            return '%d %.3f' % (self.__simulation_step, self.__simulation_time)
        except AttributeError:
            return '%d %.3f' % (0, 0.0)

    @property
    def simulation_step(self):
        """
        (*Property*)  The current simulation step value of type `int`.
        """
        return self.__simulation_step

    @property
    def simulation_time(self):
        """
        (*Property*)  The current simulation time value of type `float`.
        """
        return self.__simulation_time

    @property
    def simulation_frequency(self):
        """
        (*Property*)  The simulation frequency of type `int`.
        """
        return int(self.__simulation_frequency)

    @property
    def simulation_period(self):
        """
        (*Property*)  The simulation period of type `float`.
        """
        return self.__simulation_period

    def tick(self):
        """
        Advances the simulation step and time values.

        *Returns*:
            A tuple of two values: the current simulation step (`int`) and the
            current simulation time (`float`).

        .. note::

            The first call to this method will always returns ``(0, 0.0)``.
        """
        self.__simulation_step += Time.__SIMULATION_TICK
        self.__simulation_time = \
            self.__simulation_step / self.__simulation_frequency
        if __debug__ and self.__logger.isEnabledFor('DEBUG'):
            self.__logger.debug('Tick: the current simulation step is %d' \
                                ' and the current simulation time is %.9f' %
                                (self.__simulation_step,
                                 self.__simulation_time))
        return (self.__simulation_step, self.__simulation_time)
