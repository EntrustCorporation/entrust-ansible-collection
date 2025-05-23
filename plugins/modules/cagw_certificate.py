#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c), Entrust Corporation, 2023
# Author: Sapna Jain, Entrust
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: cagw_certificate
author:
    - Sapna Jain (@sapnajainEntrust)
short_description: Request SSL/TLS certificates with the Certificate Authority Gateway (CAGW) API
description:
    - Create, get, and take actions (Hold, Unhold, Revoke certificates) with the Certificate Authority Gateway (CAGW) API.
    - Requires credentials for calling the CAGW API.
notes:
    - C(path) must be specified as the output location of the certificate.
requirements:
    - cryptography >= 1.6
    - Ansible Core >= 2.14.0
    - Minimum Python Version = 3.6
options:
    force:
        description:
            - If O(force=true) then a certificate is requested regardless of whether I(path) points to an existing valid certificate.
        type: bool
        default: False
    path:
        description:
            - The destination path for the generated certificate as a PEM encoded cert.
            - If there is already a certificate at this location and O(force=true) then it will be replaced always.
              but if I(force) is not specified then we get the certificate validity for existing certificate from Entrust CAGW.
              If C(cert_days < remaining_days) then only a new certificate will be obtained.
            - If O(enrollment_format=PKCS12) then it will have Base64 encoded PKCS12 body.
        type: path
    csr:
        description:
            - Base-64 encoded Certificate Signing Request (CSR). csr is accepted without PEM formatting around the Base-64 string.
            - If no csr is provided when O(request_type=new) and O(enrollment_format=X509),
              the certificate will not be generated and module will be failed.
        type: path

    cagw_api_client_cert_path:
        description:
            - Path for the Client cert issued by the same CA.
        type: path
        required: true

    cagw_api_client_cert_key_path:
        description:
            - Path for the Client cert key issued by the same CA.
        type: path
        required: true

    host:
        description:
            - Host or IP address for Entrust CAGW.
        type: str
        required: true

    port:
        description:
            - Port for Entrust CAGW.
        type: int
        default: 443

    certificate_authority_id:
        description:
            - Unique id for the Certificate Authority.
        type: str
        required: true

    certificate_profile_id:
        description:
            - Profile id for the Certificate Authority.
        type: str

    request_type:
        description:
            - Request type that is new (stands for enrollment), get (stands for get certificate),
              action (stands for action to be taken on the certificate).
        type: str
        choices: [ 'new', 'action', 'get' ]
        required: true

    enrollment_format:
        description:
            - enrollment_format that is X509 or PKCS12.
        type: str
        choices: [ 'X509', 'PKCS12' ]

    validate_certs:
        description:
            - If set to false then SSL validation with Server is skipped.
              This should be set to false only for testing purposes.
        type: bool
        default: True

    action_type:
        description:
            - What action has to be taken on the certificate that is RevokeAction, HoldAction, UnholdAction.
        type: str
        choices: [ 'RevokeAction', 'HoldAction', 'UnholdAction']

    action_reason:
        description:
            - Reason has to be given for the action.
        type: str

    serial_no:
        description:
            - Serial number of the already issued certificate.
        type: str

    p12_protection_password:
        description:
            - PKCS12 password for server side generation of the private key and CSR.
        type: str

    dn:
        description:
            - Distinguished name given for the enrollment.
        type: str

    validity_period:
        description:
            - The certificate validity period. An ISO 8601 date-time interval or duration indicating the
              C(not before) and/or C(not after) dates of the certificate.
            - Specify the start date and expiry date as follows
              C(2018-07-06T13:00Z/2019-07-06T09:00:00Z)
            - Specify the start date and a duration. Start on July 6, 2018 13:00Z with a lifetime of 1 year and 3 months.
              C(2018-07-06T13:00Z/P1Y3M0DT0H0M)
            - Specify the expiry date and a duration. Expire on December 31, 2018 with a lifetime of 3 months. B(Note) that the start date will be automatically calculated.
              C(P0Y3M0DT0H0M/2018-12-31T00:00Z)
            - Specify a duration only. A lifetime of 1 year, 3 months, 10 days, 0 hours and 0 minutes. B(Note) that the start date will always be the current date.
              C(P1Y3M10DT0H0M)
        type: str

    cagw_api_specification_path:
        description:
            - Path for CAGW api specification doc.
        type: path
        required: true

    remaining_days:
        description:
            - The number of days the certificate must have left being valid.
              If a certificate is already present at the I(path) and I(force) is not specified then
              we get the certificate validity for existing certificate from Entrust CAGW.
              If C(cert_days < remaining_days) then a new certificate will be obtained.
            - The O(force=true) option may be used to ensure that a new certificate is always obtained.
        type: int
        default: 30

    connector_name:
        description:
            - This parameter defines which CA type connected at the backend.
              Supported list of CAs include Entrust Certificate Solution(ECS), Entrust Security Manager(SM),
              Entrust PKIHUB CA(PKIaaS), Microsoft CA(MSCA).
            - If connector_name is not provided when O(request_type=new), module will be failed.
        type: str
        choices: [ 'SM', 'ECS', 'PKIaaS', 'MSCA' ]

    subject_alt_name:
        description:
            - The subject alternative name identifiers.
        type: dict
        suboptions:
            dNSName:
                description: DNS name of the target server.
                type: str
            iPAddress:
                description: IP address of the target server.
                type: str
            uniformResourceIdentifier:
                description:  URI of the target server.
                type: str
            directoryName:
                description: directoryName of the target server.
                type: str
            rfc822Name:
                description: rfc822 name of the target server.
                type: str

    tracking_info:
        description: Free form tracking information to attach to the record for the certificate.
        type: str
    requester_name:
        description:
            - The requester name to associate with certificate tracking information.
            - If requester_name is not provided when O(connector_name=ECS), module will be failed.
        type: str
    requester_email:
        description:
            -The requester email to associate with certificate tracking information and
             receive delivery and expiry notices for the certificate.
            - If requester_email is not provided when O(connector_name=ECS), module will be failed.
        type: str
    requester_phone:
        description: The requester phone number to associate with certificate tracking information.
        type: str
    additional_emails:
        description: A list of additional email addresses to receive the delivery notice and expiry notification for the certificate.
        type: list
        elements: str

    custom_fields:
        description:
            - Mapping of custom fields to associate with the certificate request and certificate.
            - Only supported if custom fields are enabled for your account.
            - Each custom field specified must be a custom field you have defined for your account.
        type: dict
        suboptions:
            text1:
                description: Custom text field (maximum 500 characters).
                type: str
            text2:
                description: Custom text field (maximum 500 characters).
                type: str
            text3:
                description: Custom text field (maximum 500 characters).
                type: str
            text4:
                description: Custom text field (maximum 500 characters).
                type: str
            text5:
                description: Custom text field (maximum 500 characters).
                type: str
            text6:
                description: Custom text field (maximum 500 characters).
                type: str
            text7:
                description: Custom text field (maximum 500 characters).
                type: str
            text8:
                description: Custom text field (maximum 500 characters).
                type: str
            text9:
                description: Custom text field (maximum 500 characters).
                type: str
            text10:
                description: Custom text field (maximum 500 characters).
                type: str
            text11:
                description: Custom text field (maximum 500 characters).
                type: str
            text12:
                description: Custom text field (maximum 500 characters).
                type: str
            text13:
                description: Custom text field (maximum 500 characters).
                type: str
            text14:
                description: Custom text field (maximum 500 characters).
                type: str
            text15:
                description: Custom text field (maximum 500 characters).
                type: str
            number1:
                description: Custom number field.
                type: float
            number2:
                description: Custom number field.
                type: float
            number3:
                description: Custom number field.
                type: float
            number4:
                description: Custom number field.
                type: float
            number5:
                description: Custom number field.
                type: float
            date1:
                description: Custom date field.
                type: str
            date2:
                description: Custom date field.
                type: str
            date3:
                description: Custom date field.
                type: str
            date4:
                description: Custom date field.
                type: str
            date5:
                description: Custom date field.
                type: str
            email1:
                description: Custom email field.
                type: str
            email2:
                type: str
                description: Custom email field.
            email3:
                description: Custom email field.
                type: str
            email4:
                description: Custom email field.
                type: str
            email5:
                description: Custom email field.
                type: str
            dropdown1:
                description: Custom dropdown field.
                type: str
            dropdown2:
                description: Custom dropdown field.
                type: str
            dropdown3:
                description: Custom dropdown field.
                type: str
            dropdown4:
                description: Custom dropdown field.
                type: str
            dropdown5:
                description: Custom dropdown field.
                type: str

