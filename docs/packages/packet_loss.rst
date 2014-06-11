.. (c) 2012-2014 Michal Kalewski  <mkalewski at cs.put.poznan.pl>
   This file is a part of the Simple Network Simulator (sim2net) project.  USE,
   MODIFICATION, COPYING AND DISTRIBUTION OF THIS SOFTWARE IS SUBJECT TO THE
   TERMS AND CONDITIONS OF THE MIT LICENSE.  YOU SHOULD HAVE RECEIVED A COPY OF
   THE MIT LICENSE ALONG WITH THIS SOFTWARE; IF NOT, YOU CAN DOWNLOAD A COPY
   FROM HTTP://WWW.OPENSOURCE.ORG/.

.. _sim2net-code-documentation-packet_loss:

Package :mod:`sim2net.packet_loss`
==================================
.. automodule:: sim2net.packet_loss
    :synopsis: This package contains modules that implement packet loss models.
.. contents:: Package modules:
    :local:
.. seealso:: :mod:`sim2net.propagation`

Module :mod:`sim2net.packet_loss._packet_loss`
----------------------------------------------
.. automodule:: sim2net.packet_loss._packet_loss
    :members:
    :private-members:
    :show-inheritance:
    :synopsis: This module provides an abstract class that should be
               implemented by all packet loss model classes.

Module :mod:`sim2net.packet_loss.gilbert_elliott`
-------------------------------------------------
.. automodule:: sim2net.packet_loss.gilbert_elliott
   :members:
   :private-members:
   :show-inheritance:
   :synopsis: This module provides an implementation of the Gilbert-Elliott
              packet loss model.
