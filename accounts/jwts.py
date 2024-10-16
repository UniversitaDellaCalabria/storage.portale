import json

from cryptojwt.jwk.rsa import import_private_rsa_key_from_file, RSAKey
from cryptojwt.jwe.jwe import factory
from cryptojwt.jwe.jwe_rsa import JWE_RSA

from . settings import (
    JWE_ALG,
    JWE_ENC,
    JWE_RSA_KEY_PATH,
)


RSA_KEY = JWE_RSA_KEY_PATH
JWE_ALG = JWE_ALG
JWE_ENC = JWE_ENC


def encrypt_to_jwe(content):
    """Returns a string
    a serialized encryption from cryptojwt.jwe.jwe_rsa.JWE_RSA
    """
    if isinstance(content, dict):
        content = json.dumps(content).encode()
    elif isinstance(content, str):
        content = content.encode()

    if not isinstance(content, bytes):
        raise Exception("encrypt_to_jwe content must be a bytes object")

    priv_key = import_private_rsa_key_from_file(RSA_KEY)
    pub_key = priv_key.public_key()
    _rsa = JWE_RSA(content, alg=JWE_ALG, enc=JWE_ENC)
    jwe = _rsa.encrypt(pub_key)
    return jwe


def decrypt_from_jwe(jwe):
    priv_key = import_private_rsa_key_from_file(RSA_KEY)
    _decryptor = factory(jwe, alg=JWE_ALG, enc=JWE_ENC)
    _dkey = RSAKey(priv_key=priv_key)
    msg = _decryptor.decrypt(jwe, [_dkey])
    return msg
