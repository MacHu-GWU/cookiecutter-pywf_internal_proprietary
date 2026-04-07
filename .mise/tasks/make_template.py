# -*- coding: utf-8 -*-

"""
Convert a seed repo into a project template.
"""

import shutil
import tomllib
from pathlib import Path
from cookiecutter_maker.api import Parameter, Maker
from cookiecutter_pywf_internal_proprietary.paths import path_enum

# Get the project root directory
dir_tmp = path_enum.dir_tmp
dir_seed = Path.home().joinpath(
    "Documents",
    "GitHub",
    "cookiecutter_pywf_internal_proprietary_demo-project",
)

# Extract dynamic values from the seed project
with open(dir_seed / "pyproject.toml", "rb") as f:
    _pyproject = tomllib.load(f)
with open(dir_seed / "mise.toml", "rb") as f:
    _mise_config = tomllib.load(f)


class SeedValues:
    """Concrete values in the seed project that need to be reverse-replaced."""

    # --- identity ---
    package_name = "cookiecutter_pywf_internal_proprietary_demo"
    package_name_slug = "cookiecutter-pywf-internal-proprietary-demo"
    github_username = "MacHu-GWU"

    # --- license ---
    license = "LicenseRef-Proprietary"

    # --- author ---
    author = "Sanhe Hu"
    author_email = "husanhe@gmail.com"

    # --- versioning (dynamic) ---
    version = _pyproject["project"]["version"]
    dev_python_version = _mise_config["tools"]["python"]

    # --- secret token fields ---
    github_token_field = "github.accounts.sh.users.sh.secrets.dev.value"
    cloudflare_token_field = "cloudflare.accounts.esc.users.sh_esc.secrets.cloudflare_pages_upload.value"

    # --- AWS ---
    aws_account_id = "982534387049"
    aws_region = "us-east-1"
    aws_codeartifact_profile = "esc_app_devops_us_east_1"
    aws_codeartifact_domain = "esc"
    aws_codeartifact_repository = "esc-python"
    doc_host_aws_profile = "esc_app_devops_us_east_1"
    doc_host_s3_bucket = "esc-app-devops-us-east-1-doc-host"


# Validate version format
_parts = SeedValues.version.split(".")
assert len(_parts) == 3 and all(v.isdigit() for v in _parts), (
    f"Invalid version: {SeedValues.version}"
)

# For backward compatibility (publish-template.py imports this)
version_to_replace = SeedValues.version

