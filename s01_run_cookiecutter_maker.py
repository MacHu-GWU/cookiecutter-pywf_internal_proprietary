# -*- coding: utf-8 -*-

"""
Convert a seed repo into a project template.
"""

import sys
import shutil
import subprocess
from pathlib import Path
from cookiecutter_maker.api import Parameter, Maker

# Get the current directory and create a temporary directory for output
dir_here: Path = Path(__file__).absolute().parent
dir_tmp = dir_here.joinpath("tmp")
dir_seed = Path.home().joinpath(
    "Documents",
    "GitHub",
    "cookiecutter_pywf_internal_proprietary_demo-project",
)

# Extract the current version from the seed project to use as a placeholder
path_version = dir_seed / "cookiecutter_pywf_internal_proprietary_demo" / "_version.py"
args = [sys.executable, str(path_version)]
result = subprocess.run(args, capture_output=True)
version_to_replace = result.stdout.decode("utf-8").strip()
versions = version_to_replace.split(".")
assert len(versions) == 3
assert all(v.isdigit() for v in versions)

# Create a Maker instance to convert the project into a template
maker = Maker(
    # The input concrete project directory - the seed project you want to templatize
    dir_input=Path.home().joinpath(
        "Documents",
        "GitHub",
        "cookiecutter_pywf_internal_proprietary_demo-project",
    ),
    # The output template directory - where the generated template will be placed
    dir_output=dir_tmp,
    # Define parameters that will be customizable in the generated template
    parameters=[
        Parameter(
            selector=["cookiecutter_pywf_internal_proprietary_demo"],
            name="package_name",
            default="your_package_name",
            prompt="Your Python package name, in snake case (e.g. my_package)",
        ),
        Parameter(
            selector=["cookiecutter-pywf-internal-proprietary-demo"],
            name="package_name_slug",
            default="your-package-name",
            custom_placeholder="{{ cookiecutter.package_name | slugify }}",
            in_cookiecutter_json=False,
        ),
        Parameter(
            selector=["MacHu-GWU"],
            name="github_username",
            default="your_github_username",
        ),
        Parameter(
            selector=["Sanhe Hu"],
            name="author",
            default="Firstname Lastname",
            prompt="Author name for pyproject.toml file",
        ),
        Parameter(
            selector=["husanhe@gmail.com"],
            name="author_email",
            default="firstname.lastname@email.com",
            prompt="Author email for pyproject.toml file",
        ),
        Parameter(
            selector=[
                f'version = "{version_to_replace}"',
                f"{version_to_replace}",
            ],
            name="version",
            default="0.1.1",
            prompt="Semantic Version, in {major}.{minor}.{micro} (e.g. 0.1.1)",
        ),
        Parameter(
            selector=['dev_python = "3.11.8"', "3.11.8"],
            name="dev_python_version",
            default="3.11.8",
            prompt="Python version for local development, in {major}.{minor}.{micro} (e.g. 3.11.8)",
        ),
        # has to substitute value that may have aws_region as part of
        # the naming convention before substitute the aws_region
        Parameter(
            selector=['aws_codeartifact_profile = "esc_app_devops_us_east_1"', "esc_app_devops_us_east_1"],
            name="aws_codeartifact_profile",
            default="your_aws_codeartifact_profile",
            prompt="AWS CLI profile for publishing package to AWS CodeArtifact, e.g. your_aws_codeartifact_profile",
        ),
        Parameter(
            selector=['doc_host_aws_profile = "esc_app_devops_us_east_1"', "esc_app_devops_us_east_1"],
            name="doc_host_aws_profile",
            default="your_doc_host_aws_profile",
            prompt="AWS CLI profile for publishing document website to AWS S3 bucket, e.g. your_doc_host_aws_profile",
        ),
        Parameter(
            selector=["esc-app-devops-us-east-1-doc-host"],
            name="doc_host_s3_bucket",
            default="your_doc_host_s3_bucket",
            prompt="AWS S3 Bucket to store document site historical versions",
        ),
        Parameter(
            selector=["us-east-1"],
            name="aws_region",
            default="us-east-1",
            prompt="Your AWS CodeArtifact region name, e.g. us-east-1",
        ),
        Parameter(
            selector=["982534387049"],
            name="aws_account_id",
            default="111122223333",
            prompt="Your 12 digits AWS Account Id where you put your CodeArtifact domain, e.g. 111122223333",
        ),
        Parameter(
            selector=['aws_codeartifact_domain = "esc"', "esc"],
            name="aws_codeartifact_domain",
            default="your_aws_codeartifact_domain",
            prompt="AWS CodeArtifact domain name",
        ),
        Parameter(
            selector=['name = "esc"', "esc"],
            name="aws_codeartifact_domain",
            default="your_aws_codeartifact_domain",
            prompt="AWS CodeArtifact domain name",
        ),
        Parameter(
            selector=["https://esc", "esc"],
            name="aws_codeartifact_domain",
            default="your_aws_codeartifact_domain",
            prompt="AWS CodeArtifact domain name",
        ),
        Parameter(
            selector=['aws_codeartifact_repository = "esc-python"', "esc-python"],
            name="aws_codeartifact_repository",
            default="your_aws_codeartifact_repository",
            prompt="AWS CodeArtifact Python repository name",
        ),
        Parameter(
            selector=["pypi/esc-python/simple", "esc-python"],
            name="aws_codeartifact_repository",
            default="your_aws_codeartifact_repository",
            prompt="AWS CodeArtifact Python repository name",
        ),
        Parameter(
            selector=["providers.github.accounts.sh.users.sh.secrets.dev.value"],
            name="github_token_field",
            default="your_github_token_field",
            prompt="GitHub token field, Read https://github.com/MacHu-GWU/home_secret-project to learn how to set up your GitHub token using home_secret.json",
        ),
        Parameter(
            selector=["providers.codecov_io.accounts.sh.users.sh.secrets.dev.value"],
            name="codecov_token_field",
            default="your_codecov_token_field",
            prompt="Codecov.io token field, Read https://github.com/MacHu-GWU/home_secret-project to learn how to set up your GitHub token using home_secret.json",
        ),
        Parameter(
            selector=["providers.cloudflare.accounts.esc.users.sh_esc.secrets.cloudflare_pages_upload.value"],
            name="cloudflare_token_field",
            default="your_cloudflare_token_field",
            prompt="Your cloudflare token, , Read https://github.com/MacHu-GWU/home_secret-project to learn how to set up your GitHub token using home_secret.json",
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
        "build",  # Build artifacts
        "dist",  # Distribution packages
        "htmlcov",  # HTML coverage reports
        "__pycache__",  # Python cache files
        ".poetry", # Poetry cache
        ".wrangler",  # Cloudflare Wrangler cache
        "tmp",
        "bin/pywf_internal_proprietary",
        "docs/source/api",
        # file
        ".coverage",  # Coverage data
        ".pyc",  # Compiled Python files
    ],
    # Files that should be copied without rendering (processing)
    # Useful for files that contain syntax that conflicts with Jinja2
    # For example, template files that already use {{ }} syntax
    no_render=[
        # dir
        "*/vendor/**/*.*",
        # file
        "poetry.lock",
        "uv.lock",
        "requirements.txt",
        "requirements-automation.txt",
        "requirements-dev.txt",
        "requirements-doc.txt",
        "requirements-test.txt",
        "requirements-poetry.txt",
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
