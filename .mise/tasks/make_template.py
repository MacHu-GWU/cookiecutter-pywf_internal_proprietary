# -*- coding: utf-8 -*-

"""
Convert the seed repo into a cookiecutter template.

Input: the git-visible files of the seed repo (``CCTPL_SEED_DIR``).
Output: ``tmp/cctpl/template/``, a complete cookiecutter template root.

Rules: ``.claude/skills/cctpl-base-cn/references/03-parameterization.md``.
"""

import sys
import json
import tomllib

from cookiecutter_maker.api import Parameter, Maker

import cctpl

try:
    dir_seed = cctpl.get_seed_dir()
except cctpl.TaskError as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)

with open(dir_seed / "pyproject.toml", "rb") as f:
    _pyproject = tomllib.load(f)
with open(dir_seed / "mise.toml", "rb") as f:
    _mise_config = tomllib.load(f)


class SeedValues:
    """Concrete values in the seed repo that become cookiecutter variables."""

    # --- identity
    package_name = "cookiecutter_pywf_internal_proprietary_demo"
    package_name_slug = "cookiecutter-pywf-internal-proprietary-demo"
    github_username = "MacHu-GWU"
    # Not a parameter: only scanned for leaks (UNIQUE_SEED_VALUES).
    pypi_username = "machugwu"

    # --- author
    author = "Sanhe Hu"
    author_email = "husanhe@gmail.com"

    # --- license
    license = "LicenseRef-Proprietary"

    # --- versioning (read from the seed)
    version = _pyproject["project"]["version"]
    dev_python_version = _mise_config["tools"]["python"]

    # --- secret token fields
    github_token_field = "github.accounts.sh.users.sh.secrets.dev.value"
    cloudflare_token_field = "cloudflare.accounts.esc.users.sh_esc.secrets.cloudflare_pages_upload.value"

    # --- AWS (read from the seed's mise.toml [env])
    aws_codeartifact_profile = _mise_config["env"]["AWS_CODEARTIFACT_PROFILE"]
    doc_host_aws_profile = _mise_config["env"]["DOC_HOST_AWS_PROFILE"]
    doc_host_s3_bucket = _mise_config["env"]["DOC_HOST_S3_BUCKET"]
    aws_codeartifact_domain = _mise_config["env"]["AWS_CODEARTIFACT_DOMAIN"]
    aws_codeartifact_repository = _mise_config["env"]["AWS_CODEARTIFACT_REPO"]
    aws_account_id = _mise_config["env"]["AWS_CODEARTIFACT_DOMAIN_OWNER"]
    aws_region = _mise_config["env"]["AWS_CODEARTIFACT_REGION"]
    # The IAM role GitHub Actions assumes through OIDC (.github/workflows/main.yml).
    aws_github_oidc_role_name = "ghoidc-esc_aws_codeartifacts_only-devops-us-east-1"


_parts = SeedValues.version.split(".")
assert len(_parts) == 3 and all(v.isdigit() for v in _parts), (
    f"Invalid version: {SeedValues.version}"
)

_HOME_SECRET_HELP = "see https://github.com/MacHu-GWU/home_secret_toml-project"

# The uv index is named after the CodeArtifact domain, and uv reads its
# credentials from UV_INDEX_<NAME>_USERNAME / _PASSWORD, where <NAME> is the
# index name upper-cased with every non-alphanumeric character turned into "_".
_DOMAIN = SeedValues.aws_codeartifact_domain
_DOMAIN_ENV = _DOMAIN.upper().replace("-", "_")
_REGION = SeedValues.aws_region
_PY = SeedValues.dev_python_version

