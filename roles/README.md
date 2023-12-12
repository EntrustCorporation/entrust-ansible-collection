cagw_certificate_request_role
=====================

Purpose of role
---------------
This role creates a PKI certificate signed by Certificate Authority supported by Entrust CA Gateway.
List of Supported authorities are Entrust Certificate Authority, Entrust Certificate Solution (public CA), Microsoft CA (Third party CA), Entrust PKIaaS
This role performs below tasks -
 - Creates a private key.
 - Creates a certificate signing request (CSR).
 - Create, retrieve, or perform following actions HoldAction, UnholdAction, RevokeAction for your certificates using the Entrust CAGW API.
   - Note: You must have Entrust CA Gateway credentials.
      
	  
Requirements
------------ 
 - Ansible version 2.9
 - PyYAML version 3.11 or higher
 - cryptography version 1.6 or higher

Role Variables
--------------

See variables in defaults/main.yml


Dependencies
------------

None

Example Playbook
----------------

The command below is an example of how to use the role.

Before running the example you will need to to update the below: 
	
Mandatory Parameters:

	working_path # Path that the key pair, certificate signing request, and certificate will be stored in,

	request_type,

	entrust_host,

	cagw_api_specification_path(CAGW API spec is available here roles/common/files/cagw-api.yaml)

	certificate_authority_id

Mandatory authentication parameters:

	entrust_cagw_api_cert,
	entrust_cagw_api_cert_key

Mandatory parameters based on certain conditions:

	if O(request_type = new) then path, enrollment_format, certificate_profile_id and, connector_name,

	if O(request_type = action) then action_type, serial_no and, action_reason,

	if O(request_type = get) then path and, serial_no,

	if O(enrollment_format = X509) then csr,

	if O(enrollment_format = PKCS12) then p12_protection_password and, dn,

	if O(connector_name = ECS) then entrust_requester_name, entrust_requester_email and, entrust_requester_phone

Optional parameters:

	csr_path: # Full path to the location that will be used to save the certificate signing request,

	common_name, organization_name, locality_name, country_name, state_or_province_name: to be used to generate the CSR,

	privatekey_path: # Full path to the location that will be used to save the private key,

	entrust_port: default port is 443,

	remaining_days
			   
Run command "ansible-playbook sample_playbook.yml"

Additional references
---------------------
- Leveraging Deployment Automation Ansible Role to Set Up and Refresh Your Web Infrastructure (article)
https://blog.entrust.com/2019/08/leveraging-deployment-automation-tools/ 
		
License
-------

MIT

Author Information
------------------
This role was created by Sapna Jain 
Copyright (c), Entrust Corporation, 2023
