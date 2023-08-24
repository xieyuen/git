import hashlib


def sha256(data, *, encode='utf-8'):
    return hashlib.sha256(data.encode(encode)).hexdigest()


def md5(data, *, encode='utf-8'):
    return hashlib.md5(data.encode(encode)).hexdigest()


def sha512(data, *, encode='utf-8'):
    return hashlib.sha512(data.encode(encode)).hexdigest()


def sha384(data, *, encode='utf-8'):
    return hashlib.sha384(data.encode(encode)).hexdigest()


def sha1(data, *, encode='utf-8'):
    return hashlib.sha1(data.encode(encode)).hexdigest()


def sha224(data, *, encode='utf-8'):
    return hashlib.sha224(data.encode(encode)).hexdigest()
