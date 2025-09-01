.. image:: https://img.shields.io/badge/✍️_Release_History!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/cookiecutter-pywf_internal_proprietary/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/cookiecutter-pywf_internal_proprietary


``cookiecutter-pywf_internal_proprietary``
==============================================================================


Overview
------------------------------------------------------------------------------
This template provides a ready-to-use structure for Python internal proprietary library projects. It generates a complete development environment that allows you to start coding immediately and publish to `PyPI <https://pypi.org/>`_. with minimal setup.

The template uses `pywf_internal_proprietary <https://github.com/MacHu-GWU/pywf_internal_proprietary-project>`_ as its automation engine, eliminating the cognitive overhead of remembering complex commands like ``poetry install --extras ...`` or ``pytest -s --tb=native --cov=your_package_name --cov-report term-missing tests``.

A standout feature is the built-in AI coding assistant that creates a knowledge base from your documentation, source code, and other specified files. Unlike solutions requiring vector store databases, you can simply drag and drop files to start interacting with an AI that understands your coding, testing, and documentation style. No need for Cursor, Windsurf, or API tokens - just specify which file, module, function, or class you want to work with, and it's ready to assist.


Disclaimer
------------------------------------------------------------------------------
The best practices implemented in this repository reflect my personal experience from developing `over 150 open source Python libraries <https://pypi.org/user/machugwu/>`_, 200+ proof-of-concept initiatives, 100+ enterprise-grade applications, and 50+ production systems. This workflow enables me to publish a new Python library to PyPI within an hour of conception. While these practices have proven effective for me, please use them at your own discretion.


Usage
------------------------------------------------------------------------------
Enter the following command to use the latest template version:

.. code-block:: bash

    pip install "cookiecutter>=2.6.0,<3.0.0" && cookiecutter https://github.com/MacHu-GWU/cookiecutter-pywf_internal_proprietary

To use a specific released version (see the `full list of release at here <https://github.com/MacHu-GWU/cookiecutter-pywf_internal_proprietary/releases>`_).

.. code-block:: bash

    cookiecutter https://github.com/MacHu-GWU/cookiecutter-pywf_internal_proprietary --checkout tags/${version}

For example, to use ``0.1.3`` (the latest as of 2025-09-01):

.. code-block:: bash

    cookiecutter https://github.com/MacHu-GWU/cookiecutter-pywf_internal_proprietary --checkout tags/0.1.3

You'll then be prompted to provide the following information:

.. code-block:: bash

    [1/16] Your Python package name, in snake case (e.g. my_package) (your_package_name):
    [2/16] github_username (your_github_username):
    [3/16] Author name for pyproject.toml file (Firstname Lastname):
    [4/16] Author email for pyproject.toml file (firstname.lastname@email.com):
    [5/16] Semantic Version, in {major}.{minor}.{micro} (e.g. 0.1.1) (0.1.1):
    [6/16] Python version for local development, in {major}.{minor}.{micro} (e.g. 3.11.8) (3.11.8):
    [7/16] AWS CLI profile for publishing package to AWS CodeArtifact, e.g. your_aws_codeartifact_profile (your_aws_codeartifact_profile):
    [8/16] AWS CLI profile for publishing document website to AWS S3 bucket, e.g. your_doc_host_aws_profile (your_doc_host_aws_profile):
    [9/16] AWS S3 Bucket to store document site historical versions (your_doc_host_s3_bucket):
    [10/16] Your AWS CodeArtifact region name, e.g. us-east-1 (us-east-1):
    [11/16] Your 12 digits AWS Account Id where you put your CodeArtifact domain, e.g. 111122223333 (111122223333):
    [12/16] AWS CodeArtifact domain name (your_aws_codeartifact_domain):
    [13/16] AWS CodeArtifact Python repository name (your_aws_codeartifact_repository):
    [14/16] GitHub token field, Read https://github.com/MacHu-GWU/home_secret-project to learn how to set up your GitHub token using home_secret.json
    (your_github_token_field):
    [15/16] Codecov.io token field, Read https://github.com/MacHu-GWU/home_secret-project to learn how to set up your GitHub token using home_secret.json
    (your_codecov_token_field):
    [16/16] Your cloudflare token, , Read https://github.com/MacHu-GWU/home_secret-project to learn how to set up your GitHub token using home_secret.json
    (your_cloudflare_token_field):

This will generate a repository structure similar to `cookiecutter_pywf_internal_proprietary_demo-project <https://github.com/MacHu-GWU/cookiecutter_pywf_internal_proprietary_demo-project>`_ (Not a public Git Repo).


Variations
------------------------------------------------------------------------------
For my personal internal proprietary Python projects, I use a custom branch:

.. code-block:: bash

    cookiecutter https://github.com/MacHu-GWU/cookiecutter-pywf_internal_proprietary --checkout esc-sanhe-dev


Project Maintainer Note
------------------------------------------------------------------------------
this project follows the best practice mentioned in `THIS DOCUMENT <https://dev-exp-share.readthedocs.io/en/latest/search.html?q=Creating+Reusable+Project+Templates%3A+From+Concept+to+Implementation&check_keywords=yes&area=default>`_.

- **Seed Repository**: `cookiecutter_pywf_internal_proprietary_demo-project <https://github.com/MacHu-GWU/cookiecutter_pywf_internal_proprietary_demo-project>`_
- **Automation Library**: `pywf_internal_proprietary-project <https://github.com/MacHu-GWU/pywf_internal_proprietary-project>`_
- **Cookiecutter Template**: `cookiecutter-pywf_internal_proprietary <https://github.com/MacHu-GWU/cookiecutter-pywf_internal_proprietary>`_
