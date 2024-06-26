# Wishlists Service
[![Build Status](https://github.com/CSCI-GA-2820-SP24-001/wishlists/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP24-001/wishlists/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-red.svg)](https://www.python.org/)

This is the repo for the Wishlists microservice. Please see below for the RESTful routes of `wishlists` and `items`.

```
Endpoint              Methods  Rule
----------------      -------  -----------------------------------------------------
index                  GET      /

list_wishlists         GET      /wishlists
create_wishlists       POST     /wishlists
get_wishlists          GET      /wishlists/<wishlist_id>
update_wishlists       PUT      /wishlists/<wishlist_id>
delete_wishlists       DELETE   /wishlists/<wishlist_id>

list_items             GET      /wishlists/<int:wishlist_id>/items
create_wishlist_items  POST     /wishlists/<wishlist_id>/items
get_items              GET      /wishlists/<wishlist_id>/items/<item_id>
update_item            PUT      /wishlists/<wishlist_id>/items/<item_id>
delete_items           DELETE   /wishlists/<wishlist_id>/items/<item_id>
```
The test cases have 95% test coverage and can be run with `pytest`

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── routes.py              - module with service routes
├── models                 - business model code package
│   ├── item.py            - model of items
│   └── wishlist.py        - model of wishlists
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/                     - test cases package
├── __init__.py            - package initializer
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes
```

## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
