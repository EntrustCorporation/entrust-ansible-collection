#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c), Entrust Corporation, 2023
# Author: Sapna Jain, Entrust
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

CRYPTOGRAPHY_IMP_ERR = None
try:
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend as cryptography_backend
except ImportError:
    CRYPTOGRAPHY_IMP_ERR = traceback.format_exc()


def load_certificate(path, content=None, backend='cryptography', der_support_enabled=False):
    """Load the specified certificate."""

    try:
        if content is None:
            with open(path, 'rb') as cert_fh:
                cert_content = cert_fh.read()
        else:
            cert_content = content
    except (IOError, OSError) as exc:
        pass
    if backend == 'cryptography':
        if der_support_enabled is False:
            try:
                return x509.load_pem_x509_certificate(cert_content, cryptography_backend())
            except ValueError as exc:
                pass
        elif der_support_enabled:
            try:
                return x509.load_der_x509_certificate(cert_content, cryptography_backend())
            except ValueError as exc:
                pass
