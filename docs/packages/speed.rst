.. (c) 2012-2014 Michal Kalewski  <mkalewski at cs.put.poznan.pl>
   This file is a part of the Simple Network Simulator (sim2net) project.  USE,
   MODIFICATION, COPYING AND DISTRIBUTION OF THIS SOFTWARE IS SUBJECT TO THE
   TERMS AND CONDITIONS OF THE MIT LICENSE.  YOU SHOULD HAVE RECEIVED A COPY OF
   THE MIT LICENSE ALONG WITH THIS SOFTWARE; IF NOT, YOU CAN DOWNLOAD A COPY
   FROM HTTP://WWW.OPENSOURCE.ORG/.

.. _sim2net-code-documentation-mobility-speed:

Package :mod:`sim2net.speed`
============================
.. automodule:: sim2net.speed
    :synopsis: This package contains modules that implement speed models.
.. contents:: Package modules:
    :local:
.. seealso:: :mod:`sim2net.placement`, :mod:`sim2net._time`

Module :mod:`sim2net.speed._speed`
----------------------------------
.. automodule:: sim2net.speed._speed
    :members:
    :private-members:
    :show-inheritance:
    :synopsis: This module provides an abstract class that should be
               implemented by all speed model classes.

Module :mod:`sim2net.speed.constant`
------------------------------------
.. automodule:: sim2net.speed.constant
    :members:
    :private-members:
    :show-inheritance:
    :synopsis: This module provides an implementation a constant node speed.

Module :mod:`sim2net.speed.normal`
----------------------------------
.. automodule:: sim2net.speed.normal
    :members:
    :private-members:
    :show-inheritance:
    :synopsis: This module provides an implementation of the normal speed
               distribution.

Module :mod:`sim2net.speed.uniform`
-----------------------------------
.. automodule:: sim2net.speed.uniform
    :members:
    :private-members:
    :show-inheritance:
    :synopsis: This module provides an implementation of the uniform speed
               distribution.
