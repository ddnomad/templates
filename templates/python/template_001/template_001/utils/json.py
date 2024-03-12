"""."""
import datetime
import enum
import ipaddress
import json
import uuid

import beartype.typing


class JSONEncoder(json.JSONEncoder):
    """A better version of a JSON encoder.

    This class is an extension of a builtin :class:`json.JSONEncoder` that supports additional data types.

    Currently, the differences are:

    1. :class:`datetime.datetime` instances are encoded as a unix timestamp float, unless `datetime_as_iso8601` is set
       to `True`.
    2. :class:`uuid.UUID` instances are encoded as hexadecimal strings.
    3. :class:`enum.Enum` instances are encoded as strings.
    4. :class:`ipaddress.IPv4Address` and :class:`ipaddress.IPv6Address` instances are encoded as strings.
    """

    def __init__(  # noqa: PLR0913
        self,
        *,
        skipkeys: bool = False,
        ensure_ascii: bool = True,
        check_circular: bool = True,
        allow_nan: bool = True,
        sort_keys: bool = False,
        indent: beartype.typing.Optional[int] = None,
        separators: beartype.typing.Optional[tuple[str, str]] = None,
        default: beartype.typing.Optional[beartype.typing.Callable[[beartype.typing.Any], str]] = None,
        datetime_as_iso8601: bool = False,
    ):
        """Instantiate the encoder.

        See :class:`json.JSONEncoder` original documentation for more details on what each keyword argument does.
        """
        super().__init__(
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            sort_keys=sort_keys,
            indent=indent,
            separators=separators,
            default=default,
        )

        self.datetime_as_iso8601 = datetime_as_iso8601

    def default(self, o: beartype.typing.Any) -> beartype.typing.Union[float, int, str]:
        """Encode a native object instance.

        :param o: Object instance to encode.

        :return: Encoded object instance.
        """
        if isinstance(o, datetime.datetime):
            return o.isoformat() if self.datetime_as_iso8601 else o.timestamp()

        if isinstance(o, uuid.UUID):
            return o.hex

        if isinstance(o, enum.Enum):
            return o.value

        if isinstance(o, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
            return str(o)

        return json.JSONEncoder.default(self, o)


class ISO8601JSONEncoder(JSONEncoder):
    """."""

    def __init__(self, *args: tuple[beartype.typing.Any], **kwargs: dict[str, beartype.typing.Any]):
        """."""
        super().__init__(*args, **kwargs, datetime_as_iso8601=True)
