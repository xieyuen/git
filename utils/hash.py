import hashlib


def md5(data: str | bytes, *, encode='utf-8', decode=None) -> str:
    if isinstance(data, bytes):
        if decode is None:
            return hashlib.md5(data).hexdigest()
        return hashlib.md5(
            data.decode(decode).encode(encode)
        ).hexdigest()
    return hashlib.md5(data.encode(encode)).hexdigest()


def sha256(data: str | bytes, *, encode='utf-8', decode=None) -> str:
    if isinstance(data, bytes):
        if decode is None:
            return hashlib.sha256(data).hexdigest()
        return hashlib.sha256(
            data.decode(decode).encode(encode)
        ).hexdigest()
    return hashlib.sha256(data.encode(encode)).hexdigest()


def sha512(data: str | bytes, *, encode='utf-8', decode=None) -> str:
    if isinstance(data, bytes):
        if decode is None:
            return hashlib.sha512(data).hexdigest()
        return hashlib.sha512(
            data.decode(decode).encode(encode)
        ).hexdigest()
    return hashlib.sha512(data.encode(encode)).hexdigest()


def sha384(data: str | bytes, *, encode='utf-8', decode=None) -> str:
    if isinstance(data, bytes):
        if decode is None:
            return hashlib.sha384(data).hexdigest()
        return hashlib.sha384(
            data.decode(decode).encode(encode)
        ).hexdigest()
    return hashlib.sha384(data.encode(encode)).hexdigest()


def sha1(data: str | bytes, *, encode='utf-8', decode=None) -> str:
    if isinstance(data, bytes):
        if decode is None:
            return hashlib.sha1(data).hexdigest()
        return hashlib.sha1(
            data.decode(decode).encode(encode)
        ).hexdigest()
    return hashlib.sha1(data.encode(encode)).hexdigest()


def sha224(data: str | bytes, *, encode='utf-8', decode=None) -> str:
    if isinstance(data, bytes):
        if decode is None:
            return hashlib.sha224(data).hexdigest()
        return hashlib.sha224(
            data.decode(decode).encode(encode)
        ).hexdigest()
    return hashlib.sha224(data.encode(encode)).hexdigest()


def sha3_224(data: str | bytes, *, encode='utf-8', decode=None) -> str:
    if isinstance(data, bytes):
        if decode is None:
            return hashlib.sha3_224(data).hexdigest()
        return hashlib.sha3_224(
            data.decode(decode).encode(encode)
        ).hexdigest()
    return hashlib.sha3_224(data.encode(encode)).hexdigest()


def sha3_256(data: str | bytes, *, encode='utf-8', decode=None) -> str:
    if isinstance(data, bytes):
        if decode is None:
            return hashlib.sha3_256(data).hexdigest()
        return hashlib.sha3_256(
            data.decode(decode).encode(encode)
        ).hexdigest()
    return hashlib.sha3_256(data.encode(encode)).hexdigest()


def sha3_384(data: str | bytes, *, encode='utf-8', decode=None) -> str:
    if isinstance(data, bytes):
        if decode is None:
            return hashlib.sha3_384(data).hexdigest()
        return hashlib.sha3_384(
            data.decode(decode).encode(encode)
        ).hexdigest()
    return hashlib.sha3_384(data.encode(encode)).hexdigest()


def sha3_512(data: str | bytes, *, encode='utf-8', decode=None) -> str:
    if isinstance(data, bytes):
        if decode is None:
            return hashlib.sha3_512(data).hexdigest()
        return hashlib.sha3_512(
            data.decode(decode).encode(encode)
        ).hexdigest()
    return hashlib.sha3_512(data.encode(encode)).hexdigest()


def blake2b(data: str | bytes, *, encode='utf-8', decode=None) -> str:
    if isinstance(data, bytes):
        if decode is None:
            return hashlib.blake2b(data).hexdigest()
        return hashlib.blake2b(
            data.decode(decode).encode(encode)
        ).hexdigest()
    return hashlib.blake2b(data.encode(encode)).hexdigest()


def blake2s(data: str | bytes, *, encode='utf-8', decode=None) -> str:
    if isinstance(data, bytes):
        if decode is None:
            return hashlib.blake2s(data).hexdigest()
        return hashlib.blake2s(
            data.decode(decode).encode(encode)
        ).hexdigest()
    return hashlib.blake2s(data.encode(encode)).hexdigest()


def shake128(data: str | bytes, length: int, *, encode='utf-8', decode=None) -> str:
    if isinstance(data, bytes):
        if decode is None:
            return hashlib.shake_128(data).hexdigest(length)
        return hashlib.shake_128(
            data.decode(decode).encode(encode)
        ).hexdigest(length)
    return hashlib.shake_128(data.encode(encode)).hexdigest(length)


def shake256(data: str | bytes, length, *, encode='utf-8', decode=None) -> str:
    if isinstance(data, bytes):
        if decode is None:
            return hashlib.shake_256(data).hexdigest(length)
        return hashlib.shake_256(
            data.decode(decode).encode(encode)
        ).hexdigest(length)
    return hashlib.shake_256(data.encode(encode)).hexdigest(length)
