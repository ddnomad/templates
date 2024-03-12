"""."""
__version__ = '0.1.0'
__author__ = 'ddnomad <self@ddnomad.net>'

import warnings

import beartype.claw
import beartype.roar

beartype.claw.beartype_this_package()

warnings.filterwarnings('ignore', category=beartype.roar.BeartypeClawDecorWarning)