seealso:
    - module: community.crypto.openssl_privatekey
      description: Can be used to create private keys (both for certificates and accounts).
    - module: community.crypto.openssl_csr
      description: Can be used to create a Certificate Signing Request (CSR).

'''

EXAMPLES = r'''
- name: Request a new certificate from SM via CAGW with bare minimum parameters.  Will request a new certificate
  entrust.crypto.cagw_certificate:
    path: /etc/ssl/crt/ansible.com.crt
    csr: /etc/ssl/csr/ansible.com.csr
    cagw_api_client_cert_path: /etc/ssl/entrust/cagw-client.crt
    cagw_api_client_cert_key_path: /etc/ssl/entrust/cagw-client.key
    certificate_authority_id: ca_id
    certificate_profile_id: profile_id
    request_type: new
    enrollment_format: X509
    connector_name: SM
    cagw_api_specification_path: /etc/ssl/entrust/cagw-api.yaml

- name: Request a new certificate from CAGW with subjectAltName parameters and server cert validation is false
  entrust.crypto.cagw_certificate:
    path: /etc/ssl/crt/ansible.com.crt
    csr: /etc/ssl/csr/ansible.com.csr
    cagw_api_client_cert_path: /etc/ssl/entrust/cagw-client.crt
    cagw_api_client_cert_key_path: /etc/ssl/entrust/cagw-client.key
    certificate_authority_id: ca_id
    certificate_profile_id: profile_id
    request_type: new
    enrollment_format: X509
    connector_name: SM
    cagw_api_specification_path: /etc/ssl/entrust/cagw-api.yaml
    validity_period: 2018-07-06T13:00Z/2019-07-06T09:00:00Z
    subject_alt_name:
      dNSName: server.example.com
      iPAddress: 192.168.1.1
      directoryName: cn=john doe,o=example inc,c=us
      uniformResourceIdentifier: http://example.com/
      rfc822Name: server.example.com
    validate_certs: false

