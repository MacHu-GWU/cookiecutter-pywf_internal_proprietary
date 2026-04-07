# -*- coding: utf-8 -*-

"""
Remove a specific version of a Python package from AWS CodeArtifact.

This script:
1. Reads the package name and version from pyproject.toml
2. Prompts for confirmation before deletion
3. Calls AWS CLI to delete the package version

Required environment variables (set in mise.toml):
- AWS_CODEARTIFACT_PROFILE: AWS profile with CodeArtifact permissions
- AWS_CODEARTIFACT_DOMAIN: CodeArtifact domain name
- AWS_CODEARTIFACT_DOMAIN_OWNER: AWS account ID owning the domain
- AWS_CODEARTIFACT_REPO: CodeArtifact repository name

WARNING: This operation is irreversible. If you re-publish with the same version,
invalidate the uv/pip cache first to avoid stale resolution.
"""

# ------------------------------------------------------------------------------
# Environment Variable Names
# ------------------------------------------------------------------------------
ENV_AWS_CODEARTIFACT_PROFILE = "AWS_CODEARTIFACT_PROFILE"
ENV_AWS_CODEARTIFACT_DOMAIN = "AWS_CODEARTIFACT_DOMAIN"
ENV_AWS_CODEARTIFACT_DOMAIN_OWNER = "AWS_CODEARTIFACT_DOMAIN_OWNER"
ENV_AWS_CODEARTIFACT_REPO = "AWS_CODEARTIFACT_REPO"

import os
import sys
import subprocess

from utils import config


def main():
    profile = os.environ.get(ENV_AWS_CODEARTIFACT_PROFILE)
    domain = os.environ.get(ENV_AWS_CODEARTIFACT_DOMAIN)
    domain_owner = os.environ.get(ENV_AWS_CODEARTIFACT_DOMAIN_OWNER)
    repo = os.environ.get(ENV_AWS_CODEARTIFACT_REPO)

    for name, value in [
        (ENV_AWS_CODEARTIFACT_PROFILE, profile),
        (ENV_AWS_CODEARTIFACT_DOMAIN, domain),
        (ENV_AWS_CODEARTIFACT_DOMAIN_OWNER, domain_owner),
        (ENV_AWS_CODEARTIFACT_REPO, repo),
    ]:
        if not value:
            print(f"Error: {name} environment variable not set")
            sys.exit(1)

    package = config.readthedocs_slug  # e.g. {{ cookiecutter.package_name | slugify }}
    version = config.pyproject_data["project"]["version"]

    console_url = (
        f"https://{{ cookiecutter.aws_region }}.console.aws.amazon.com/codesuite/codeartifact/d"
        f"/{domain_owner}/{domain}/r/{repo}/p/pypi/{package}/versions"
    )
    print(f"Package : {package}")
    print(f"Version : {version}")
    print(f"Domain  : {domain} (owner: {domain_owner})")
    print(f"Repo    : {repo}")
    print(f"Preview : {console_url}")
    print()

    answer = input(
        f"Are you sure you want to remove {package!r} version {version!r} "
        f"from AWS CodeArtifact? (Y/N): "
    )
    if answer != "Y":
        print("Aborted.")
        sys.exit(0)

    try:
        subprocess.run(
            [
                "aws", "codeartifact", "delete-package-versions",
                "--profile", profile,
                "--domain", domain,
                "--domain-owner", domain_owner,
                "--repository", repo,
                "--format", "pypi",
                "--package", package,
                "--versions", version,
                "--expected-status", "Published",
            ],
            check=True,
        )
        print(f"✅ Removed {package!r} version {version!r} from AWS CodeArtifact")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to delete package version")
        print(f"Details: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
