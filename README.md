# Ansible Collection - entrust.crypto

Request SSL/TLS certificates with the Certificate Authority Gateway (CAGW) API.
You can find documentation for the collection [here](https://entrustcorporation.github.io/entrust-ansible-collection/)

## Ansible version compatibility

Tested with the Ansible Core >= 2.14.0 versions, and the current development version of Ansible. Ansible Core versions before 2.14.0 are not supported.

## Python version compatibility

This collection is tested with Python 3.10.12. Minimum Python version of `3.6` is required for this collection to function properly.

## Installing this collection

### Using `ansible-galaxy` CLI

To install the Entrust Crypto Ansible Collection using the command-line interface, execute the following:

```terminal
ansible-galaxy collection install entrust.crypto
```

### Using a `requirements.yml` File

To include the collection in a `requirements.yml` file and install it through `ansible-galaxy`, use the following format:

```yaml
---
collections:
  - entrust.crypto
```

Then run:

```terminal
ansible-galaxy collection install -r requirements.yml
```

# Contributing

If you want to develop new content or improve on this collection, please open an issue or create a pull request. All contributions are welcome!

# Release Notes

See the [changelog](https://github.com/EntrustCorporation/entrust-ansible-collection/blob/main/changelogs/changelog.yaml) for a history of notable changes to this collection

# License

See the [license](https://github.com/EntrustCorporation/entrust-ansible-collection/blob/main/LICENSE) for more information