# The seed depends on the demo private package ``esc-aws-org-struct``
# (pyproject.toml, README.rst, example_module_1.py). It stays literal: a
# generated project keeps a working private dependency to replace with its own.
# No parameter touches it: the aws_codeartifact_domain contexts below never
# match inside it.
PARAMETERS = [
    Parameter(
        selector=[SeedValues.package_name],
        name="package_name",
        default="your_package_name",
        prompt="Your Python package name, in snake case (e.g. my_package)",
    ),
    Parameter(
        selector=[SeedValues.package_name_slug],
        name="package_name_slug",
        custom_placeholder="{{ cookiecutter.package_name | slugify }}",
        in_cookiecutter_json=False,
    ),
    # The seed also links to the maintainer's own projects (plugin marketplace,
    # home_secret_toml, docfly) and credits the template's author in
    # AUTHORS.rst. Those must stay literal, so the files that only mention them
    # are excluded from this parameter.
    Parameter(
        selector=[SeedValues.github_username],
        name="github_username",
        default="your_github_username",
        prompt="Your GitHub username, the owner of the new repo",
        exclude=[
            ".claude/settings.local.json.example",
            ".claude/skills/pywf-priv-base/references/01-secrets.md",
            ".claude/skills/pywf-priv-base/references/15-docfly.md",
            "AUTHORS.rst",
        ],
    ),
    # AUTHORS.rst is the template author's bio, kept as is (LEGAL_RESIDUES).
    Parameter(
        selector=[SeedValues.author],
        name="author",
        default="Firstname Lastname",
        prompt="Author name for pyproject.toml file",
        exclude=["AUTHORS.rst"],
    ),
    Parameter(
        selector=[SeedValues.author_email],
        name="author_email",
        default="firstname.lastname@email.com",
        prompt="Author email for pyproject.toml file",
    ),
    # Generic value: only the project license field in pyproject.toml. A text
    # variable; LICENSE.txt is always the proprietary one (hooks/post_gen_project.py).
    Parameter(
        selector=[f'license = "{SeedValues.license}"', SeedValues.license],
        name="license",
        default=SeedValues.license,
        prompt="SPDX license expression for pyproject.toml (e.g. LicenseRef-Proprietary)",
        include=["pyproject.toml"],
    ),
    # Generic value: only the project version line in pyproject.toml.
    Parameter(
        selector=[f'version = "{SeedValues.version}"', SeedValues.version],
        name="version",
        default="0.1.1",
        prompt="Semantic Version, in {major}.{minor}.{micro} (e.g. 0.1.1)",
        include=["pyproject.toml"],
    ),
    # Generic value: the dev Python pin in mise.toml, and the CI jobs that
    # must match it. One variable, four contexts; only the first one goes into
    # cookiecutter.json. The comment next to the CI matrix quotes the
    # mise.toml line, so the first context matches it as well.
    Parameter(
        selector=[f'python = "{_PY}"', _PY],
        name="dev_python_version",
        default=_PY,
        prompt=f"Python version for local development, in {{major}}.{{minor}} (e.g. {_PY})",
        include=["mise.toml", ".github/workflows/main.yml"],
    ),
    Parameter(
        selector=[f'python-version: ["{_PY}"]', _PY],
        name="dev_python_version_ci_matrix",
        custom_placeholder="{{ cookiecutter.dev_python_version }}",
        in_cookiecutter_json=False,
        include=[".github/workflows/main.yml"],
    ),
    Parameter(
        selector=[f'python-version: "{_PY}"', _PY],
        name="dev_python_version_ci_setup",
        custom_placeholder="{{ cookiecutter.dev_python_version }}",
        in_cookiecutter_json=False,
        include=[".github/workflows/main.yml"],
    ),
    Parameter(
        selector=[f"Setup Python {_PY}", _PY],
        name="dev_python_version_ci_step",
        custom_placeholder="{{ cookiecutter.dev_python_version }}",
        in_cookiecutter_json=False,
        include=[".github/workflows/main.yml"],
    ),
    Parameter(
        selector=[SeedValues.github_token_field],
        name="github_token_field",
        default="your_github_token_field",
        prompt=f"GitHub token field path in home_secret.toml, {_HOME_SECRET_HELP}",
    ),
    Parameter(
        selector=[SeedValues.cloudflare_token_field],
        name="cloudflare_token_field",
        default="your_cloudflare_token_field",
        prompt=f"Cloudflare API token field path in home_secret.toml, {_HOME_SECRET_HELP}",
    ),
    # The two profiles have the same value in the seed: each one only in its
    # own mise.toml line.
    Parameter(
        selector=[
            f'AWS_CODEARTIFACT_PROFILE = "{SeedValues.aws_codeartifact_profile}"',
            SeedValues.aws_codeartifact_profile,
        ],
        name="aws_codeartifact_profile",
        default="your_aws_codeartifact_profile",
        prompt="AWS CLI profile for publishing package to AWS CodeArtifact",
        include=["mise.toml"],
    ),
    Parameter(
        selector=[
            f'DOC_HOST_AWS_PROFILE = "{SeedValues.doc_host_aws_profile}"',
            SeedValues.doc_host_aws_profile,
        ],
        name="doc_host_aws_profile",
        default="your_doc_host_aws_profile",
        prompt="AWS CLI profile for deploying documentation to AWS S3",
        include=["mise.toml"],
    ),
    Parameter(
        selector=[SeedValues.doc_host_s3_bucket],
        name="doc_host_s3_bucket",
        default="your_doc_host_s3_bucket",
        prompt="AWS S3 bucket for storing versioned documentation",
    ),
    # Generic value ("esc" is a common substring): only these contexts. The
    # longer seed values that contain it (bucket, repository, token field,
    # OIDC role, the demo private package) are matched as a whole first.
    # A context never includes another seed value (e.g. the account id next
    # to it): replaced text is never replaced again.
    Parameter(
        selector=[f'AWS_CODEARTIFACT_DOMAIN = "{_DOMAIN}"', _DOMAIN],
        name="aws_codeartifact_domain",
        default="your_aws_codeartifact_domain",
        prompt="AWS CodeArtifact domain name",
    ),
    Parameter(
        selector=[f"--domain {_DOMAIN} ", _DOMAIN],
        name="aws_codeartifact_domain_cli",
        custom_placeholder="{{ cookiecutter.aws_codeartifact_domain }}",
        in_cookiecutter_json=False,
    ),
    Parameter(
        selector=[f"/{_DOMAIN}/r/", _DOMAIN],
        name="aws_codeartifact_domain_console",
        custom_placeholder="{{ cookiecutter.aws_codeartifact_domain }}",
        in_cookiecutter_json=False,
    ),
    Parameter(
        selector=[f"https://{_DOMAIN}-", _DOMAIN],
        name="aws_codeartifact_domain_url",
        custom_placeholder="{{ cookiecutter.aws_codeartifact_domain }}",
        in_cookiecutter_json=False,
    ),
    # uv index name, in [[tool.uv.index]] and [tool.uv.sources]
    Parameter(
        selector=[f'name = "{_DOMAIN}"', _DOMAIN],
        name="aws_codeartifact_domain_uv_index",
        custom_placeholder="{{ cookiecutter.aws_codeartifact_domain }}",
        in_cookiecutter_json=False,
        include=["pyproject.toml", "README.rst"],
    ),
    Parameter(
        selector=[f'index = "{_DOMAIN}"', _DOMAIN],
        name="aws_codeartifact_domain_uv_source",
        custom_placeholder="{{ cookiecutter.aws_codeartifact_domain }}",
        in_cookiecutter_json=False,
        include=["pyproject.toml", "README.rst"],
    ),
    Parameter(
        selector=[f"UV_INDEX_{_DOMAIN_ENV}_", _DOMAIN_ENV],
        name="aws_codeartifact_domain_uv_env",
        custom_placeholder="{{ cookiecutter.aws_codeartifact_domain | upper | replace('-', '_') }}",
        in_cookiecutter_json=False,
    ),
    Parameter(
        selector=[SeedValues.aws_codeartifact_repository],
        name="aws_codeartifact_repository",
        default="your_aws_codeartifact_repository",
        prompt="AWS CodeArtifact Python repository name",
    ),
    Parameter(
        selector=[SeedValues.aws_account_id],
        name="aws_account_id",
        default="111122223333",
        prompt="Your 12 digits AWS Account Id where you put your CodeArtifact domain, e.g. 111122223333",
    ),
    # Generic value: only these contexts.
    Parameter(
        selector=[f'AWS_CODEARTIFACT_REGION = "{_REGION}"', _REGION],
        name="aws_region",
        default=_REGION,
        prompt=f"Your AWS CodeArtifact region name, e.g. {_REGION}",
    ),
    Parameter(
        selector=[f".codeartifact.{_REGION}.amazonaws.com", _REGION],
        name="aws_region_url",
        custom_placeholder="{{ cookiecutter.aws_region }}",
        in_cookiecutter_json=False,
    ),
    Parameter(
        selector=[f"https://{_REGION}.console.aws.amazon.com", _REGION],
        name="aws_region_console",
        custom_placeholder="{{ cookiecutter.aws_region }}",
        in_cookiecutter_json=False,
    ),
    Parameter(
        selector=[f"?region={_REGION}", _REGION],
        name="aws_region_console_query",
        custom_placeholder="{{ cookiecutter.aws_region }}",
        in_cookiecutter_json=False,
    ),
    Parameter(
        selector=[f"aws-region: {_REGION}", _REGION],
        name="aws_region_ci",
        custom_placeholder="{{ cookiecutter.aws_region }}",
        in_cookiecutter_json=False,
        include=[".github/workflows/main.yml"],
    ),
    Parameter(
        selector=[SeedValues.aws_github_oidc_role_name],
        name="aws_github_oidc_role_name",
        default="your_aws_github_oidc_role_name",
        prompt="IAM role name that GitHub Actions assumes through OIDC to read AWS CodeArtifact (role/<name> in .github/workflows/main.yml)",
    ),
]

