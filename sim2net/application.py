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
"""


from abc import ABCMeta, abstractmethod


__docformat__ = 'reStructuredText'


#pylint: disable=R0921
class Application(object):
    """
    """

    __metaclass__ = ABCMeta

    def initialize(self, node_id, shared):
        """
        """
        pass

    def finalize(self, shared):
        """
        """
        pass

    def failure(self, time, shared):
        """
        """
        pass

    def main(self, time, communication, neighbors, shared):
        """
        """
        pass
