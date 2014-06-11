# -*- coding: utf-8 -*


# For bug reports, feature and support requests please visit
# <https://github.com/mkalewski/sim2net/issues>.

"""
sim2net -- simulation configuration file.

If in any doubt, refer to the technical documentations that is available on the
Internet:  <https://sim2net.readthedocs.org/en/latest/>.
"""


from sim2net.area.rectangle import Rectangle
from sim2net.area.square import Square
from sim2net.failure.crash import Crash
from sim2net.mobility.gauss_markov import GaussMarkov
from sim2net.mobility.nomadic_community import NomadicCommunity
from sim2net.mobility.random_direction import RandomDirection
from sim2net.mobility.random_waypoint import RandomWaypoint
from sim2net.packet_loss.gilbert_elliott import GilbertElliott
from sim2net.placement.grid import Grid as PlacementGrid
from sim2net.placement.normal import Normal as PlacementNormal
from sim2net.placement.uniform import Uniform as PlacementUniform
from sim2net.propagation.path_loss import PathLoss
from sim2net.speed.constant import Constant as SpeedConstant
from sim2net.speed.normal import Normal as SpeedNormal
from sim2net.speed.uniform import Uniform as SpeedUniform


## EDIT BELOW -----------------------------------------------------------------

## One of: 'critical', 'error', 'warning', 'info', or 'debug'
logger_level = 'warning'

## Simulation frequency:
simulation_frequency = 4

## Total simulation steps:
total_simulation_steps = 40

## Number of nodes:
nodes_number = 2

## area
area = [Square, {'side': 100.0}]
#area = [Rectangle, {'width':100.0, 'height': 100.0}]

## placement
placement = [PlacementGrid]
#placement = [PlacementNormal, {'standard_deviation': 0.2}]
#placement = [PlacementUniform]

## speed
speed = [SpeedConstant, {'speed': 1.0}]
#speed = [SpeedNormal, {'mean': 5.0, 'standard_deviation': 2.0}]
#speed = [SpeedUniform, {'minimal_speed': 0.0, 'maximal_speed': 5.0}]

## mobility
#mobility = [GaussMarkov, {'initial_speed': 1.5}]
#mobility = [NomadicCommunity, {'pause_time': 0.0, 'area_factor': 0.25}]
#mobility = [RandomDirection, {'pause_time': 0.0}]
mobility = [RandomWaypoint, {'pause_time': 0.0}]

## channel
propagation = [PathLoss]
packet_loss = [GilbertElliott, {'prhk': None}]
transmission_range = 50.0
maximum_transmission_time = 0.125

## failure
failure = [Crash, {'crash_probability': 0.1, 'maximum_crash_number': 0,
                   'transient_steps': 0}]
