#!/usr/bin/env python
# -*- coding: utf-8 -*-


# (c) 2012-2014 Michal Kalewski  <mkalewski at cs.put.poznan.pl>
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
This module provides an implementation of the mobile ad hoc network that is to
be simulated.

The network is composed of the given number of nodes running the provided
simulation application.  The main method of this module, the
:func:`sim2net._network.Network.step` method, is called at each simulation step
and it advances the simulation by computing node failures, new positions of the
nodes, performing direct communication between neighboring nodes, and executing
the simulation application at each node.

Additionally, the :class:`sim2net._network._Communication` class is
implemented, which serves as a communication interface for the simulated nodes.
"""


from copy import deepcopy

from sim2net._channel import Channel
from sim2net.utility import logger


__docformat__ = 'reStructuredText'


class _Communication(object):
    """
    This class implements a communication interface for the simulated nodes
    providing two methods for sending and receiving application messages.
    """

    def __init__(self, node_id, send_message, receive_message):
        """
        *Parameters*:
            - **node_id** (`int`): an identifier of the node;
            - **send_message**: a sending method in the
              :class:`sim2net._network.Network` class;
            - **receive_message**: a receiving method in the
              :class:`sim2net._network.Network` class.
        """
        self.__node_id = node_id
        self.__send_message = send_message
        self.__receive_message = receive_message

    def send(self, message):
        """
        Sends an application message.

        *Parameters*:
            - **message**: the application message to send of any type.
        """
        self.__send_message(self.__node_id, message)

    def receive(self):
        """
        Returns None value if there is no message at the current simulation
        step, or a tuple that contains an identifier of the sender and the
        received application message.
        """
        return self.__receive_message(self.__node_id)


class Network(object):
    """
    This class implements the mobile ad hoc network that is to be simulated.
    """

    #: Simulator modules that form the network environment for simulations.
    __ENVIRONMENT = {
        'application': None,  # a class of the simulation application
        'failure': None,  # an object that implements 'sim2net.failure'
        'mobility': None,  # an object that implements 'sim2net.mobility'
        'propagation': None,  # an object that implements 'sim2net.propagation'
        'time': None,  # an object that implements 'sim2net._time''
        'maximum_transmission_time': None,  # float value
        'initial_coordinates': None,  # a list of initial coordinates
        'speed': None,  # a list of speed objects for all nodes
        'packet_loss': None}  #: a list of packet loss objects for all nodes

    def __init__(self, environment):
        """
        *Parameters*:
            - **environment**: a dictionary that contains objects, which form
              the network environment for simulations (see
              :attr:`sim2net._network.Network.__ENVIRONMENT` for the objects
              list).
        """
        self.__logger = logger.get_logger(Network.__name__)
        self.__logger.debug('Initializing the simulated network')
        try:
            for key in Network.__ENVIRONMENT:
                if environment[key] is None:
                    raise KeyError(key)
        except KeyError, err:
            self.__logger.critical('No settings given for "%s" parameter!'
                                   % err)
            raise
        # NETWORK
        self.__network = dict()
        self.__network['time'] = environment['time']
        self.__network['mobility'] = environment['mobility']
        self.__network['propagation'] = environment['propagation']
        self.__network['failure'] = environment['failure']
        # NODES
        self.__nodes_number = len(environment['initial_coordinates'])
        self.__nodes = dict()
        self.__nodes['coordinates'] = environment['initial_coordinates']
        self.__nodes['speed'] = environment['speed']
        self.__nodes['neighbors'] = \
            self.__network['propagation'] \
                .get_neighbors(self.__nodes['coordinates'])
        self.__nodes['channel'] = \
            [Channel(self.__network['time'], environment['packet_loss'][node],
                     node, environment['maximum_transmission_time'])
                for node in range(0, self.__nodes_number)]
        self.__nodes['communication'] = \
            [_Communication(node, self.communication_send,
                            self.communication_receive)
                for node in range(0, self.__nodes_number)]
        self.__nodes['failure'] = [False] * self.__nodes_number
        self.__network['shared'] = dict()
        self.__nodes['application'] = \
            [environment['application']()
                for node in range(0, self.__nodes_number)]
        self.__logger.debug('Initializing the "%s" application for %d nodes'
                            % (environment['application'].__name__,
                               self.__nodes_number))
        for node in range(0, self.__nodes_number):
            self.__nodes['application'][node].initialize(
                node, self.__network['shared'])
        self.__current_time = self.__network['time'].tick()

    def communication_send(self, node_id, message):
        """
        Sends an application message.

        *Parameters*:
            - **node_id** (`int`): an identifier of the sender;
            - **message**:  the application message to send of any type.

        .. warning::

            This method uses the :func:`copy.deepcopy` function, and hence may
            be slow.

        .. seealso:: :class:`sim2net._network._Communication`
        """
        self.__nodes['channel'][node_id].send_message(
            deepcopy(message), self.__nodes['neighbors'][node_id])

    def communication_receive(self, node_id):
        """
        Receives an application message for the given node.

        *Parameters*:
            - **node_id** (`int`): an identifier of the receiver.

        *Returns*:
            None value if there is no message at the current simulation step
            for the receiver, or a tuple that contains an identifier of the
            sender and the received application message.

        .. seealso:: :class:`sim2net._network._Communication`
        """
        return self.__nodes['channel'][node_id].receive_message()

    def __failure(self):
        """
        Computes node failures at the current simulation step.

        .. seealso:: :mod:`sim2net.failure`
        """
        failures = \
            self.__network['failure'].node_failure(self.__nodes['failure'])
        for failure in failures:
            self.__nodes['application'][failure].failure(
                self.__current_time, self.__network['shared'])

    def __move(self):
        """
        Calculates new positions of the simulated nodes at the current
        simulation step.

        .. seealso:: :mod:`sim2net.mobility`
        """
        for node in range(0, self.__nodes_number):
            self.__nodes['coordinates'][node] = \
                self.__network['mobility'].get_current_position(
                    node, self.__nodes['speed'][node],
                    self.__nodes['coordinates'][node])

    def __neighborhood(self):
        """
        Calculates neighboring nodes at the current simulation step.

        .. seealso:: :mod:`sim2net.propagation`
        """
        self.__nodes['neighbors'] = \
            self.__network['propagation'] \
                .get_neighbors(self.__nodes['coordinates'])
        # print self.__nodes['neighbors']
        for node in range(0, self.__nodes_number):
            failures = [neighbor for neighbor in
                        self.__nodes['neighbors'][node]
                        if self.__nodes['failure'][neighbor]]
            self.__nodes['neighbors'][node] = \
                list(set(self.__nodes['neighbors'][node]) - set(failures))
        # print self.__nodes['neighbors']

    def __communication(self):
        """
        Performs packets propagation in the network at the current simulation
        step.

        .. seealso:: :class:`sim2net._channel.Channel`
        """
        for node in range(0, self.__nodes_number):
            self.__nodes['channel'][node].transmit_packets(
                self.__nodes['neighbors'][node])
        for node in range(0, self.__nodes_number):
            while True:
                packet = self.__nodes['channel'][node].deliver_packet()
                if packet is None:
                    break
                for receiver in packet[-1]:
                    self.__nodes['channel'][receiver].capture_packet(
                        (packet[0], packet[1]))

    def __application(self):
        """
        Executes the simulation application at each operative node at the
        current simulation step.

        .. seealso:: :class:`sim2net.application`
        """
        for node in range(0, self.__nodes_number):
            if not self.__nodes['failure'][node]:
                self.__nodes['application'][node].main(
                    self.__current_time, self.__nodes['communication'][node],
                    self.__nodes['neighbors'][node], self.__network['shared'])

    def step(self):
        """
        Advances the simulation by one simulation step.  This method is called
        as many times as there is simulation steps by the
        :func:`sim2net.simulator.Sim2Net.run` method.

        This method calls: :func:`sim2net._network.Network._Network__failure`,
        :func:`sim2net._network.Network._Network__move`,
        :func:`sim2net._network.Network._Network__neighborhood`,
        :func:`sim2net._network.Network._Network__communication`,
        :func:`sim2net._network.Network._Network__application`, and
        :func:`sim2net._time.Time.tick` methods.
        """
        self.__failure()
        self.__move()
        self.__neighborhood()
        self.__communication()
        self.__application()
        self.__current_time = self.__network['time'].tick()

    def finalize(self):
        """
        Calls the :func:`sim2net.application.Application.finalize` finalization
        method at each node after all simulation steps.
        """
        for node in range(0, self.__nodes_number):
            self.__nodes['application'][node].finalize(
                self.__network['shared'])
