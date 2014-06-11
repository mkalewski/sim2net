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
Provides an implementation of bidirectional communication channels for nodes in
the simulated network.

The channels transmit *packets* that transport application *messages* between
*neighboring* nodes.  Each packet has its own identifier that is unique under
the same sender, and can be received only by these nodes that are neighbors of
the sender for the duration of the packet transmission according to the
wireless signal propagation model used (see: :mod:`sim2net.propagation`).
Potential packet losses are determined on the basis of the given model (see:
:mod:`sim2net.packet_loss`), and transmission time of each packet is uniformly
randomized in range :math:`(0, t_{max}]`, where :math:`t_{max}` is the given
maximum transmission time in the *simulation time* units (see:
:mod:`sim2net._time`).
"""


from sim2net.utility import logger
from sim2net.utility.randomness import get_random_generator
from sim2net.utility.validation import check_argument_type


__docformat__ = 'reStructuredText'


class _Output(object):
    """
    This class implements output channels for nodes in the simulated network.

    .. note::

        Methods :meth:`transmit_packets` and :meth:`deliver_packet` are
        responsible for the transmission and delivery of packages, so it is
        presumed that these methods are called at each step of the simulation.
    """

    def __init__(self, time, packet_loss, node_id, maximum_transmission_time):
        """
        *Parameters*:
            - **time**: a simulation time object of the
              :class:`sim2net._time.Time` class;
            - **packet_loss**: an object representing a packet loss model to
              use (see :mod:`sim2net.packet_loss`);
            - **node_id** (`int`): an identifier of the node for which the
              output channel is created;
            - **maximum_transmission_time** (`float`): maximum message
              transmission time between neighboring nodes in the *simulation
              time* units (see: :mod:`sim2net._time`).
        """
        self.__logger = logger.get_logger('channel.output')
        assert self.__logger is not None, \
            'A logger object expected but "None" value got!'
        self.__random_generator = get_random_generator()
        assert self.__random_generator is not None, \
            'A random generator object expected but "None" value got!'
        super(_Output, self).__init__(node_id)
        self.__time = time
        self.__packet_loss = packet_loss
        self.__node_id = node_id
        self.__packet_counter = int(-1)
        self.__maximum_transmission_time = maximum_transmission_time
        self.__next_transmission_time = float(-1.0)
        # [ transmission start time,  transmission end time,
        #   message identifier,  (sending node identifier, message),
        #   [ list of neighboring nodes ] ]
        self.__transmitted_packets = list()

    def __get_transmission_neighbors(self, packet_id, transmission_time,
                                     neighbors):
        """
        Returns a list of neighboring nodes at the beginning of packet
        transmission.

        *Parameters*:
            - **packet_id** (`int`): an identifier of the transmitted packet;
            - **transmission_time** (`float`): scheduled start time of the
              transmission;
            - **neighbors** (`list`): a list of identifiers of all neighboring
              nodes of the sender at the current simulation step.

        *Returns*:
            (`list`) a list of identifiers of neighboring nodes of the sender
            for the given packet transmission or `None` value if the
            transmission time has not yet begun.
        """
        if transmission_time \
                <= self.__time.simulation_time + self.__time.simulation_period:
            if self.__logger.isEnabledFor('DEBUG'):
                self.__logger.debug('Node #%d: transmitting packet %d'
                                    % (self.__node_id, packet_id))
            return neighbors
        return None

    def send_message(self, message, neighbors):
        """
        Sends an application message.

        *Parameters*:
            - **message**: the application message to send of any type;
            - **neighbors** (`list`): a list of identifiers of all neighboring
              nodes of the sender at the current simulation step.
        """
        assert isinstance(neighbors, list) or isinstance(neighbors, tuple), \
            'Node #%d: an invalid type of the given list of neighbors!' \
            % self.__node_id
        if not message:
            self.__logger.error('Node #%d: discarding the empty message'
                                ' passed to send!' % self.__node_id)
            return
        self.__packet_counter += 1
        while True:
            message_transmission_time = \
                self.__random_generator.uniform(
                    0.0, self.__maximum_transmission_time)
            if message_transmission_time > 0.0:
                break
        if self.__next_transmission_time < self.__time.simulation_time:
            self.__next_transmission_time = self.__time.simulation_time
        packet_neighbors = \
            self.__get_transmission_neighbors(self.__packet_counter,
                                              self.__next_transmission_time,
                                              neighbors)
        # [ transmission start time,  transmission end time,
        #   packet identifier,  (sending node identifier, message),
        #   [ list of neighboring nodes ] ]
        self.__transmitted_packets.append(
            [self.__next_transmission_time,
             self.__next_transmission_time + message_transmission_time,
             self.__packet_counter,
             (self.__node_id, message),
             packet_neighbors])
        self.__next_transmission_time += message_transmission_time
        # print self.__transmitted_packets

    def transmit_packets(self, neighbors):
        """
        Transmits packets to neighboring nodes.

        *Parameters*:
            - **neighbors** (`list`): a list of identifiers of all neighboring
              nodes of the sender at the current simulation step according to
              the wireless signal propagation model used (see:
              :mod:`sim2net.propagation`).
        """
        assert isinstance(neighbors, list) or isinstance(neighbors, tuple), \
            'Node #%d: an invalid type of the given list of neighbors!' \
            % self.__node_id
        neighbors_set = set(neighbors)
        for packet in self.__transmitted_packets:
            if packet[-1] is None:
                packet[-1] = \
                    self.__get_transmission_neighbors(packet[2], packet[0],
                                                      neighbors)
            if packet[0] <= self.__time.simulation_time \
                    and packet[1] >= self.__time.simulation_time:
                assert packet[-1] is not None, \
                    'Node #%d: the list of neighbors for packet %d is empty!' \
                    % (self.__node_id, packet[2])
                if packet[-1]:
                    packet[-1] = list(set(packet[-1]) & neighbors_set)
            # print packet

    def deliver_packet(self):
        """
        Delivers packets to neighboring nodes.

        *Returns*:
            `None` value if there is no packet to deliver at the current
            simulation step, or a `tuple` that contains the packet to deliver.
            In such a case, the tuple has the following data:

                * an identifier of the packet to deliver of type `int`;
                * a `tuple` that contains an identifier of the sender of
                  type `int` and the transported application message;
                * a list of identifiers of nodes which receive the packet.

        .. hint::

            * It is possible that at one simulation step there will be multiple
              packets to deliver, so this method should be called as long until
              it returns `None` value.

            * This method requires the use of complementary method
              :meth:`_Input.capture_packet` of input channels of all nodes
              receiving the packet.
        """
        for packet_no in range(0, len(self.__transmitted_packets)):
            packet = self.__transmitted_packets[0]
            if packet[1] > self.__time.simulation_time:
                return None
            losses = [neighbor for neighbor in packet[-1]
                      if self.__packet_loss.packet_loss()]
            packet[-1] = list(set(packet[-1]) - set(losses))
            if losses and self.__logger.isEnabledFor('DEBUG'):
                msg = 'Node #%d: in accordance with the packet loss model' \
                      ' packet %d was lost during transmission to node(s) #%s'
                self.__logger.debug(msg %
                                    (self.__node_id, packet[2],
                                     ', #'.join(str(node) for node in losses)))
            if not packet[-1]:
                if self.__logger.isEnabledFor('DEBUG'):
                    msg = 'Node #%d: no neighboring node is able to receive' \
                          ' packet %d'
                    self.__logger.debug(msg % (self.__node_id, packet[2]))
                del self.__transmitted_packets[0]
                continue
            packet_out = (packet[2], packet[3], packet[-1])
            del self.__transmitted_packets[0]
            return packet_out


class _Input(object):
    """
    This class implements input channels for nodes in the simulated network.
    """

    def __init__(self, node_id):
        """
        *Parameters*:
            - **node_id** (`int`): an identifier of the node for which the
              input channel is created.
        """
        self.__logger = logger.get_logger('channel.input')
        assert self.__logger is not None, \
            'A logger object expected but "None" value got!'
        self.__random_generator = get_random_generator()
        assert self.__random_generator is not None, \
            'A random generator object expected but "None" value got!'
        self.__node_id = node_id
        self.__captured_packets = list()

    def capture_packet(self, packet):
        """
        Captures packets transmitted by neighboring nodes.

        *Parameters*:
            - **packet** (`tuple`): a packet to capture represented by a tuple
              that contains the packet's identifier and transported application
              message, which is also a tuple containing an identifier of the
              sender and the message.
        """
        assert isinstance(packet, tuple) and len(packet) == 2, \
            'Invalid packet has been captured!'
        self.__captured_packets.append(packet[1])
        if self.__logger.isEnabledFor('DEBUG'):
            self.__logger.debug('Node #%s: packet %s from node %s has been'
                                ' received' % (self.__node_id, packet[0],
                                               packet[1][0]))

    def receive_message(self):
        """
        Returns a received application message.

        *Returns*:
            `None` value if there is no message at the current simulation step,
            or a `tuple` that contains an identifier of the sender and the
            received application message.
        """
        try:
            return self.__captured_packets.pop(0)
        except IndexError:
            return None


class Channel(_Output, _Input):
    """
    This class implements bidirectional communication channels for each node in
    the simulated network.

    The class has no members and inherits all its methods from two classes:
    :class:`_Input` and :class:`_Output`.

    Application message passing is implemented here as follows.  First, a
    message is sent locally by the :meth:`_Output.send_message` method.  Then,
    it is transmitted in a packet to neighboring nodes by the
    :meth:`_Output.transmit_packets` method.  If the transmission is
    successful, the packet leaves the output channel by calling the
    :meth:`_Output.deliver_packet` method and will be transferred to receiving
    nodes by calling the :meth:`_Input.capture_packet` methods.  Finally, the
    message can be received by the application by calling the
    :meth:`_Input.receive_message` method.
    """

    def __init__(self, time, packet_loss, node_id, maximum_transmission_time):
        """
        *Parameters*:
            - **time**: a simulation time object of the
              :class:`sim2net._time.Time` class;
            - **packet_loss**: an object representing the packet loss model
              (see :mod:`sim2net.packet_loss`);
            - **node_id** (`int`): an identifier of the node;
            - **maximum_transmission_time** (`float`): maximum message
              transmission time between neighboring nodes in the *simulation
              time* units (see: :mod:`sim2net._time`).

        *Raises*:
            - **ValueError**: raised when the given value of the *time* or
              *packet_loss* parameter is `None`; or when the given value of the
              *node_id* or *maximum_transmission_time* parameter is less than
              zero.
        """
        if time is None:
            raise ValueError('Parameter "time": a time abstraction object'
                             ' expected but "None" value given!')
        if packet_loss is None:
            raise ValueError('Parameter "packet_loss": an object'
                             ' representing a packet loss model expected'
                             ' but "None" value given!')
        self.__logger = logger.get_logger(Channel.__name__)
        assert self.__logger is not None, \
            'A logger object expected but "None" value got!'
        check_argument_type(Channel.__name__, 'node_id', int, node_id,
                            self.__logger)
        if node_id < 0:
            raise ValueError('Parameter "node_id": a value of the identifier'
                             ' cannot be less that zero but %d given!'
                             % int(node_id))
        check_argument_type(Channel.__name__, 'maximum_transmission_time',
                            float, maximum_transmission_time, self.__logger)
        if maximum_transmission_time < 0.0:
            raise ValueError('Parameter "maximum_transmission_time": a value'
                             ' of the maximum message transmission time'
                             ' cannot be less that zero but %f given!'
                             % float(maximum_transmission_time))
        super(Channel, self).__init__(time, packet_loss, node_id,
                                      maximum_transmission_time)