- name: Get an already issued certificate from CAGW with valid serial num in hexadecimal format
  entrust.crypto.cagw_certificate:
    path: /etc/ssl/crt/ansible.com.crt
    cagw_api_client_cert_path: /etc/ssl/entrust/cagw-client.crt
    cagw_api_client_cert_key_path: /etc/ssl/entrust/cagw-client.key
    certificate_authority_id: ca_id
    request_type: get
    serial_no: 5b9ba13d
    cagw_api_specification_path: /etc/ssl/entrust/cagw-api.yaml

- name: Request a certificate from CAGW with enrollment format PKCS12
  entrust.crypto.cagw_certificate:
    path: /etc/ssl/crt/ansible.com.crt
    cagw_api_client_cert_path: /etc/ssl/entrust/cagw-client.crt
    cagw_api_client_cert_key_path: /etc/ssl/entrust/cagw-client.key
    certificate_authority_id: ca_id
    certificate_profile_id: profile_id
    request_type: new
    enrollment_format: PKCS12
    connector_name: SM
    p12_protection_password: 'Password@2023'
    dn: /C=CA/O=iotrust/CN=CA/CN=ans-test-101
    cagw_api_specification_path: /etc/ssl/entrust/cagw-api.yaml

- name: Request a new SSL certificate from ECS via CAGW with bare minimum parameters.  Will request a new certificate
  entrust.crypto.cagw_certificate:
    path: /etc/ssl/crt/ansible.com.crt
    csr: /etc/ssl/csr/ansible.com.csr
    cagw_api_client_cert_path: /etc/ssl/entrust/cagw-client.crt
    cagw_api_client_cert_key_path: /etc/ssl/entrust/cagw-client.key
    certificate_authority_id: ca_id
    certificate_profile_id: profile_id
    request_type: new
    enrollment_format: X509
    cagw_api_specification_path: /etc/ssl/entrust/cagw-api.yaml
    connector_name: ECS
    requester_name: John-Clark
    requester_email: john.clark@example.com