# Git-visible seed files that must not enter the template.
EXCLUDE = [
    "LICENSE.txt",  # generated by hooks/post_gen_project.py
    "uv.lock",  # carries the seed's own package name; generated projects re-lock
    # Seed-only maintenance files: the seed's own changelog and the skill that
    # writes it (02-repo-layout.md, "seed repo").
    "release-history-seed-repo.rst",
    ".claude/skills/pywf-priv-changelog-seed-repo/",
]

# Seed files whose links pin the seed's own version tag (blob/<version>/...).
# check-version requires every pinned version to equal the seed version, so a
# version bump cannot leave them behind (08-versioning-and-release.md).
SEED_VERSION_PIN_FILES: list[str] = []

# Files copied byte for byte (no variable replacement).
NO_RENDER = [
    "*/vendor/**/*.*",
    "requirements.txt",
    "requirements-dev.txt",
    "requirements-doc.txt",
    "requirements-mise.txt",
    "requirements-test.txt",
    "*.jinja",
    "*.j2",
    "*.html",
]

# Choice variables whose values send hooks or the template down different
# branches. test-template generates once per extra choice value
# (03-parameterization.md, "Choice Coverage"). There is no choice variable.
CHOICE_COVERAGE: list[str] = []

# Files the hooks create or rewrite in a generated project. check-roundtrip
# allows them to differ from the seed.
HOOK_OUTPUTS = [
    "LICENSE.txt",  # hooks/post_gen_project.py writes it with the current year
]

