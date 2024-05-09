"""."""
import logging
import platform
import time

import beartype
import beartype.typing
import click
import click_help_colors
import dotenv

import general_purpose_project.cli.context
import general_purpose_project.config
import general_purpose_project.utils.logging

VERSION_MESSAGE = f"""
General Purpose Python Project v{general_purpose_project.__version__}

Compat details:
+ Package version: v{general_purpose_project.__version__}
+ Python version:  v{platform.python_version()}
"""


@click.group(
    cls=click_help_colors.HelpColorsGroup,
    context_settings={
        'help_option_names': ('-h', '--help'),
        'max_content_width': general_purpose_project.config.CLI_CONFIG.max_content_width,
    },
    help_headers_color=general_purpose_project.config.CLI_CONFIG.header_colour,
    help_options_color=general_purpose_project.config.CLI_CONFIG.option_colour,
    invoke_without_command=True,
)
@click.option(
    '-l',
    '--log-level',
    help='Application log level.',
    default=general_purpose_project.config.CLI_CONFIG.log_level.value,
    metavar='LEVEL',
    show_default=True,
    type=click.Choice([level.value for level in general_purpose_project.utils.logging.LogLevel]),
)
@click.option(
    '--development-mode',
    help='Enable development mode.',
    hidden=True,
    is_flag=True,
)
@click.option(
    '--force-pretty-logs',
    help='Force pretty log output formatting even if TTY is not detected.',
    is_flag=True,
)
@click.option('-v', '-V', '--version', help='Print application version and exit.', is_flag=True)
@click.pass_context
# # NOTE: It is necessary to explicitly enable beartype for click decorated functions, because _reasons_ (most probably,
# # beartype.claw.beartype_this_package() decorates everything at the very top, where all arguments that actually get to
# # cli() below are obscured).
@beartype.beartype  # pyright: ignore[reportUnknownMemberType]
def cli(
    context: click.Context,
    log_level: str,
    development_mode: bool,
    force_pretty_logs: bool,
    version: bool,
):
    """General purpose Python project."""
    if version:
        click.echo(VERSION_MESSAGE)
        context.exit(0)

    if context.invoked_subcommand is None:
        click.echo(context.get_help())
        context.exit(0)

    config = general_purpose_project.config.create_config()

    config.cli.development_mode = development_mode
    config.cli.log_level = general_purpose_project.utils.logging.LogLevel(log_level)

    logger = general_purpose_project.utils.logging.configure_logging(  # pyright: ignore[reportUnknownMemberType]
        config.cli.log_level,
        force_pretty_renderer=force_pretty_logs,
        log_callsite_parameters=development_mode,
        timestamp_format=config.cli.timestamp_format,
        print_test_log_messages=True,  # NOTE: Remove me?
    )

    context.ensure_object(general_purpose_project.cli.context.CliContext)

    context.obj.config = config
    context.obj.log_level = log_level
    context.obj.start_time = time.time()


def run_cli():
    """."""
    # NOTE: Local imports here are required due to some Click magic shenanigans
    import general_purpose_project.cli.commands
    import general_purpose_project.cli.context
    import general_purpose_project.config

    enabled_commands = [  # pyright: ignore[reportUnknownVariableType]
        general_purpose_project.cli.commands.hello_world,
        general_purpose_project.cli.commands.help,
    ]

    for command in enabled_commands:  # pyright: ignore[reportUnknownVariableType]
        if isinstance(command, click.core.Group):
            command.add_command(general_purpose_project.cli.commands.help)

        cli.add_command(command)

    dotenv.load_dotenv()
    cli(
        auto_envvar_prefix=general_purpose_project.config.CLI_CONFIG.env_var_prefix,
        obj=general_purpose_project.cli.context.CliContext(),
    )
