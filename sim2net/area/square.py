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
Provides an implementation of a square simulation area in the two-dimensional
space.
"""


from sim2net.area.rectangle import Rectangle


__docformat__ = 'reStructuredText'


class Square(Rectangle):
    """
    This class implements a square simulation area of the given size in the
    two-dimensional space with the origin in (0, 0).
    """

    def __init__(self, side):
        """
        *Parameters*:
            - **side** (`float`): a side length of the square simulation area.

        .. note::

            In this case, the :meth:`sim2net.area.rectangle.Rectangle` method
            is called with the **width** and **height** parameters set to the
            value of the given **side** argument.
        """
        super(Square, self).__init__(side, side)

    def get_area(self):
        """
        Creates a dictionary that stores information about the simulation area.

        *Returns*:
            A dictionary that stores information about the simulation area;
            it has the following fields:

                - 'area name': a name of the simulation area of type `str`,
                - 'side': a side length of the square simulation area of type
                  `float`.
        """
        return {'area name': self.__class__.__name__.lower(),
                'side': self.width}