# Seed values unique enough that any occurrence left in the template is a
# leak, scanned by check-seed-values. Generic values (license, version,
# dev_python_version, aws_codeartifact_domain, aws_region) also appear
# legitimately elsewhere; check-roundtrip verifies them instead.
UNIQUE_SEED_VALUES = {
    "package_name": SeedValues.package_name,
    "package_name_slug": SeedValues.package_name_slug,
    "github_username": SeedValues.github_username,
    "pypi_username": SeedValues.pypi_username,
    "author": SeedValues.author,
    "author_email": SeedValues.author_email,
    "github_token_field": SeedValues.github_token_field,
    "cloudflare_token_field": SeedValues.cloudflare_token_field,
    "aws_codeartifact_profile": SeedValues.aws_codeartifact_profile,
    "doc_host_s3_bucket": SeedValues.doc_host_s3_bucket,
    "aws_codeartifact_repository": SeedValues.aws_codeartifact_repository,
    "aws_account_id": SeedValues.aws_account_id,
    "aws_github_oidc_role_name": SeedValues.aws_github_oidc_role_name,
    "aws_codeartifact_domain_uv_env": f"UV_INDEX_{_DOMAIN_ENV}_",
}

_MAINTAINER_LINK = "links to the maintainer's own project, must stay literal"
_TEMPLATE_AUTHOR = "credits the template's author, not the generated project's"

# Unique seed values that may legally remain in the template, consumed by
# check-seed-values. Each entry: (seed value name, template-relative file, reason).
LEGAL_RESIDUES: list[tuple[str, str, str]] = [
    ("github_username", ".claude/settings.local.json.example", _MAINTAINER_LINK),
    ("github_username", ".claude/skills/pywf-priv-base/references/01-secrets.md", _MAINTAINER_LINK),
    ("github_username", ".claude/skills/pywf-priv-base/references/15-docfly.md", _MAINTAINER_LINK),
    ("github_username", "AUTHORS.rst", _TEMPLATE_AUTHOR),
    ("pypi_username", "AUTHORS.rst", _TEMPLATE_AUTHOR),
    ("author", "AUTHORS.rst", _TEMPLATE_AUTHOR),
]


def get_seed_context() -> dict[str, str]:
    """
    The cookiecutter context that renders the template back into the seed.
    """
    return {
        p.name: getattr(SeedValues, p.name)
        for p in PARAMETERS
        if p.in_cookiecutter_json
    }


def add_template_version(path_json) -> None:
    """
    Record the shared version (the seed's) as the private variable
    ``_template_version``: cookiecutter never prompts for it, but it is part of
    every generation's context. It goes right after the last prompted variable.
    """
    data = json.loads(path_json.read_text(encoding="utf-8"))
    result = {}
    for key, value in data.items():
        if key.startswith("_") and "_template_version" not in result:
            result["_template_version"] = cctpl.get_seed_version()
        result[key] = value
    path_json.write_text(json.dumps(result, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    dir_stage_seed = cctpl.dir_stage / dir_seed.name
    cctpl.reset_dir(cctpl.dir_stage)
    n_files = cctpl.stage_git_visible_files(dir_seed, dir_stage_seed)
    print(f"Staged {n_files} git-visible files from {dir_seed}")

    if cctpl.dir_template.exists():
        cctpl.reset_dir(cctpl.dir_template)
        cctpl.dir_template.rmdir()
    maker = Maker(
        dir_input=dir_stage_seed,
        dir_output=cctpl.dir_template,
        parameters=PARAMETERS,
        exclude=EXCLUDE,
        no_render=NO_RENDER,
        dir_hooks=cctpl.dir_project_root / "hooks",
        verbose=False,
    )
    maker.make_template()
    add_template_version(maker.path_cookiecutter_json)
    print(f"Template written to {cctpl.dir_template}")
    return 0


if __name__ == "__main__":
    cctpl.run_task(main)
