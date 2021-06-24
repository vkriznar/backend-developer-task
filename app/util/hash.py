import hashlib
import os
from typing import NamedTuple
from hmac import compare_digest

ITERATION_COUNT = 200000


class SaltHash(NamedTuple):
    salt: str
    hash: str


def sha256(in_str: str) -> str:
    sha = hashlib.sha256()
    sha.update(in_str.encode())
    return sha.hexdigest()


def get_password_hash(password: str) -> SaltHash:
    """
    Hash the provided password with a randomly-generated salt and return the
    salt and hash (hexadecimal strings) to store in the database.
    """
    salt = os.urandom(16)
    pw_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATION_COUNT)
    return SaltHash(salt=salt.hex(), hash=pw_hash.hex())


def is_valid_password(salt: str, password_hash: str, password: str) -> bool:
    """
    Given a previously-stored salt and hash (hexadecimal strings), and a password provided by a user
    trying to log in, check whether the password is correct.
    """
    pw_hash_bytes = bytes.fromhex(password_hash)
    salt_bytes = bytes.fromhex(salt)
    return compare_digest(
        pw_hash_bytes,
        hashlib.pbkdf2_hmac("sha256", password.encode(), salt_bytes, ITERATION_COUNT)
    )
