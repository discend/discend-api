"""
Elastic License 2.0

Copyright Clack and/or licensed to Clack under one
or more contributor license agreements. Licensed under the Elastic License;
you may not use this file except in compliance with the Elastic License.
"""
import os

from flask import request
from flask_limiter import Limiter, util

from .database import verify_token


def key_func():
    auth = request.headers.get('Authorization', None)

    try:
        user = verify_token(token=auth)
    except:
        return util.get_remote_address()
    else:
        return str(user.id)


limiter = Limiter(
    key_func=key_func,
    key_prefix='clack_brute',
    headers_enabled=True,
    strategy='fixed-window-elastic-expiry',
    storage_uri=os.getenv('STORAGE_URI'),
    default_limits=['50/second'],
)
