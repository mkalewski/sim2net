#!/usr/bin/env python
# -*- coding: utf-8 -*-


# For bug reports, feature and support requests please visit
# <https://github.com/mkalewski/sim2net/issues>.

"""
sim2net -- simulation application file.

If in any doubt, refer to the technical documentations that is available on the
Internet:  <https://sim2net.readthedocs.org/en/latest/>.
"""


from sim2net.application import Application


class HelloWorld(Application):
    """
    A "Hello World" example with two nodes: the node with ID equal 0 sends a
    message that should be received and printed by the node with ID equal to 1.
    (See also the ``configuration.py`` file.)

    For more information about the methods that follows refer to the technical
    documentation:
    """

    def initialize(self, node_id, shared):
        """
        Initialization method.
        """
        self.__node_id = node_id
        print '[node %d] initialize' % self.__node_id

    def finalize(self, shared):
        """
        Finalization method.
        """
        print '[node %d] finalize' % self.__node_id

    def failure(self, time, shared):
        """
        This method is called only if the node crashes.
        """
        print ('[node %d] failure @ (%d, %2f)'
               % (self.__node_id, time[0], time[1]))

    def main(self, time, communication, neighbors, shared):
        """
        This method is called at each simulation step.
        """
        if self.__node_id == 0 and time[0] == 1:
            communication.send('Hello World!')
        while True:
            msg = communication.receive()
            if msg is None:
                break
            print ('[node %d] message from node %d: "%s"'
                   % (self.__node_id, msg[0], msg[1]))
