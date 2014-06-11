.. (c) 2012-2014 Michal Kalewski  <mkalewski at cs.put.poznan.pl>
   This file is a part of the Simple Network Simulator (sim2net) project.  USE,
   MODIFICATION, COPYING AND DISTRIBUTION OF THIS SOFTWARE IS SUBJECT TO THE
   TERMS AND CONDITIONS OF THE MIT LICENSE.  YOU SHOULD HAVE RECEIVED A COPY OF
   THE MIT LICENSE ALONG WITH THIS SOFTWARE; IF NOT, YOU CAN DOWNLOAD A COPY
   FROM HTTP://WWW.OPENSOURCE.ORG/.

.. _sim2net-code-documentation-propagation:

Package :mod:`sim2net.propagation`
==================================
.. automodule:: sim2net.propagation
    :synopsis: This package contains modules that implement wireless signal
               propagation models.
.. contents:: Package modules:
    :local:
.. seealso:: :mod:`sim2net.packet_loss`

Module :mod:`sim2net.propagation._propagation`
----------------------------------------------
.. automodule:: sim2net.propagation._propagation
    :members:
    :private-members:
    :show-inheritance:
    :synopsis: This module provides an abstract class that should be
               implemented by all propagation model classes.

Module :mod:`sim2net.propagation.path_loss`
-------------------------------------------
.. automodule:: sim2net.propagation.path_loss
   :members:
   :private-members:
   :show-inheritance:
   :synopsis: This module provides an implementation of the simplified path
              loss propagation model.
