.. This file is the source of README.rst. Do not edit README.rst by hand:
   apply-template (mise run sync) renders it from this file.

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/cookiecutter-pywf_internal_proprietary/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/cookiecutter-pywf_internal_proprietary


``cookiecutter-pywf_internal_proprietary``
==============================================================================


Overview
------------------------------------------------------------------------------
This template provides a ready-to-use structure for internal, closed source Python library projects. It generates a complete development environment that allows you to start coding immediately and publish to a private `AWS CodeArtifact <https://aws.amazon.com/codeartifact/>`_ repository, never to PyPI.

**Key Features:**

- **Modern tooling**: Uses `mise-en-place <https://mise.jdx.dev/>`_ for task management and `uv <https://docs.astral.sh/uv/>`_ for fast Python package management
- **Private packages**: Resolves and publishes private packages through AWS CodeArtifact; ``mise run inst`` fetches the token with your AWS CLI profile
- **Complete CI/CD**: Pre-configured GitHub Actions that authenticate to AWS through OIDC, no long-lived AWS keys
- **Private documentation**: Sphinx documentation, hosted on Cloudflare Pages behind Cloudflare Access (latest) and AWS S3 (one copy per released version)
- **Developer-friendly**: Simple commands like ``mise run test`` or ``mise run cov`` replace complex pytest invocations
- **AI ready**: Ships Claude Code skills that know the project's toolchain and workflows


Disclaimer
------------------------------------------------------------------------------
The best practices implemented in this repository reflect my personal experience from developing `over 150 open source Python libraries <https://pypi.org/user/machugwu/>`_, 200+ proof-of-concept initiatives, 100+ enterprise-grade applications, and 50+ production systems, many of them internal libraries that never leave a company's private package repository. While these practices have proven effective for me, please use them at your own discretion.


Usage
------------------------------------------------------------------------------
Enter the following command to use the latest template version:

.. code-block:: bash

    pip install "cookiecutter>=2.6.0,<3.0.0" && cookiecutter https://github.com/MacHu-GWU/cookiecutter-pywf_internal_proprietary

To use a specific released version (see the `full list of releases <https://github.com/MacHu-GWU/cookiecutter-pywf_internal_proprietary/releases>`_):

.. code-block:: bash

    cookiecutter https://github.com/MacHu-GWU/cookiecutter-pywf_internal_proprietary --checkout tags/${version}

For example, to use ``1.0.0``, the latest version:

.. code-block:: bash

    cookiecutter https://github.com/MacHu-GWU/cookiecutter-pywf_internal_proprietary --checkout tags/1.0.0

You'll then be prompted to provide the following information (defaults in parentheses):

.. code-block:: bash

    [1/17] Your Python package name, in snake case (e.g. my_package) (your_package_name): your_package_name
    [2/17] Your GitHub username, the owner of the new repo (your_github_username): your_github_username
    [3/17] Author name for pyproject.toml file (Firstname Lastname): Firstname Lastname
    [4/17] Author email for pyproject.toml file (firstname.lastname@email.com): firstname.lastname@email.com
    [5/17] SPDX license expression for pyproject.toml (e.g. LicenseRef-Proprietary) (LicenseRef-Proprietary): LicenseRef-Proprietary
    [6/17] Semantic Version, in {major}.{minor}.{micro} (e.g. 0.1.1) (0.1.1): 0.1.1
    [7/17] Python version for local development, in {major}.{minor} (e.g. 3.12) (3.12): 3.12
    [8/17] GitHub token field path in home_secret.toml, see https://github.com/MacHu-GWU/home_secret_toml-project (your_github_token_field): your_github_token_field
    [9/17] Cloudflare API token field path in home_secret.toml, see https://github.com/MacHu-GWU/home_secret_toml-project (your_cloudflare_token_field): your_cloudflare_token_field
    [10/17] AWS CLI profile for publishing package to AWS CodeArtifact (your_aws_codeartifact_profile): your_aws_codeartifact_profile
    [11/17] AWS CLI profile for deploying documentation to AWS S3 (your_doc_host_aws_profile): your_doc_host_aws_profile
    [12/17] AWS S3 bucket for storing versioned documentation (your_doc_host_s3_bucket): your_doc_host_s3_bucket
    [13/17] AWS CodeArtifact domain name (your_aws_codeartifact_domain): your_aws_codeartifact_domain
    [14/17] AWS CodeArtifact Python repository name (your_aws_codeartifact_repository): your_aws_codeartifact_repository
    [15/17] Your 12 digits AWS Account Id where you put your CodeArtifact domain, e.g. 111122223333 (111122223333): 111122223333
    [16/17] Your AWS CodeArtifact region name, e.g. us-east-1 (us-east-1): us-east-1
    [17/17] IAM role name that GitHub Actions assumes through OIDC to read AWS CodeArtifact (role/<name> in .github/workflows/main.yml) (your_aws_github_oidc_role_name): your_aws_github_oidc_role_name

This will generate a repository structure similar to `cookiecutter_pywf_internal_proprietary_demo-project <https://github.com/MacHu-GWU/cookiecutter_pywf_internal_proprietary_demo-project>`_.

Once generated, navigate to your project directory and explore the available automation tasks:

.. code-block:: bash

    cd your_package_name-project
    mise tasks ls  # List all available tasks


Project Maintainer Note
------------------------------------------------------------------------------
**Project Architecture:**

- **Seed Repository**: `cookiecutter_pywf_internal_proprietary_demo-project <https://github.com/MacHu-GWU/cookiecutter_pywf_internal_proprietary_demo-project>`_ - A concrete, runnable project used as the source for template generation
- **Cookiecutter Template**: `cookiecutter-pywf_internal_proprietary <https://github.com/MacHu-GWU/cookiecutter-pywf_internal_proprietary>`_ - This repository

**Maintenance Workflow:**

This template is maintained using a "reverse engineering" approach, driven by Claude Code skills (``.claude/skills/cctpl-*-cn``):

1. Make changes in the Seed project (``cookiecutter_pywf_internal_proprietary_demo-project``)
2. In the Seed, bump the version and record the changes in its own ``release-history-seed-repo.rst``. The Seed and this template share one version number, and the Seed's ``pyproject.toml`` is its only source
3. Run ``mise run e2e``: it converts the Seed into a template, checks it, applies it to this repo (version included), then generates a project and runs its tests and docs build
4. Commit and push the Seed, then tag it with ``mise run publish`` and ``mise run release`` in the Seed
5. Run ``/cctpl-release-cn`` to write this repo's changelog section, which links to the Seed's section of the same version, then ``mise run publish-template`` to publish the template to GitHub. A published version is never overwritten
6. Run ``/cctpl-verify-cn`` to verify the published template

**Toolchain:**

- **mise-en-place**: Task runner and tool version manager
- **uv**: Fast Python package installer and resolver
- **cookiecutter-maker**: Reverse-engineering tool that converts concrete projects into templates

For the full maintenance specification, see `cctpl-base-cn <./.claude/skills/cctpl-base-cn/SKILL.md>`_.
