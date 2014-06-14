==================================
Simple Network Simulator (sim2net)
==================================

:Author:  Michał Kalewski
:Version: 3.1.2
:Documentation: http://sim2net.readthedocs.org/en/latest/
:License: MIT License

**Simple Network Simulator**  (**sim2net**) is a discrete event simulator of
*mobile ad hoc networks* (MANETs) implemented in Python.  The simulator allows
us to simulate networks of a given number of nodes that move according to the
selected mobility model, run custom applications, and communicate only by
sending application messages through wireless links.

Installation
============
There are two possibilities to install the **sim2net** simulator: with the use
of the ``pip`` installation tool, or from the source code obtained from `GitHub
<https://github.com/mkalewski/sim2net>`_.

1. Using the ``pip`` installation tool
--------------------------------------
.. code-block:: bash

   $ sudo pip install sim2net

2. Manually from the source code
--------------------------------
Step 1.  Clone the project:

.. code-block:: bash

    $ git clone git@github.com:mkalewski/sim2net.git sim2net
    $ cd sim2net

Step 2.  Run install:

.. code-block:: bash

    $ sudo python setup.py install

"Hello World" example
=====================
.. code-block:: bash

    $ sim2net -i .
    $ sim2net ./configuration.py ./application.py


**The full documentation can be found on**
`readthedocs.org <https://sim2net.readthedocs.org/en/latest/>`_.

Copyright
=========
| Copyright (c) 2012-2014  Michal Kalewski  <mkalewski at cs.put.poznan.pl>
|
| This program comes with ABSOLUTELY NO WARRANTY.
| THIS IS FREE SOFTWARE, AND YOU ARE WELCOME TO REDISTRIBUTE IT UNDER THE TERMS
| AND CONDITIONS OF THE MIT LICENSE.  YOU SHOULD HAVE RECEIVED A COPY OF THE
| LICENSE ALONG WITH THIS SOFTWARE; IF NOT, YOU CAN DOWNLOAD A COPY FROM
| HTTP://WWW.OPENSOURCE.ORG.
