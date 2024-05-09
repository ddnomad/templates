"""."""
import attrs
import beartype.typing
import structlog

import general_purpose_project.config
import general_purpose_project.utils.logging


@attrs.define(kw_only=True, repr=True)
class CliContext:
    """."""

    config: beartype.typing.Optional[general_purpose_project.config.Config] = None
    log_level: beartype.typing.Optional[general_purpose_project.utils.logging.LogLevel] = None
    logger: beartype.typing.Optional[structlog.BoundLogger] = None
    start_time: beartype.typing.Optional[float] = None
