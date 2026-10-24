.. image:: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project/actions?query=workflow:CI

.. .. image:: https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project

.. image:: https://img.shields.io/badge/Cloudflare%20Pages-📔_Document-None.svg?style=flat&logo=cloudflare&color=darkorange
    :target: https://{{ cookiecutter.package_name | slugify }}.pages.dev

.. image:: https://img.shields.io/badge/AWS_CodeArtifact-📦_Link-None.svg?style=flat&logo=amazonwebservices&logoColor=darkorange&color=darkorange
    :target: https://{{ cookiecutter.aws_region }}.console.aws.amazon.com/codesuite/codeartifact/d/{{ cookiecutter.aws_account_id }}/{{ cookiecutter.aws_codeartifact_domain }}/r/{{ cookiecutter.aws_codeartifact_repository }}/p/pypi/{{ cookiecutter.package_name | slugify }}/versions?region={{ cookiecutter.aws_region }}

.. image:: https://img.shields.io/badge/✍️_Release_History!--None.svg?style=social&logo=github
    :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
    :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project

------

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://{{ cookiecutter.package_name | slugify }}.pages.dev/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project/releases


Welcome to ``{{ cookiecutter.package_name }}`` Documentation
==============================================================================
Documentation for ``{{ cookiecutter.package_name }}``.


.. _install:

Install
------------------------------------------------------------------------------
``{{ cookiecutter.package_name }}`` is a private package, released on the company's AWS CodeArtifact repository, not on PyPI. You need AWS credentials that can read that repository.

With uv, declare the private index in your project's ``pyproject.toml``, and pin this package **and every private package it depends on** to it (uv only reads ``[tool.uv.sources]`` from your own project):

.. code-block:: toml

    [project]
    dependencies = [
        "{{ cookiecutter.package_name | slugify }}>=0.1.4,<1.0.0",
        "esc-aws-org-struct>=0.1.3,<1.0.0", # private dependency of the package above
    ]

    [[tool.uv.index]]
    name = "{{ cookiecutter.aws_codeartifact_domain }}"
    url = "https://{{ cookiecutter.aws_codeartifact_domain }}-{{ cookiecutter.aws_account_id }}.d.codeartifact.{{ cookiecutter.aws_region }}.amazonaws.com/pypi/{{ cookiecutter.aws_codeartifact_repository }}/simple/"
    authenticate = "always"
    explicit = true

    [tool.uv.sources]
    {{ cookiecutter.package_name | slugify }} = { index = "{{ cookiecutter.aws_codeartifact_domain }}" }
    esc-aws-org-struct = { index = "{{ cookiecutter.aws_codeartifact_domain }}" }

Then fetch a CodeArtifact token before ``uv sync``:

.. code-block:: console

    $ export UV_INDEX_{{ cookiecutter.aws_codeartifact_domain | upper | replace('-', '_') }}_USERNAME=aws
    $ export UV_INDEX_{{ cookiecutter.aws_codeartifact_domain | upper | replace('-', '_') }}_PASSWORD="$(aws codeartifact get-authorization-token --domain {{ cookiecutter.aws_codeartifact_domain }} --domain-owner {{ cookiecutter.aws_account_id }} --query authorizationToken --output text)"
    $ uv sync

With pip:

.. code-block:: console

    $ aws codeartifact login --tool pip --domain {{ cookiecutter.aws_codeartifact_domain }} --domain-owner {{ cookiecutter.aws_account_id }} --repository {{ cookiecutter.aws_codeartifact_repository }}
    $ pip install {{ cookiecutter.package_name | slugify }}
