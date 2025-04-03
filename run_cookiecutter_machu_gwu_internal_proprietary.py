# -*- coding: utf-8 -*-

"""
"""

import typing as T
import dataclasses
import shutil
from pathlib import Path
from cookiecutter.main import cookiecutter


@dataclasses.dataclass
class Context:
    package_name: str = dataclasses.field()
    github_username: str = dataclasses.field()
    author: str = dataclasses.field()
    author_email: str = dataclasses.field()
    version: str = dataclasses.field()
    dev_python_version: str = dataclasses.field()
    token_name: str = dataclasses.field()
    aws_region: str = dataclasses.field()
    aws_account_id: str = dataclasses.field()
    aws_codeartifact_profile: str = dataclasses.field()
    aws_codeartifact_domain: str = dataclasses.field()
    aws_codeartifact_repository: str = dataclasses.field()
    doc_host_aws_profile: str = dataclasses.field()
    doc_host_s3_bucket: str = dataclasses.field()
    cloudflare_account_alias: str = dataclasses.field()

    # --- Derived
    package_name_slug: str = dataclasses.field(init=False)

    def __post_init__(self):
        self.package_name_slug = self.package_name.replace("_", "-")

    def to_dict(self) -> dict[str, T.Any]:
        return dataclasses.asdict(self)


if __name__ == "__main__":
    context = Context(
        package_name="cookiecutter_pywf_internal_proprietary_demo",
        github_username="MacHu-GWU",
        author="Sanhe Hu",
        author_email="husanhe@gmail.com",
        version="0.1.1",
        dev_python_version="3.11.8",
        token_name="sanhe-dev",
        aws_region="us-east-1",
        aws_account_id="982534387049",
        aws_codeartifact_profile="esc_app_devops_us_east_1",
        aws_codeartifact_domain="esc",
        aws_codeartifact_repository="esc-python",
        doc_host_aws_profile="esc_app_devops_us_east_1",
        doc_host_s3_bucket="esc-app-devops-us-east-1-doc-host",
        cloudflare_account_alias="esc",
    )

    dir_here: Path = Path(__file__).absolute().parent
    dir_output = dir_here.joinpath("tmp")
    if dir_output.exists():
        shutil.rmtree(dir_output)

    cookiecutter(
        template=f"{dir_here}",
        no_input=True,
        extra_context=context.to_dict(),
        output_dir=f"{dir_output}",
    )
