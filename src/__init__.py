"""Dishwasher bot module."""

from enum import Enum


class Action(Enum):
    """Possible actions to do with a dishwasher."""

    START = 'start'
    RESET = 'reset'


class Dishwasher(Enum):
    """Known dishwashers."""

    ASTERIX = 'asterix'
    OBELIX = 'obelix'
    IDEFIX = 'idefix'
    MIRACULIX = 'miraculix'
    TICK = 'tick'
    TRICK = 'trick'
    TRACK = 'track'
    DONALD = 'donald'
