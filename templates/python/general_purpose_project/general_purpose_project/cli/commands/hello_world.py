"""."""
import beartype
import click
import click_help_colors

import general_purpose_project.config


@click.group(
    cls=click_help_colors.HelpColorsGroup,
    context_settings={
        'help_option_names': ('-h', '--help'),
        'max_content_width': general_purpose_project.config.CLI_CONFIG.max_content_width,
    },
    help_headers_color=general_purpose_project.config.CLI_CONFIG.header_colour,
    help_options_color=general_purpose_project.config.CLI_CONFIG.option_colour,
)
@click.pass_context
# # NOTE: It is necessary to explicitly enable beartype for click decorated functions, because _reasons_ (most probably,
# # beartype.claw.beartype_this_package() decorates everything at the very top, where all arguments that actually get to
# # cli() below are obscured).
@beartype.beartype  # pyright: ignore[reportUnknownMemberType]
def hello_world(context: click.Context):
    """Hello world command."""
    print('Hello, world!')
