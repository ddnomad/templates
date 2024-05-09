"""."""
import beartype
import click
import click_help_colors

import general_purpose_project.config


@click.command(
    cls=click_help_colors.HelpColorsCommand,
    help_options_color=general_purpose_project.config.CLI_CONFIG.option_colour,
)
@click.pass_context
# NOTE: It is necessary to explicitly enable beartype for click decorated functions, because _reasons_ (most probably,
# beartype.claw.beartype_this_package() decorates everything at the very top, where all arguments that actually get to
# cli() below are obscured).
@beartype.beartype  # pyright: ignore[reportUnknownMemberType]
def help(context: click.Context):  # noqa: A001
    """Show this help message and exit."""
    if context.parent is None:
        raise RuntimeError('Unexpected state: Click context does not have a parent')

    click.echo(context.parent.get_help())

