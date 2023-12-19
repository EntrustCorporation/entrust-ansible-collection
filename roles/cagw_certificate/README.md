# Entrust `cagw_certificate` Role for Ansible

This role creates a PKI certificate signed by Certificate Authority supported by Entrust CA Gateway.
List of Supported authorities are Entrust Certificate Authority, Entrust Certificate Solution (public CA), Microsoft CA (Third party CA), Entrust PKIaaS
This role performs below tasks -
 - Creates a private key.
 - Creates a certificate signing request (CSR).
 - Create, retrieve, or perform following actions HoldAction, UnholdAction, RevokeAction for your certificates using the Entrust CAGW API.

 >**NOTE:** You must have Entrust CA Gateway credentials.
      
	  
Requirements
------------ 
 - Ansible Core >= 2.14.0
 - PyYAML version 3.11 or higher
 - cryptography version 1.6 or higher

Role Variables
--------------

   | Variable Name                             | Description                                                  |
   | -------------------------------           | ------------------------------------------------------------ |
   | `cagw_certificate_entrust_host`           | Entrust CA Gateway Server IP or URL(Mandatory) |
   | `cagw_certificate_entrust_port`           | Entrust CA Gateway Server Port(Default port is 443) |
   | `cagw_certificate_api_cert`               | Entrust CAGW tenant Credential Certificate(Mandatory) |
   | `cagw_certificate_api_cert_key`           | Entrust CAGW tenant Credential Key(Mandatory) |
   | `cagw_certificate_api_specification_path` | Entrust CAGW API spec file path(Mandatory) |
   | `cagw_certificate_connector_name`         | Certificate Authority type, can be SM, ECS, PKIaaS or MSCA (Mandatory) |
   | `cagw_certificate_ca_id`                  | Certificate Authority Id to perform Certificate Operations (Mandatory) |
   | `cagw_certificate_request_type`           | Can be new(enrollment), get(retrieve certificate), action(action to be taken on the certificate)(Mandatory) |
   | `cagw_certificate_enrollment_format`      | Can be X509 or PKCS12 (Mandatory) |
   | `cagw_certificate_profile_id`             | Certificate Authority Profile Id (Mandatory when cagw_certificate_request_type is new) |
   | `cagw_certificate_cert_path`              | The destination path for the generated certificate(Mandatory when cagw_certificate_request_type is new) |
   | `cagw_certificate_dn`                     | Subject DN of certificates (Mandatory when cagw_certificate_enrollment_format is PKCS12) |
   | `cagw_certificate_p12_password`           | Mandatory when cagw_certificate_enrollment_format is PKCS12 |
   | `cagw_certificate_serialnumber`           | Mandatory when cagw_certificate_request_type is get or action |
   | `cagw_certificate_requester_name`         | Mandatory when cagw_certificate_connector_name is ECS |
   | `cagw_certificate_requester_email`        | Mandatory when cagw_certificate_connector_name is ECS |
   | `cagw_certificate_action_type`            | Can be RevokeAction, HoldAction or UnholdAction(Mandatory when cagw_certificate_request_type is action |
   | `cagw_certificate_action_reason`          | Reason to take specific action(Mandatory when cagw_certificate_request_type is action |

   Refer defaults/main.yml for complete list


Dependencies
------------

None

Example Playbook
----------------

See [sample playbook](https://github.com/EntrustCorporation/entrust-ansible-collection/blob/main/examples/sample_playbook.yml).

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
