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
This module provides an implementation of the Gauss-Markov mobility model.

In the Gauss-Markov mobility model ([LH99]_), motion of a single node is
modelled in the form of a Gauss-Markov stochastic process.  At the beginning,
each node is assigned with an initial speed and direction, as well as mean
values of these parameters.  Then, at set intervals of time (e.g. *simulation
steps*), a new speed and direction are calculated for each node, which follow
the new course until the next time step.  This is repeated through the duration
of the simulation.  The new speed (:math:`v`) and direction (:math:`d`), at
time interval :math:`n`, are evaluated in the following manner:

* :math:`v_n=\\alpha\\times
  v_{n-1}+(1-\\alpha)\\times\\overline{v}+\\sqrt{(1-\\alpha^2)}\\times v_x`,
* :math:`d_n=\\alpha\\times
  d_{n-1}+(1-\\alpha)\\times\\overline{d}+\\sqrt{(1-\\alpha^2)}\\times d_x`;

where:

* :math:`0\\leqslant\\alpha\\leqslant 1` is a tuning parameter used to vary the
  randomness;
* :math:`\\overline{v}` is constant representing the mean value of speed;
* :math:`\\overline{d}` is constant representing the mean value of
  direction;
* :math:`v_x` and :math:`d_x` are random variables from a normal (Gaussian)
  distribution.

Consequently, at time interval :math:`n`, node's horizontal (:math:`x`) and
vertical (:math:`y`) coordinates in the simulation area are given by the
following equations:

* :math:`x_n=x_{n-1}+v_{n-1}\\times\\cos d_{n-1}`;
* :math:`y_n=y_{n-1}+v_{n-1}\\times\\sin d_{n-1}`.

It is worth to note that when :math:`\\alpha` is equal to :math:`1`, movement
becomes predictable, losing all randomness.  On the other hand, if
:math:`\\alpha` is equal to :math:`0`, the model becomes memoryless: the new
speed and direction are based completely upon the mean speed and direction
constants (:math:`\\overline{v}` and :math:`\\overline{d}`) and the Gaussian
random variables (:math:`v_x` and :math:`d_x`).


.. [LH99]  Ben Liang, Zygmunt J. Haas.  Predictive Distance-Based Mobility
   Management for PCS Networks.  In Proceedings of the *18th Annual Joint
   Conference of the IEEE Computer and Communications Societies* (INFOCOM
   1999), pp. 1377--1384, vol. 3.  New York, NY, United States, March 1999.