- name: Request a new SSL certificate from ECS via CAGW with optional custom_field parameters.  Will request a new certificate
  entrust.crypto.cagw_certificate:
    path: /etc/ssl/crt/ansible.com.crt
    csr: /etc/ssl/csr/ansible.com.csr
    cagw_api_client_cert_path: /etc/ssl/entrust/cagw-client.crt
    cagw_api_client_cert_key_path: /etc/ssl/entrust/cagw-client.key
    certificate_authority_id: ca_id
    certificate_profile_id: profile_id
    request_type: new
    enrollment_format: X509
    cagw_api_specification_path: /etc/ssl/entrust/cagw-api.yaml
    connector_name: ECS
    requester_name: John-Clark
    requester_email: john.clark@example.com
    custom_fields:
      text1: Admin
      text2: Invoice 25
      number1: 342
      date1: '2018-01-01'
      email1: sales@ansible.testcertificates.com
      dropdown1: red

- name: Take an action(HoldAction) on certificate already recieved from CAGW
  entrust.crypto.cagw_certificate:
    cagw_api_client_cert_path: /etc/ssl/entrust/cagw-client.crt
    cagw_api_client_cert_key_path: /etc/ssl/entrust/cagw-client.key
    certificate_authority_id: ca_id
    request_type: action
    action_type: HoldAction
    action_reason: unspecified
    serial_no: 5b9ba13d
    cagw_api_specification_path: /etc/ssl/entrust/cagw-api.yaml

- name: Take an action(UnholdAction) on certificate already recieved from CAGW
  entrust.crypto.cagw_certificate:
    cagw_api_client_cert_path: /etc/ssl/entrust/cagw-client.crt
    cagw_api_client_cert_key_path: /etc/ssl/entrust/cagw-client.key
    certificate_authority_id: ca_id
    request_type: action
    action_type: UnholdAction
    action_reason: unspecified
    serial_no: 5b9ba13d
    cagw_api_specification_path: /etc/ssl/entrust/cagw-api.yaml

- name: Take an action(RevokeAction) on certificate already recieved from CAGW
  entrust.crypto.cagw_certificate:
    cagw_api_client_cert_path: /etc/ssl/entrust/cagw-client.crt
    cagw_api_client_cert_key_path: /etc/ssl/entrust/cagw-client.key
    certificate_authority_id: ca_id
    request_type: action
    action_type: RevokeAction
    action_reason: unspecified
    serial_no: 5b9ba13d
    cagw_api_specification_path: /etc/ssl/entrust/cagw-api.yaml
'''

RETURN = '''
filename:
    description: The destination path for the generated certificate or PKCS12.
    returned: changed or success
    type: str
    sample: /etc/ssl/crt/www.ansible.com.crt

serial_number:
    description: The serial number of the issued certificate.
    returned: success
    type: str
    sample: 5b9ba13d

cert_days:
    description: The number of days the certificate remains valid from now.
    returned: success
    type: int
    sample: 253

cert_status:
    description:
        - The certificate status in CAGW.
        - 'Possible values are: ACCEPTED, normal, Revoked, Held'
    returned: success
    type: str

message:
    description:
        - Message we get from CAGW.
    returned: success
    type: dict

cert_details:
    description:
        - The full response JSON from the New/Get Certificate call of the CAGW API.
        - While the response contents are guaranteed to be forwards compatible with new CAGW API releases,
          Entrust recommends that you do not make any playbooks take actions based on the content of this field.
          However it may be useful for debugging, logging, or auditing purposes.
    returned: success
    type: dict

