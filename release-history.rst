.. _release_history:

Release and Version History
==============================================================================


Backlog (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.0.0 (2026-10-24)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Seed repo changes: `1.0.0 (2026-10-23) <https://github.com/MacHu-GWU/cookiecutter_pywf_internal_proprietary_demo-project/blob/1.0.0/release-history-seed-repo.rst#100-2026-10-23>`__

The first template release with the shared version: the template and its seed repo now share one version number, so a template version also names the seed state it was generated from. The version jumps from ``0.1.4`` to ``1.0.0`` for this reason. ``0.1.4`` was never released, so this release also carries its changes (see below). The seed changelog's ``1.0.0`` section lists everything a generated project gets.

**Breaking Changes**

- Preset branches are renamed: use ``--checkout preset/esc-sanhe-dev`` or ``--checkout preset/bmt-sanhe-dev`` instead of ``esc-sanhe-dev`` or ``bmt-sanhe-dev``. The old branches are no longer updated and will be deleted

**Features and Improvements**

- New variable ``aws_github_oidc_role_name``: the IAM role GitHub Actions assumes through OIDC to read AWS CodeArtifact, written into ``.github/workflows/main.yml``. It used to be the esc role, with only the region replaced
- A generated project gets a ``LICENSE.txt``: the proprietary license with the current year and the author. Before, it had none, although ``pyproject.toml`` lists it in ``license-files``
- Generation stops early when ``dev_python_version`` is not one of ``3.11``, ``3.12``, ``3.13``, ``3.14``, the versions a generated project supports
- Every release entry in this file now starts with a link to the seed repo's own changelog (``release-history-seed-repo.rst``) at the seed's tag of the same version

**Bugfixes**

- A project generated for a CodeArtifact domain other than ``esc`` installs and publishes again: ``[tool.uv.sources]`` points at the project's own index instead of ``esc``, and the credential variables are ``UV_INDEX_<DOMAIN>_USERNAME`` / ``UV_INDEX_<DOMAIN>_PASSWORD`` instead of ``UV_INDEX_ESC_*``
- The Python version of the CI jobs in ``.github/workflows/main.yml`` now follows ``dev_python_version``, instead of always ``3.12``
- The AWS console link of ``mise run remove-pkg-version`` now uses ``aws_region``, instead of always ``us-east-1``
- ``aws_codeartifact_domain`` and ``aws_region`` are only replaced where they are meant (CodeArtifact URLs, CLI options, ``mise.toml`` settings), so other text that happens to contain them stays as it is

**Miscellaneous**

- The template is maintained with the ``cctpl-*-cn`` Claude Code skills: ``mise run sync`` generates it from the seed and checks it (no seed value left over, no unresolved placeholder, the seed's own values render the seed back, valid presets), and ``mise run e2e`` also generates an ``esc-sanhe-dev`` project and runs its install, tests and docs build
- ``mise run publish-template`` only creates a release, never overwrites one; preset branches are regenerated from ``main`` plus ``presets/*.json`` by ``mise run publish-presets``


0.1.4 (2026-04-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- AI-first template: Claude Code takes over as the primary development assistant
- All tooling managed by ``mise``: Python, uv, and Claude are all ``mise``-managed
- Replaced old ``s01_run_cookiecutter_maker.py`` / ``s02_update_everything.py`` scripts with ``mise tasks`` for all automation; no longer depends on shell wrappers
- Expanded cookiecutter parameters: added ``license``, ``cloudflare_token_field``, ``aws_account_id``, ``aws_region``, ``aws_codeartifact_profile``, ``aws_codeartifact_domain``, ``aws_codeartifact_repository``, ``doc_host_aws_profile``, ``doc_host_s3_bucket``; removed ``codecov_token_field`` and ``readthedocs_token_field``
- Added confirmation gate to ``publish-template`` task (must type ``Y`` to proceed)
- Updated GitHub Actions workflows to latest versions


0.1.3 (2025-09-01)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add ``make uv-lock`` command to generate ``uv.lock`` file.
- Add support for publishing documentation website to Cloudflare Pages, which has built-in One-Time-Password (OTP) support using company email.
- Add support to use ``docs`` branch to publish documentation website to Cloudflare Pages.


0.1.2 (2025-06-23)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Use ``home_secret`` system to manage all secret tokens and keys.


0.1.1 (2025-04-02)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First Release.
- Use ``pywf_internal_proprietary`` as the automation engine.
