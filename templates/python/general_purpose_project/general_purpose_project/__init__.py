"""."""
import warnings

import beartype.claw
import beartype.roar

from .meta import AUTHOR, DESCRIPTION, LICENSE, PACKAGE_NAME, VERSION

__author__ = AUTHOR
__description__ = DESCRIPTION
__license__ = LICENSE
__package_name__ = PACKAGE_NAME
__version__ = VERSION

beartype.claw.beartype_this_package()

warnings.filterwarnings('ignore', category=beartype.roar.BeartypeClawDecorWarning)
