"""."""
import enum
import logging
import pathlib
import sys

import beartype.typing
import structlog


class LogLevel(enum.Enum):
    """."""

    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'
    DISABLED = 'DISABLED'


# NOTE: PyLance is having a meltdown if this function is annotated with an actual type it returns, which is
# `structlog._config.BoundLoggerLazyProxy`, while beartype will die with a current return annotation, so it
# is disabled for this function specifically.
@beartype.typing.no_type_check
def configure_logging(  # noqa: PLR0913
    level: LogLevel,
    print_test_log_messages: bool = False,
    log_file: beartype.typing.Optional[pathlib.Path] = None,
    log_file_level: beartype.typing.Optional[LogLevel] = None,
    logger_name: str = f'{__package__}.{__name__}',
    timestamp_format: str = '%Y-%m-%dT%H:%M:%SZ',
) -> structlog.stdlib.BoundLogger:
    """Configure unified Python's logging and structlog logging.

    This mostly follows a set up guide from Structlog's documentation, so excuse the madness:
    https://www.structlog.org/en/stable/standard-library.html#rendering-using-structlog-based-formatters-within-logging
    """
    shared_processors = [  # pyright: ignore[reportUnknownVariableType]
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt=timestamp_format, utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            },
        ),
    ]

    structlog.configure(
        cache_logger_on_first_use=True,
        logger_factory=structlog.stdlib.LoggerFactory(),
        processors=[*shared_processors, structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
    )

    if sys.stderr.isatty():
        formatter_processors = [structlog.dev.ConsoleRenderer()]
    else:
        formatter_processors = [structlog.processors.dict_tracebacks, structlog.processors.JSONRenderer()]  # pyright: ignore[reportUnknownVariableType]

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[structlog.stdlib.ProcessorFormatter.remove_processors_meta, *formatter_processors],
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(stream_handler)

    # TODO(ddnomad): Support logging to a file
    if log_file is not None:
        log_file_level = level if log_file_level is None else log_file_level
        raise NotImplementedError('Logging to a file is not yet supported')

    match level:
        case LogLevel.DISABLED:
            root_logger.setLevel(LogLevel.CRITICAL.value)
            logging.disable(logging.CRITICAL)
        case _:
            root_logger.setLevel(level.value)

    if print_test_log_messages is True:
        gen_test_log_messages(use_structlog=True)
        gen_test_log_messages(use_structlog=False)

    return structlog.stdlib.get_logger(logger_name)


def gen_test_log_messages(use_structlog: bool = False, logger_name: str = 'test'):
    """."""
    if use_structlog:
        logger = structlog.get_logger(logger_name)

        logger.debug('Structlog debug message', foo='bar', baz=42)
        logger.info('Structlog info message', foo='bar', baz=42)
        logger.warning('Structlog warning message', foo='bar', baz=42)
        logger.error('Structlog error message', foo='bar', baz=42)
        logger.critical('Structlog critical message', foo='bar', baz=42)

        return

    logger = logging.getLogger(logger_name)

    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')
