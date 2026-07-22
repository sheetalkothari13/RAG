from __future__ import annotations

import os
import random
import time
import uuid

from uuid import SafeUUID

MAX = uuid.UUID("ffffffff-ffff-ffff-ffff-ffffffffffff")
NAMESPACE_DNS = uuid.NAMESPACE_DNS
NAMESPACE_OID = uuid.NAMESPACE_OID
NAMESPACE_URL = uuid.NAMESPACE_URL
NAMESPACE_X500 = uuid.NAMESPACE_X500
NIL = uuid.UUID("00000000-0000-0000-0000-000000000000")
RESERVED_FUTURE = uuid.RESERVED_FUTURE
RESERVED_MICROSOFT = uuid.RESERVED_MICROSOFT
RESERVED_NCS = uuid.RESERVED_NCS
RFC_4122 = uuid.RFC_4122
UUID = uuid.UUID
__version__ = "0.0.0-local"

_RANDOM = random.SystemRandom()


def _uuid4_int() -> int:
    return uuid.uuid4().int


def _uuid7_int(timestamp: int | None = None, nanos: int | None = None) -> int:
    if timestamp is None:
        unix_ns = time.time_ns()
    else:
        unix_ns = int(timestamp) * 1_000_000_000 + int(nanos or 0)

    unix_ms = unix_ns // 1_000_000
    unix_ms &= (1 << 48) - 1

    rand_a = _RANDOM.getrandbits(12)
    rand_b = _RANDOM.getrandbits(62)

    value = (unix_ms << 80) | (0x7 << 76) | (rand_a << 64) | (0x2 << 62) | rand_b
    return value


def reseed_rng() -> None:
    return None


def getnode() -> int:
    return uuid.getnode()


def uuid1(node: int | None = None, clock_seq: int | None = None) -> uuid.UUID:
    return uuid.uuid1(node=node, clock_seq=clock_seq)


def uuid3(namespace: uuid.UUID, name: str) -> uuid.UUID:
    return uuid.uuid3(namespace, name)


def uuid4() -> uuid.UUID:
    return uuid.UUID(int=_uuid4_int())


def uuid5(namespace: uuid.UUID, name: str) -> uuid.UUID:
    return uuid.uuid5(namespace, name)


def uuid6(node: int | None = None, timestamp: int | None = None) -> uuid.UUID:
    if timestamp is None:
        base = uuid.uuid1(node=node)
        timestamp_100ns = base.time
        clock_seq = base.clock_seq
        node = base.node
    else:
        timestamp_100ns = int(timestamp)
        clock_seq = _RANDOM.getrandbits(14)
        node = getnode() if node is None else node

    time_low = (timestamp_100ns >> 28) & 0xFFFFFFFF
    time_mid = (timestamp_100ns >> 12) & 0xFFFF
    time_hi = timestamp_100ns & 0x0FFF

    fields = (
        time_low,
        time_mid,
        time_hi | (6 << 12),
        (clock_seq >> 8) | 0x80,
        clock_seq & 0xFF,
        node,
    )
    return uuid.UUID(fields=fields)


def uuid7(timestamp: int | None = None, nanos: int | None = None) -> uuid.UUID:
    return uuid.UUID(int=_uuid7_int(timestamp=timestamp, nanos=nanos))


def uuid8(bytes: bytes) -> uuid.UUID:
    if len(bytes) != 16:
        raise ValueError("uuid8 requires exactly 16 bytes")
    data = bytearray(bytes)
    data[6] = (data[6] & 0x0F) | 0x80
    data[8] = (data[8] & 0x3F) | 0x80
    return uuid.UUID(bytes=bytes(data))


if hasattr(os, "fork"):
    os.register_at_fork(after_in_child=reseed_rng)
