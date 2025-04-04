# -*- coding: utf-8 -*-

"""
Convert a seed repo into a project template.
"""

import shutil
from pathlib import Path
from cookiecutter_maker.api import Parameter, Maker

# Get the current directory and create a temporary directory for output
dir_here: Path = Path(__file__).absolute().parent
dir_tmp = dir_here.joinpath("tmp")

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
                'version = "0.1.1"',
                "0.1.1",
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
        Parameter(
            selector=["sanhe-dev"],
            name="token_name",
            default="your_github_codecov_cloudflare_token_name",
            prompt=(
                "Your GitHub token, codecov token and cloudflare token name (better to be the same name), "
                "if you want to automatically setup CI/CD for your project"
            ),
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
            selector=['aws_codeartifact_profile = "esc_app_devops_us_east_1"', "esc_app_devops_us_east_1"],
            name="aws_codeartifact_profile",
            default="your_aws_codeartifact_profile",
            prompt="AWS CLI profile for publishing package to AWS CodeArtifact, e.g. your_aws_codeartifact_profile",
        ),
        Parameter(
            selector=['aws_codeartifact_domain = "esc"', "esc"],
            name="aws_codeartifact_domain",
            default="your_aws_codeartifact_domain",
            prompt="AWS CodeArtifact domain name",
        ),
        Parameter(
            selector=["/esc/r/", "esc"],
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
            selector=["esc-python/p/pypi/", "esc-python"],
            name="aws_codeartifact_repository",
            default="your_aws_codeartifact_repository",
            prompt="AWS CodeArtifact Python repository name",
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
            selector=['cloudflare_account_alias = "esc"', "esc"],
            name="cloudflare_account_alias",
            default="your_cloudflare_account_alias",
            prompt="Your cloudflare account alias, we need this to locate the token file",
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
        ".poetry",
        "tmp",
        "bin/pywf_internal_proprietary",
        "docs/source/cookiecutter_pywf_internal_proprietary_demo",
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
