from __future__ import annotations

import uuid

import uuid_utils

NIL = uuid_utils.NIL
MAX = uuid_utils.MAX

__version__ = uuid_utils.__version__


def _from_int(value: int) -> uuid.UUID:
    return uuid.UUID(int=value)


def uuid1(node=None, clock_seq=None):
    return _from_int(uuid_utils.uuid1(node, clock_seq).int)


def uuid3(namespace, name):
    namespace = uuid_utils.UUID(namespace.hex) if namespace else namespace
    return _from_int(uuid_utils.uuid3(namespace, name).int)


def uuid4():
    return _from_int(uuid_utils._uuid4_int())


def uuid5(namespace, name):
    namespace = uuid_utils.UUID(namespace.hex) if namespace else namespace
    return _from_int(uuid_utils.uuid5(namespace, name).int)


def uuid6(node=None, timestamp=None):
    return _from_int(uuid_utils.uuid6(node, timestamp).int)


def uuid7(timestamp=None, nanos=None):
    return _from_int(uuid_utils._uuid7_int(timestamp, nanos))


def uuid8(bytes):
    return _from_int(uuid_utils.uuid8(bytes).int)