# Create a Maker instance to convert the project into a template
maker = Maker(
    # The input concrete project directory - the seed project you want to templatize
    dir_input=dir_seed,
    # The output template directory - where the generated template will be placed
    dir_output=dir_tmp,
    # Define parameters that will be customizable in the generated template
    parameters=[
        Parameter(
            selector=[SeedValues.package_name],
            name="package_name",
            default="your_package_name",
            prompt="Your Python package name, in snake case (e.g. my_package)",
        ),
        Parameter(
            selector=[SeedValues.package_name_slug],
            name="package_name_slug",
            default="your-package-name",
            custom_placeholder="{{ cookiecutter.package_name | slugify }}",
            in_cookiecutter_json=False,
        ),
        Parameter(
            selector=[SeedValues.github_username],
            name="github_username",
            default="your_github_username",
        ),
        Parameter(
            selector=[SeedValues.author],
            name="author",
            default="Firstname Lastname",
            prompt="Author name for pyproject.toml file",
        ),
        Parameter(
            selector=[SeedValues.author_email],
            name="author_email",
            default="firstname.lastname@email.com",
            prompt="Author email for pyproject.toml file",
        ),
        Parameter(
            selector=[f'license = "{SeedValues.license}"', SeedValues.license],
            name="license",
            default="LicenseRef-Proprietary",
            prompt="SPDX license expression for pyproject.toml (e.g. LicenseRef-Proprietary)",
        ),
        Parameter(
            selector=[
                f'version = "{SeedValues.version}"',
                SeedValues.version,
            ],
            name="version",
            default="0.1.1",
            prompt="Semantic Version, in {major}.{minor}.{micro} (e.g. 0.1.1)",
        ),
        Parameter(
            selector=[
                f'__version__ = "{SeedValues.version}"',
                SeedValues.version,
            ],
            name="version",
            default="0.1.1",
            prompt="Semantic Version, in {major}.{minor}.{micro} (e.g. 0.1.1)",
        ),
        Parameter(
            selector=[
                f'python = "{SeedValues.dev_python_version}"',
                SeedValues.dev_python_version,
            ],
            name="dev_python_version",
            default=SeedValues.dev_python_version,
            prompt=f"Python version for local development, in {{major}}.{{minor}} (e.g. {SeedValues.dev_python_version})",
        ),
        Parameter(
            selector=[SeedValues.github_token_field],
            name="github_token_field",
            default="your_github_token_field",
            prompt="GitHub token field path in home_secret.toml, see https://github.com/MacHu-GWU/home_secret_toml-project",
        ),
        Parameter(
            selector=[SeedValues.cloudflare_token_field],
            name="cloudflare_token_field",
            default="your_cloudflare_token_field",
            prompt="Cloudflare API token field path in home_secret.toml, see https://github.com/MacHu-GWU/home_secret_toml-project",
        ),
        # NOTE: substitute longer/more-specific strings that contain aws_region
        # before substituting aws_region itself, to avoid partial replacements.
        Parameter(
            selector=[
                f'AWS_CODEARTIFACT_PROFILE = "{SeedValues.aws_codeartifact_profile}"',
                SeedValues.aws_codeartifact_profile,
            ],
            name="aws_codeartifact_profile",
            default="your_aws_codeartifact_profile",
            prompt="AWS CLI profile for publishing package to AWS CodeArtifact",
        ),
        Parameter(
            selector=[
                f'DOC_HOST_AWS_PROFILE = "{SeedValues.doc_host_aws_profile}"',
                SeedValues.doc_host_aws_profile,
            ],
            name="doc_host_aws_profile",
            default="your_doc_host_aws_profile",
            prompt="AWS CLI profile for deploying documentation to AWS S3",
        ),
        Parameter(
            selector=[SeedValues.doc_host_s3_bucket],
            name="doc_host_s3_bucket",
            default="your_doc_host_s3_bucket",
            prompt="AWS S3 bucket for storing versioned documentation",
        ),
        # NOTE: substitute aws_codeartifact_domain before aws_region,
        # because domain names like "esc" may appear inside region-derived strings.
        Parameter(
            selector=[
                f'AWS_CODEARTIFACT_DOMAIN = "{SeedValues.aws_codeartifact_domain}"',
                SeedValues.aws_codeartifact_domain,
            ],
            name="aws_codeartifact_domain",
            default="your_aws_codeartifact_domain",
            prompt="AWS CodeArtifact domain name",
        ),
        Parameter(
            selector=[
                f'name = "{SeedValues.aws_codeartifact_domain}"',
                SeedValues.aws_codeartifact_domain,
            ],
            name="aws_codeartifact_domain",
            default="your_aws_codeartifact_domain",
            prompt="AWS CodeArtifact domain name",
        ),
        Parameter(
            selector=[
                f"https://{SeedValues.aws_codeartifact_domain}",
                SeedValues.aws_codeartifact_domain,
            ],
            name="aws_codeartifact_domain",
            default="your_aws_codeartifact_domain",
            prompt="AWS CodeArtifact domain name",
        ),
        Parameter(
            selector=[
                f"/{SeedValues.aws_codeartifact_domain}/r/",
                SeedValues.aws_codeartifact_domain,
            ],
            name="aws_codeartifact_domain",
            default="your_aws_codeartifact_domain",
            prompt="AWS CodeArtifact domain name",
        ),
        Parameter(
            selector=[
                f'AWS_CODEARTIFACT_REPO = "{SeedValues.aws_codeartifact_repository}"',
                SeedValues.aws_codeartifact_repository,
            ],
            name="aws_codeartifact_repository",
            default="your_aws_codeartifact_repository",
            prompt="AWS CodeArtifact Python repository name",
        ),
        Parameter(
            selector=[
                f"pypi/{SeedValues.aws_codeartifact_repository}/simple",
                SeedValues.aws_codeartifact_repository,
            ],
            name="aws_codeartifact_repository",
            default="your_aws_codeartifact_repository",
            prompt="AWS CodeArtifact Python repository name",
        ),
        Parameter(
            selector=[
                f"r/{SeedValues.aws_codeartifact_repository}/p/pypi",
                SeedValues.aws_codeartifact_repository,
            ],
            name="aws_codeartifact_repository",
            default="your_aws_codeartifact_repository",
            prompt="AWS CodeArtifact Python repository name",
        ),
        Parameter(
            selector=[SeedValues.aws_account_id],
            name="aws_account_id",
            default="111122223333",
            prompt="12-digit AWS account ID where your CodeArtifact domain lives (e.g. 111122223333)",
        ),
        Parameter(
            selector=[SeedValues.aws_region],
            name="aws_region",
            default="us-east-1",
            prompt="AWS region for CodeArtifact and S3 doc hosting (e.g. us-east-1)",
        ),
    ],
    # Define which files/directories to include in the template
    # Empty list means include everything not explicitly excluded
    # You can use patterns like "**/*.py" to include all Python files
    # The rule is 'explicit exclude' > 'explicit include' > 'default include'
    include=[],
    # define what to exclude in the input directory
    # Define which files/directories to exclude from the template
    exclude=[
        # dir
        ".git",  # Git repository data
        ".venv",  # Virtual environment
        ".pytest_cache",  # Test cache
        ".idea",  # PyCharm stuff
        ".wrangler",  # Cloudflare Wrangler cache
        "build",  # Build artifacts
        "dist",  # Distribution packages
        "htmlcov",  # HTML coverage reports
        "__pycache__",  # Python cache files
        "tmp",
        "docs/source/api",  # Auto-generated API reference docs
        f"{SeedValues.package_name}.egg-info",
        # file
        ".claude/claude-code-messages.md",
        ".claude/settings.local.json",
        ".coverage",  # Coverage data
        ".pyc",  # Compiled Python files
        "LICENSE.txt",  # License file, we will generate this later
    ],
    # Files that should be copied without rendering (processing)
    # Useful for files that contain syntax that conflicts with Jinja2
    # For example, template files that already use {{ }} syntax
    no_render=[
        # dir
        "*/vendor/**/*.*",
        # file
        "uv.lock",
        "requirements.txt",
        "requirements-dev.txt",
        "requirements-doc.txt",
        "requirements-mise.txt",
        "requirements-test.txt",
        # template file
        "*.jinja",  # Jinja template files
        "*.j2",  # Alternative Jinja extension
        "*.html",  # HTML files with {{ }} syntax
    ],
    # Print detailed information during processing
    verbose=True,
)

if __name__ == "__main__":
    # Clean up any existing temporary directory
    if dir_tmp.exists():
        shutil.rmtree(dir_tmp)

    # Execute the template generation process
    maker.make_template()

    print("\n" + "=" * 80)
    print("Template generation complete!")
    print(f"The template is available at: {dir_tmp}")
    print("\nTo create a new project from this template, run:")
    print(f"    cookiecutter {dir_tmp}")
    print("=" * 80 + "\n")
