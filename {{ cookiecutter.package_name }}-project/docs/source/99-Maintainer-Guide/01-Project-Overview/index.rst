Project Overview
==============================================================================

Overview
------------------------------------------------------------------------------
This project is an **AI-First Python internal library skeleton** — a battle-tested starting point purpose-built for teams that ship private, pip-installable Python packages inside an enterprise environment. Unlike a public open source library, this package is never deployed as a service; it's a library consumed by other internal projects via ``pip install``. Everything in this skeleton is tuned for that use case: private registries, gated documentation, and a secure-by-default CI/CD pipeline.

The toolchain is modern, opinionated, and fast:

- Private package distribution via **AWS CodeArtifact** — your own PyPI, inside your AWS account
- Documentation gated behind **Cloudflare Pages** with OTP email authentication — only colleagues with a company email can read it
- A **hybrid CI/CD strategy** on GitHub Actions that mixes official GitHub Actions with ``mise``-managed tools for maximum reliability and caching efficiency
- First-class **Claude Code** integration baked in from day one


Dev Tool Manager — mise
------------------------------------------------------------------------------
We use `mise (mise en place) <https://mise.jdx.dev>`_ to manage every developer tool in the project. The single source of truth is `mise.toml <https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project/blob/main/mise.toml>`_. Throughout this guide, whenever a new tool or environment variable is introduced, we'll always point back to the corresponding entry in that file.

This project's ``mise.toml`` has evolved significantly compared to simpler skeletons — it carries the full weight of a private enterprise workflow. Open it up and read it carefully; it's well-commented and self-explanatory. Here's what makes it special:

- **Tool version pinning.** Python, ``uv``, ``pandoc``, ``awscli``, ``node``, ``wrangler``, and ``claude`` are all declared in ``[tools]`` — one file pins the entire toolchain.
- **Environment variable management.** The ``[env]`` section is the single source of truth for all project-level env vars. Sensitive values (tokens, secrets) are fetched from ``~/home_secret.toml`` via ``hst`` locally; in CI they are injected as GitHub Secrets. The same ``mise.toml`` works in both environments with zero changes.
- **Rich task library.** The ``[tasks.*]`` sections replace ``make``, shell scripts, and tribal knowledge. Every workflow — install, test, publish, release, deploy docs, manage Cloudflare Pages — is a single ``mise run <task>`` away.

The most important commands you'll use day-to-day:

- ``mise run inst`` — install all project dependencies (syncs from ``pyproject.toml`` via ``uv``)
- ``mise run cov`` — run unit tests with a coverage report
- ``mise run publish`` — build and publish the package to AWS CodeArtifact
- ``mise run release`` — cut a new GitHub release
- ``mise run deploy-pages`` — deploy documentation to Cloudflare Pages


Package Manager — uv
------------------------------------------------------------------------------
We use `uv <https://docs.astral.sh/uv/>`_ as the Python package manager. Written in Rust, it resolves and installs dependencies 10–100x faster than ``pip`` or ``poetry`` — and it speaks the standard ``pyproject.toml`` format natively.

All package metadata, dependencies, and optional extras live in `pyproject.toml <https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project/blob/main/pyproject.toml>`_. You never need to call ``uv`` directly for day-to-day work — ``mise run inst`` handles it.

- Deterministic lockfile (``uv.lock``) for fully reproducible environments across machines and CI
- Private index support: the ``[[tool.uv.index]]`` block in ``pyproject.toml`` points ``uv`` at your AWS CodeArtifact repository for private packages, while all public packages still resolve from PyPI
- Seamlessly integrated with ``mise`` — zero friction, zero ceremony


Coding Agent — Claude Code
------------------------------------------------------------------------------
We treat Claude Code as a first-class member of the development workflow. The project ships with a `CLAUDE.md <https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project/blob/main/CLAUDE.md>`_ file that gives Claude a complete map of the project: which tools are in use, how to run tasks, where tests live, and how to navigate the codebase without wasting tokens on guesswork.

This means Claude can:

- Run ``mise run cov`` to execute tests and interpret failures in context
- Navigate ``pyproject.toml`` for dependency and private-index configuration
- Follow the project's testing conventions without being briefed every session

No more copy-pasting boilerplate into every chat. The `.claude/ <https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project/tree/main/.claude>`_ directory holds additional context files that keep the agent grounded in this project's specific conventions — including task documentation and message templates.


Unit Testing — pytest
------------------------------------------------------------------------------
Tests are written with `pytest <https://docs.pytest.org>`_ and configured for coverage tracking. The relevant config files are:

- `.coveragerc <https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project/blob/main/.coveragerc>`_ — coverage measurement settings (which paths to include, which to exclude)

