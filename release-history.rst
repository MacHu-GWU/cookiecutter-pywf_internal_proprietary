.. _release_history:

Release and Version History
==============================================================================


Backlog (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


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
