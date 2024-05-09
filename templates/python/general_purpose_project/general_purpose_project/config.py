"""."""
from __future__ import annotations

import ipaddress

import attrs
import beartype.typing
import cattrs

import general_purpose_project.utils.logging

# NOTE: Mostly future proofing
CONVERTER = cattrs.Converter()
CONVERTER.register_structure_hook(ipaddress.IPv4Address | ipaddress.IPv6Address, lambda v, _: ipaddress.ip_address(v))
CONVERTER.register_unstructure_hook(ipaddress.IPv4Address | ipaddress.IPv6Address, lambda v: str(v))


@attrs.define(kw_only=True, repr=True)
class Config:
    """."""

    cli: CLIConfig = attrs.field(factory=lambda: CLIConfig())

    @classmethod
    def structure(cls, d: dict[str, beartype.typing.Any]) -> Config:
        """."""
        return CONVERTER.structure(d, cls)

    def unstructure(self):
        """."""
        return CONVERTER.unstructure(self)


@attrs.define(kw_only=True, repr=True)
class CLIConfig:
    """."""

    development_mode: bool = False
    env_var_prefix: str = 'GENERAL_PURPOSE_PROJECT'
    header_colour: str = 'cyan'
    log_level: general_purpose_project.utils.logging.LogLevel = general_purpose_project.utils.logging.LogLevel.DISABLED
    max_content_width: int = 120
    option_colour: str = 'green'
    timestamp_format: str = '%Y-%m-%d %H:%M:%S %z'


def create_config():
    """."""
    # TODO(ddnomad): Support creation from a TOML config file
    return Config()


# TODO(ddnomad): Allow to specify CLI config via TOML configuration file
CLI_CONFIG = CLIConfig()