This project does **not** use Codecov — coverage reports are generated locally and in CI for the team's own inspection, without publishing to a third-party service. That's a deliberate choice for an internal library: keep everything inside your own perimeter.

A unique pattern used in this project: every test file can be run as a standalone script. The ``if __name__ == "__main__":`` block at the bottom of each test file invokes pytest as a subprocess, targeting only that file. This lets you iterate on a single test module in complete isolation — no full suite spin-up, no IDE configuration required. Fast feedback, zero ceremony.

Run all tests with coverage in one shot:

.. code-block:: bash

    mise run cov


Documentation — Sphinx + Cloudflare Pages
------------------------------------------------------------------------------
Documentation is built with `Sphinx <https://www.sphinx-doc.org>`_ from source files in `docs/source/ <https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project/tree/main/docs/source>`_ and deployed to **Cloudflare Pages** — not a public hosting service, but a gated internal one.

What makes this setup special: Cloudflare Pages is configured with **email OTP (One-Time Password) authentication**. Anyone visiting the documentation URL must enter their company email address and confirm via a one-time code. Only email addresses on the allowlist (your company domain) can get in. Your internal documentation stays internal — no accidental public exposure.

The deployment workflow:

- Build docs locally with ``mise run build-doc``
- Preview locally with ``mise run view-doc``
- Deploy to Cloudflare Pages with ``mise run deploy-pages`` (or let CI do it automatically on the ``doc`` branch — see the CI/CD section below)

The ``wrangler`` CLI (Cloudflare's deployment tool) is managed as part of the toolchain. Authentication uses the ``CLOUDFLARE_API_TOKEN`` environment variable, which is fetched from ``~/home_secret.toml`` locally and injected as a GitHub Secret in CI.


Package Publishing — AWS CodeArtifact
------------------------------------------------------------------------------
This is an **internal library** — it is never published to the public PyPI. Instead, packages are published to `AWS CodeArtifact <https://aws.amazon.com/codeartifact/>`_, which acts as your team's private PyPI inside your AWS account.

The relevant configuration lives in two places:

- `pyproject.toml <https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project/blob/main/pyproject.toml>`_ — the ``[[tool.uv.index]]`` block declares the CodeArtifact endpoint, and ``[tool.uv.sources]`` pins private packages to that index
- `mise.toml <https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project/blob/main/mise.toml>`_ — the ``[env]`` section holds ``AWS_CODEARTIFACT_*`` variables; ``.mise/tasks/codeartifact-env.sh`` fetches a short-lived auth token and exports it before ``uv`` runs

Publishing is a one-liner:

.. code-block:: bash

    mise run publish

This builds the wheel, authenticates against CodeArtifact via OIDC (in CI) or your local AWS profile (locally), and uploads the artifact. Consumers in other projects add the CodeArtifact index to their own ``uv`` config and ``pip install`` as usual.


CI/CD — GitHub Actions
------------------------------------------------------------------------------
Continuous integration runs on GitHub Actions, configured in `.github/workflows/main.yml <https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}-project/blob/main/.github/workflows/main.yml>`_.

This pipeline uses a **hybrid tool management strategy** — a deliberate, performance-optimized design that's worth understanding:

- Tools with excellent official GitHub Actions (Python, ``uv``, Node.js, AWS credentials) are managed by those actions — they come with built-in caching, matrix support, and battle-tested reliability.
- Tools without good GA equivalents (``pandoc``) are managed by ``mise`` and installed on-demand via ``install_args``.
- ``wrangler`` is installed explicitly via ``npm install -g`` after ``actions/setup-node`` — this avoids a conflict where ``mise``'s ``npm:wrangler`` backend would try to use ``mise``'s own node instead of the one provided by the GA step.
- ``MISE_DISABLE_TOOLS`` is set at the job level to prevent ``mise`` from auto-installing tools that are already provided by GitHub Actions — keeping CI fast and deterministic.

The pipeline has **two jobs**:

- **test** — runs on every push and pull request to ``main`` and ``doc`` branches. Installs dependencies, runs the full test suite with coverage. This is your quality gate.
- **deploy-doc** — runs only when pushing to the ``doc`` branch, and only after ``test`` passes. Builds the Sphinx documentation and deploys it to Cloudflare Pages via ``wrangler``.

The **``doc`` branch** is the deployment trigger for documentation. The workflow is: build your docs, merge or push to ``doc``, and CI deploys automatically. This keeps doc deployments deliberate and auditable — you choose exactly when to publish, rather than deploying on every ``main`` push.

AWS authentication in CI uses **OIDC** (OpenID Connect) — no long-lived AWS credentials stored as secrets. The CI job assumes an IAM role with CodeArtifact permissions via a token exchange, following AWS security best practices.