"""


from math import cos, fabs, pi, sin, sqrt

from sim2net.mobility._mobility import Mobility
from sim2net.utility.validation import check_argument_type


__docformat__ = 'reStructuredText'


class GaussMarkov(Mobility):
    """
    This class implements the Gauss-Markov mobility model, in which motion of
    each node is modelled in the form of a Gauss-Markov stochastic process.

    .. note::

        * Due to the characteristics of this model, it is expected that each
          node has assigned the normal speed distribution (see:
          :mod:`sim2net.speed.normal`) -- the speed is used as random variable
          :math:`v_x` when a new speed is calculated.

        * All direction values used in this implementation are expressed in
          radians.

        * The :meth:`get_current_position` method computes a position of a node
          at the current *simulation step* (see: :mod:`sim2net._time`), so it
          is presumed that the method is called at each step of the simulation.
    """

    #: Default value of the alpha parameter.
    __DEFAULT_ALPHA = 0.75

    #: Default value of the direction standard deviation.
    __DEFAULT_DIRECTION_DEVIATION = float(pi/2.0)

    #: Default direction margin used to change the direction mean to ensure
    #: that nodes do not remain near the border of the simulation area for a
    #: long period of time.
    __DEFAULT_DIRECTION_MARGIN = 0.15

    #: Default value of the direction mean.
    __DEFAULT_DIRECTION_MEAN = float(pi/0.6)


    def __init__(self, area, time, initial_coordinates, initial_speed,
                 **kwargs):
        """
        *Parameters*:
            - **area**: an object representing the simulation area;
            - **time**: a simulation time object of the
              :class:`sim2net._time.Time` class;
            - **initial_coordinates** (`list`): initial coordinates of all
              nodes; each element of this parameter should be a tuple of two
              coordinates: horizontal and vertical (respectively) of type
              `float`;
            - **initial_speed** (`float`): a value of the initial speed that is
              assigned to each node at the beginning of the simulation;
            - **kwargs** (`dict`): a dictionary of (optional) keyword
              parameters related to the Gauss-Markov mobility model; the
              following parameters are accepted:

              **alpha** (`float`)
                  The tuning parameter :math:`0\\leqslant\\alpha\\leqslant 1`
                  used to vary the randomness of movements (default: `0.75`).

              **direction_deviation** (`float`)
                  Constant representing the standard deviation of direction
                  random variable :math:`d_x` (it defaults to
                  :math:`\\frac{\\pi}{2}`).

              **direction_margin** (`float`)
                  Constant used to change direction mean :math:`\\overline{d}`
                  to ensure that nodes do not remain near a border of the
                  simulation area for a long period of time (it defaults to
                  `0.15`, or `15%` of the simulation area width/height, and
                  cannot be less than zero and greater than one; see:
                  :meth:`_GaussMarkov__velocity_recalculation`).

              **direction_mean** (`float`)
                  Constant representing mean value :math:`\\overline{d}` of
                  direction (it defaults to :math:`\\frac{\\pi}{6}`).  The same
                  value is used as mean of direction random variable
                  :math:`d_x`.

              **recalculation_interval** (`int`)
                  Velocity (i.e. speed and direction) recalculation time
                  interval (it defaults to the *simulation frequency*; see:
                  :mod:`sim2net._time`).  It determines how often, counting in
                  simulation steps, new values of velocity are recalculated.

        *Raises*:
            - **ValueError**: raised when the given value of the *area*,
              *time*, *initial_coordinates* or *initial_speed* parameter is
              `None`; or when the given value of the keyword parameter *alpha*
              is less than zero or greater that one; or when the given value of
              the (optional) keyword parameter *direction_margin* is less than
              zero or greater than one.

        *Example*:

        .. doctest::
            :options: +SKIP

            >>> gm = GaussMarkov(area, time, coordinates, 10.0, alpha=0.35)

        """
        if area is None:
            raise ValueError('Parameter "area": a simulation area object' \
                             ' expected but "None" value given!')
        if time is None:
            raise ValueError('Parameter "time": a time abstraction object' \
                             ' expected but "None" value given!')
        if initial_coordinates is None:
            raise ValueError('Parameter "initial_coordinates": identifiers' \
                             ' of nodes expected but "None" value given!')
        if initial_speed is None:
            raise ValueError('Parameter "initial_speed": a value of the' \
                             ' initial speed of nodes expected but "None"' \
                             ' value given!')
        Mobility.__init__(self, GaussMarkov.__name__)
        self.__area = area
        self.__time = time
        check_argument_type(GaussMarkov.__name__, 'initial_coordinates', list,
                            initial_coordinates, self.logger)
        check_argument_type(GaussMarkov.__name__, 'initial_speed', float,
                            initial_speed, self.logger)
        if 'alpha' in kwargs:
            check_argument_type(GaussMarkov.__name__, 'alpha', float,
                                kwargs['alpha'], self.logger)
            if kwargs['alpha'] < 0.0 or kwargs['alpha'] > 1.0:
                raise ValueError('Keyword parameter "alpha": a value of the' \
                                 ' "alpha" parameter cannot be less than' \
                                 ' zero and greater than one but %f given!' \
                                 % float(kwargs['alpha']))
        if 'direction_deviation' in kwargs:
            check_argument_type(GaussMarkov.__name__, 'direction_deviation',
                                float, kwargs['direction_deviation'],
                                self.logger)
        if 'direction_margin' in kwargs:
            check_argument_type(GaussMarkov.__name__, 'direction_margin',
                                float, kwargs['direction_margin'], self.logger)
            if kwargs['direction_margin'] < 0.0 \
               or kwargs['direction_margin'] > 1.0:
                raise ValueError('Keyword parameter "direction_margin": a' \
                                 ' value of the direction margin cannot be' \
                                 ' less than zero and greater than one but' \
                                 ' %f given!' \
                                 % float(kwargs['direction_margin']))
        if 'direction_mean' in kwargs:
            check_argument_type(GaussMarkov.__name__, 'direction_mean', float,
                                kwargs['direction_mean'], self.logger)
        if 'recalculation_interval' in kwargs:
            check_argument_type(GaussMarkov.__name__, 'recalculation_interval',
                                int, kwargs['recalculation_interval'],
                                self.logger)
        self.__alpha = float(kwargs.get('alpha', GaussMarkov.__DEFAULT_ALPHA))
        self.__direction_deviation = \
            float(kwargs.get('direction_deviation',
                             GaussMarkov.__DEFAULT_DIRECTION_DEVIATION))
        self.__direction_margin = \
            float(kwargs.get('direction_margin',
                             GaussMarkov.__DEFAULT_DIRECTION_MARGIN))
        self.__direction_mean = \
            float(kwargs.get('direction_mean',
                             GaussMarkov.__DEFAULT_DIRECTION_MEAN))
        self.__recalculation_interval = \
            int(kwargs.get('recalculation_interval',
                           self.__time.simulation_frequency))
        # 1.0 - alpha:
        self.__gauss_markov_factor_one = 1.0 - self.__alpha
        # sqrt((1.0 - alpha^2)):
        self.__gauss_markov_factor_two = sqrt(1.0 - (pow(self.__alpha, 2.0)))
        # area width * direction margin:
        self.__width_left = self.__area.width * self.__direction_margin
        # area width - (area width * direction margin):
        self.__width_right = self.__area.width - self.__width_left
        # area height * direction margin:
        self.__height_bottom = self.__area.height * self.__direction_margin
        # area height - (area height * direction margin):
        self.__height_top = self.__area.height - self.__height_bottom
        # { node id:
        #     { 'speed':      current speed),
        #       'direction':  current direction } }
        self.__velocities = dict()
        for node_id in range(0, len(initial_coordinates)):
            self.__velocities[node_id] = dict()
            self.__velocities[node_id]['speed'] = float(initial_speed)
            self.__velocities[node_id]['direction'] = \
                self.__get_new_direction()
        self.logger.debug('Speed and direction values has been initialized' \
                          ' for %d nodes' % len(self.__velocities))

    def __get_new_direction(self):
        """
        Randomizes a new direction with the normal (Gaussian) distribution.

        *Returns*:
            (`float`) a newly randomized direction value.
        """
        return fabs(self.random_generator.normal(self.__direction_mean,
                                                 self.__direction_deviation))

    def __velocity_recalculation(self, node_id, node_speed, node_coordinates):
        """
        Recalculates a node's velocity, i.e. its speed and direction, as a
        Gauss-Markov stochastic process.

        To ensure that a node does not remain near a border of the simulation
        area for a long period of time, the node is forced away from the border
        when it moves within certain distance of the edge.  This is done by
        modifying mean direction :math:`\\overline{d}`.  For example, when a
        node is near the right border of the simulation area, the value of
        :math:`\\overline{d}` changes to 180 degrees (:math:`\\pi`).  The
        distance that is used in this method is calculated as a product of the
        **direction margin** and area width or height.

        *Parameters*:
            - **node_id** (`int`): an identifier of the node;
            - **node_speed**: an object representing the node's speed;
            - **node_coordinates** (`list`): values of the node's horizontal
              and vertical coordinates at the previous simulation step.
        """
        # speed
        random_speed = node_speed.get_new()
        self.__velocities[node_id]['speed'] = \
            fabs((self.__alpha * self.__velocities[node_id]['speed'])
                 + (self.__gauss_markov_factor_one * node_speed.mean)
                 + (self.__gauss_markov_factor_two * random_speed))
        # direction
        if node_coordinates[1] >= self.__height_top:
            if node_coordinates[0] <= self.__width_left:
                mean = (7.0/4.0)*pi
            elif node_coordinates[0] >= self.__width_right:
                mean = (5.0/4.0)*pi
            else:
                mean = (3.0/2.0)*pi
        elif node_coordinates[1] <= self.__height_bottom:
            if node_coordinates[0] <= self.__width_left:
                mean = pi/4.0
            elif node_coordinates[0] >= self.__width_right:
                mean = (3.0/4.0)*pi
            else:
                mean = pi/2.0
        elif node_coordinates[0] <= self.__width_left:
            mean = 0.0
        elif node_coordinates[0] >= self.__width_right:
            mean = pi
        else:
            mean = self.__direction_mean
        random_direction = self.__get_new_direction()
        self.__velocities[node_id]['direction'] = \
            (self.__alpha * self.__velocities[node_id]['direction']) \
            + (self.__gauss_markov_factor_one * mean) \
            + (self.__gauss_markov_factor_two * random_direction)
        if self.logger.isEnabledFor('DEBUG'):
            msg = 'A new velocity has been selected for the node #%d: the' \
                  ' new speed is equal to %f and the new direction is equal' \
                  ' to %f'
            self.logger.debug(msg %
                              (node_id, self.__velocities[node_id]['speed'],
                               self.__velocities[node_id]['direction']))

    def __step_move(self, node_id, node_coordinates):
        """
        Computes a node's position at the current simulation step.

        *Parameters*:
            - **node_id** (`int`): an identifier of the node;
            - **node_coordinates** (`list`): values of the node's horizontal
              and vertical coordinates at the previous simulation step.

        *Returns*:
            (`tuple`) current values of the node's horizontal and vertical
            coordinates.
        """
        horizontal_coordinate = \
            node_coordinates[0] \
            + (self.__velocities[node_id]['speed'] \
               * cos(self.__velocities[node_id]['direction']))
        horizontal_coordinate = \
            node_coordinates[0] \
            + ((horizontal_coordinate - node_coordinates[0]) \
                * self.__time.simulation_period)
        if horizontal_coordinate < 0.0:
            horizontal_coordinate = 0.0
            self.__velocities[node_id]['direction'] = \
                (2.0*pi) - (2.0*self.__velocities[node_id]['direction'])
        elif horizontal_coordinate > self.__area.width:
            horizontal_coordinate = \
                self.__area.width - (horizontal_coordinate - self.__area.width)
            self.__velocities[node_id]['direction'] = \
                (2.0*pi) - (2.0*self.__velocities[node_id]['direction'])
        vertical_coordinate = \
            node_coordinates[1] \
            + (self.__velocities[node_id]['speed'] \
               * sin(self.__velocities[node_id]['direction']))
        vertical_coordinate = \
            node_coordinates[1] \
            + ((vertical_coordinate - node_coordinates[1]) \
                * self.__time.simulation_period)
        if vertical_coordinate < 0.0:
            vertical_coordinate = 0.0
            self.__velocities[node_id]['direction'] = \
                (2.0*pi) - (2.0*self.__velocities[node_id]['direction'])
        elif vertical_coordinate > self.__area.height:
            vertical_coordinate = \
                self.__area.height - (vertical_coordinate - self.__area.height)
            self.__velocities[node_id]['direction'] = \
                (2.0*pi) - (2.0*self.__velocities[node_id]['direction'])
        return (horizontal_coordinate, vertical_coordinate)

    def get_current_position(self, node_id, node_speed, node_coordinates):
        """
        Calculates and returns a node's position at the current simulation step
        in accordance with the Gauss-Markov mobility model.

        A distance of the route traveled by the node, between the current and
        previous simulation steps, is calculated as the product of the current
        node's speed and the *simulation period* (see: :mod:`sim2net._time`
        module).  Therefore, it is assumed that this method is called at every
        simulation step.

        *Parameters*:
            - **node_id** (`int`): an identifier of the node;
            - **node_speed**: an object representing the node's speed;
            - **node_coordinates** (`list`): values of the node's horizontal
              and vertical coordinates at the previous simulation step.

        *Returns*:
            A tuple containing current values of the node's horizontal and
            vertical coordinates.
        """
        if self.__time.simulation_step == 0:
            if __debug__ and self.logger.isEnabledFor('DEBUG'):
                msg = 'The current position of the node #%d is (%f, %f) with' \
                      ' the current speed equal to %f and direction equal to' \
                      ' %f'
                self.logger.debug(msg %
                    (node_id, node_coordinates[0], node_coordinates[1],
                     self.__velocities[node_id]['speed'],
                     self.__velocities[node_id]['direction']))
            return node_coordinates
        coordinates = self.__step_move(node_id, node_coordinates)
        if __debug__ and self.logger.isEnabledFor('DEBUG'):
            msg = 'The current position of the node #%d is (%f, %f) with the' \
                  ' current speed equal to %f and direction equal to %f'
            self.logger.debug(msg % (node_id, coordinates[0], coordinates[1],
                                     self.__velocities[node_id]['speed'],
                                     self.__velocities[node_id]['direction']))
        if self.__time.simulation_step % self.__recalculation_interval == 0:
            self.__velocity_recalculation(node_id, node_speed, node_coordinates)
        # print "%.30f    %.30f" % (coordinates[0], coordinates[1])
        return coordinates