'''

from ansible_collections.entrust.crypto.plugins.module_utils.cagw.api import (
    cagw_client_argument_spec,
    CAGWClient,
    RestOperationException,
    SessionConfigurationException,
)

from dateutil.parser import parse
from datetime import datetime, timezone
import os
import traceback

from ansible.module_utils.compat.version import LooseVersion

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible.module_utils._text import to_native

from ansible_collections.entrust.crypto.plugins.module_utils.cagw.support import (
    load_certificate,
)

CRYPTOGRAPHY_IMP_ERR = None
try:
    import cryptography
    CRYPTOGRAPHY_VERSION = LooseVersion(cryptography.__version__)
except ImportError:
    CRYPTOGRAPHY_IMP_ERR = traceback.format_exc()
    CRYPTOGRAPHY_FOUND = False
else:
    CRYPTOGRAPHY_FOUND = True

MINIMAL_CRYPTOGRAPHY_VERSION = '1.6'


def calculate_cert_days(validityPeriod):
    expiry = validityPeriod.split("/")
    expiresAfter = expiry[1]
    cert_days = 0
    if expiresAfter:
        expires_after_datetime = parse(expiresAfter)
        cert_days = (expires_after_datetime - datetime.now(timezone.utc)).days
    return cert_days


class CagwCertificate(object):
    '''
    CA gateway certificate class
    '''
    def __init__(self, module):
        self.request_type = module.params['request_type']
        self.path = module.params['path']
        self.force = module.params['force']

        # All return values
        self.changed = False
        self.filename = None
        self.cert_details = None
        self.cert_status = None
        self.serialNumber = None
        self.cert_days = None
        self.message = None

        self.cert = None
        self.cagw_client = None
        if self.path and os.path.exists(self.path):
            try:
                self.cert = load_certificate(self.path, backend='cryptography')
            except Exception as dummy:
                self.cert = None
        # Instantiate the CAGW client
        try:
            self.cagw_client = CAGWClient(
                cagw_api_cert=module.params['cagw_api_client_cert_path'],
                cagw_api_cert_key=module.params['cagw_api_client_cert_key_path'],
                cagw_api_specification_path=module.params['cagw_api_specification_path']
            )
        except SessionConfigurationException as e:
            module.fail_json(msg='Failed to initialize Entrust Provider: {0}'.format(to_native(e)))

    def write_cert_to_file(self):
        fh = open(self.path, "w")
        try:
            fh.write(self.cert)
        finally:
            fh.close()

    def update_csr(self, module):
        body = {}
        csr = ''
        with open(module.params['csr']) as csr_file:
            lines = csr_file.readlines()
            # Remove first line
            lines = lines[1:]
            # Remove last line
            lines = lines[:-1]
            # Remove all linespaces
            csr = "".join(line.rstrip("\n") for line in lines)
        body['csr'] = csr
        return body

    def update_optional_certificate_request_details(self, module):
        body = {}
        optionalCertificateRequestDetails = {}
        optionalCertificateRequestDetails['subjectDn'] = module.params['dn']
        if module.params['validity_period']:
            optionalCertificateRequestDetails['validityPeriod'] = module.params['validity_period']
        body['optionalCertificateRequestDetails'] = optionalCertificateRequestDetails
        return body

    def update_properties(self, module):
        body = {}
        properties = {}
        if module.params['requester_name']:
            properties['tracking.requesterName'] = module.params['requester_name']
        if module.params['requester_email']:
            properties['tracking.requesterEmail'] = module.params['requester_email']
        if module.params['requester_phone']:
            properties['tracking.requesterPhone'] = module.params['requester_phone']
        if module.params['tracking_info']:
            properties['tracking.trackingInfo'] = module.params['tracking_info']
        if module.params['additional_emails']:
            properties['tracking.additionalEmails'] = module.params['additional_emails']
        if module.params['custom_fields']:
            # Omit custom fields from submitted dict if not present, instead of submitting them with value of 'null'
            # The ECS API does technically accept null without error, but it complicates debugging user escalations and is unnecessary bandwidth.
            for k, v in module.params['custom_fields'].items():
                if v is not None:
                    key = "tracking.customFields.{k}".format(k=k)
                    properties[key] = v
        body['properties'] = properties
        return body

    def update_protection(self, module):
        requiredFormat = {}
        protection = {}

        protection['type'] = "PasswordProtection"
        protection['password'] = module.params['p12_protection_password']

        requiredFormat['protection'] = protection
        return requiredFormat

    def update_required_format(self, module):
        body = {}
        requiredFormat = {}
        module_params_format = module.params['enrollment_format']
        requiredFormat['format'] = module_params_format
        if module_params_format == 'PKCS12':
            requiredFormat.update(self.update_protection(module))
        body['requiredFormat'] = requiredFormat
        return body

    def update_cert_subject_alt_name(self, module):
        body = {}
        subjectAltNames = []
        if module.params['subject_alt_name']:
            for k, v in module.params['subject_alt_name'].items():
                if v is not None:
                    options = {}
                    options['type'] = k
                    options['value'] = v
                    subjectAltNames.append(options)
            body['subjectAltNames'] = subjectAltNames
        return body

    def update_action(self, module):
        body = {}
        action = {}
        action['type'] = module.params['action_type']
        action['reason'] = module.params['action_reason']
        body['action'] = action
        return body

    def set_cert_details(self, module):
        module_params_format = module.params['enrollment_format']
        if module_params_format == 'X509':
            self.serialNumber = self.cert_details.get('serialNumber')
            self.validityPeriod = self.cert_details.get('validityPeriod')
            self.cert_days = calculate_cert_days(self.cert_details.get('validityPeriod'))

        if self.request_type == 'new':
            self.cert = self.cert_details.get('body')
        elif self.request_type == 'get':
            self.cert = self.cert_details.get('certificateData')

    def check(self, module):
        if self.cert:
            serial_number = "{0:X}".format(self.cert.serial_number)
            result = self.cagw_client.GetCertificate(ca_id=module.params['certificate_authority_id'],
                                                     serial_no=serial_number,
                                                     validate_certs=module.params['validate_certs'],
                                                     host=module.params['host'], port=module.params['port'])
            self.cert_details = result.get('certificate')
            # Changing the request type to get since we are getting the certificate here on the basis of
            # serial number and we need to populate the cert details on the get response only.
            self.request_type = 'get'
            self.set_cert_details(module)
            # Changing the request back to new
            self.request_type = 'new'

            module_params_connector_name = module.params['connector_name']
            # ECS CA getCertificate api through CAGW doesn't return status of the certificate
            if module_params_connector_name == 'SM':
                self.cert_status = self.cert_details.get('status')
                if self.cert_status == 'EXPIRED' or self.cert_status == 'expired' or \
                   self.cert_status == 'SUSPENDED' or self.cert_status == 'suspended' or \
                   self.cert_status == 'REVOKED' or self.cert_status == 'revoked' or self.cert_status == 'held':
                    return False

            if self.cert_days < module.params['remaining_days']:
                return False

            return True

        return False

    def request_cert(self, module):
        body = {}
        begin_line = "-----BEGIN CERTIFICATE-----\n"
        end_line = "\n-----END CERTIFICATE-----"
        try:
            if self.request_type == 'new':
                if self.force or not self.check(module):
                    body['profileId'] = module.params['certificate_profile_id']
                    body.update(self.update_required_format(module))
                    body.update(self.update_cert_subject_alt_name(module))
                    module_params_format = module.params['enrollment_format']
                    body.update(self.update_optional_certificate_request_details(module))
                    if module_params_format == 'X509':
                        body.update(self.update_csr(module))
                    module_params_connector_name = module.params['connector_name']
                    if module_params_connector_name == 'ECS':
                        body.update(self.update_properties(module))
                    result = self.cagw_client.NewCertRequest(Body=body, ca_id=module.params['certificate_authority_id'],
                                                             validate_certs=module.params['validate_certs'],
                                                             host=module.params['host'], port=module.params['port'])
                    self.cert_details = result.get('enrollment')
                    self.set_cert_details(module)
                    if module_params_format == 'X509':
                        self.cert = begin_line + self.cert + end_line
                    self.write_cert_to_file()
                    self.changed = True
                else:
                    return
            elif self.request_type == 'action':
                body.update(self.update_action(module))
                result = self.cagw_client.ActionOnCertificate(Body=body, ca_id=module.params['certificate_authority_id'],
                                                              serial_no=module.params['serial_no'],
                                                              validate_certs=module.params['validate_certs'],
                                                              host=module.params['host'], port=module.params['port'])
                self.cert_details = result.get('action')
            elif self.request_type == 'get':
                result = self.cagw_client.GetCertificate(ca_id=module.params['certificate_authority_id'],
                                                         serial_no=module.params['serial_no'],
                                                         validate_certs=module.params['validate_certs'],
                                                         host=module.params['host'], port=module.params['port'])
                self.cert_details = result.get('certificate')
                self.set_cert_details(module)
                self.cert = begin_line + self.cert + end_line
                self.write_cert_to_file()
                self.changed = True
        except RestOperationException as e:
            module.fail_json(msg='Failed in certificate operation from Entrust (CAGW) {0} Error:'.format(e))

        self.message = result.get('message')
        self.cert_status = self.cert_details.get('status')

    def dump(self):
        result = {
            'changed': self.changed,
            'filename': self.path,
            'cert_status': self.cert_status,
            'serialNumber': self.serialNumber,
            'cert_days': self.cert_days,
            'cert_details': self.cert_details,
            'message': self.message,
        }
        return result


def custom_fields_spec():
    return dict(
        text1=dict(type='str'),
        text2=dict(type='str'),
        text3=dict(type='str'),
        text4=dict(type='str'),
        text5=dict(type='str'),
        text6=dict(type='str'),
        text7=dict(type='str'),
        text8=dict(type='str'),
        text9=dict(type='str'),
        text10=dict(type='str'),
        text11=dict(type='str'),
        text12=dict(type='str'),
        text13=dict(type='str'),
        text14=dict(type='str'),
        text15=dict(type='str'),
        number1=dict(type='float'),
        number2=dict(type='float'),
        number3=dict(type='float'),
        number4=dict(type='float'),
        number5=dict(type='float'),
        date1=dict(type='str'),
        date2=dict(type='str'),
        date3=dict(type='str'),
        date4=dict(type='str'),
        date5=dict(type='str'),
        email1=dict(type='str'),
        email2=dict(type='str'),
        email3=dict(type='str'),
        email4=dict(type='str'),
        email5=dict(type='str'),
        dropdown1=dict(type='str'),
        dropdown2=dict(type='str'),
        dropdown3=dict(type='str'),
        dropdown4=dict(type='str'),
        dropdown5=dict(type='str'),
    )


def subject_alt_name_spec():
    return dict(
        dNSName=dict(type='str'),
        iPAddress=dict(type='str'),
        directoryName=dict(type='str'),
        uniformResourceIdentifier=dict(type='str'),
        rfc822Name=dict(type='str'),
    )


def cagw_certificate_argument_spec():
    return dict(
        force=dict(type='bool', default=False),
        path=dict(type='path'),
        request_type=dict(type='str', required=True, choices=['new', 'action', 'get']),
        action_type=dict(type='str', choices=['RevokeAction', 'HoldAction', 'UnholdAction']),
        action_reason=dict(type='str'),
        enrollment_format=dict(type='str', choices=['X509', 'PKCS12']),
        host=dict(type='str', required=True),
        port=dict(type='int', default=443),
        certificate_authority_id=dict(type='str', required=True),
        serial_no=dict(type='str'),
        p12_protection_password=dict(type='str', no_log=True),
        dn=dict(type='str'),
        validity_period=dict(type='str'),
        certificate_profile_id=dict(type='str'),
        csr=dict(type='path'),
        remaining_days=dict(type='int', default=30),
        connector_name=dict(type='str', choices=['SM', 'ECS', 'PKIaaS', 'MSCA']),
        tracking_info=dict(type='str'),
        requester_name=dict(type='str'),
        requester_email=dict(type='str'),
        requester_phone=dict(type='str'),
        additional_emails=dict(type='list', elements='str'),
        custom_fields=dict(type='dict', default=None, options=custom_fields_spec()),
        subject_alt_name=dict(type='dict', default=None, options=subject_alt_name_spec()),
        validate_certs=dict(type='bool', default=True),
    )


def main():
    cagw_argument_spec = cagw_client_argument_spec()
    cagw_argument_spec.update(cagw_certificate_argument_spec())
    module = AnsibleModule(
        argument_spec=cagw_argument_spec,
        required_if=(
            ['request_type', 'new', ['path', 'enrollment_format', 'certificate_profile_id', 'connector_name']],
            ['request_type', 'action', ['action_type', 'serial_no', 'action_reason']],
            ['request_type', 'get', ['path', 'serial_no']],
            ['enrollment_format', 'X509', ['csr']],
            ['enrollment_format', 'PKCS12', ['p12_protection_password', 'dn']],
            ['connector_name', 'ECS', ['requester_name', 'requester_email']],
        )
    )
    if not CRYPTOGRAPHY_FOUND or CRYPTOGRAPHY_VERSION < LooseVersion(MINIMAL_CRYPTOGRAPHY_VERSION):
        module.fail_json(msg=missing_required_lib('cryptography >= {0}'.format(MINIMAL_CRYPTOGRAPHY_VERSION)),
                         exception=CRYPTOGRAPHY_IMP_ERR)

    # A new x509 based enrollment request must have the csr field
    if module.params['request_type'] == 'new':
        module_params_format = module.params['enrollment_format']
        if module_params_format == "X509":
            module_params_csr = module.params['csr']
            if not os.path.exists(module_params_csr):
                module.fail_json(msg='The csr field of {0} was not a valid path.'.format(module_params_csr))

    certificate = CagwCertificate(module)
    certificate.request_cert(module)
    result = certificate.dump()
    module.exit_json(**result)


if __name__ == '__main__':
    main()
