# -*- coding: utf-8 -*-

"""
Print AWS CodeArtifact URL after publish.
"""

import os
from utils import config

project_name = config.project_name
version = config.pyproject_data["project"]["version"]

domain = os.environ["AWS_CODEARTIFACT_DOMAIN"]
domain_owner = os.environ["AWS_CODEARTIFACT_DOMAIN_OWNER"]
region = os.environ["AWS_CODEARTIFACT_REGION"]
repo = os.environ["AWS_CODEARTIFACT_REPO"]

package_slug = config.readthedocs_slug  # CodeArtifact uses hyphenated names

codeartifact_url = (
    f"https://{domain}-{domain_owner}.d.codeartifact.{region}.amazonaws.com"
    f"/pypi/{repo}/simple/{project_name}/{version}/"
)
console_url = (
    f"https://{region}.console.aws.amazon.com/codesuite/codeartifact"
    f"/d/{domain_owner}/{domain}/r/{repo}/p/pypi/{package_slug}/v/{version}"
    f"?region={region}"
)

print(f"📦 Will publish to AWS CodeArtifact: {codeartifact_url}")
print(f"🔗 AWS Console: {console_url}")
