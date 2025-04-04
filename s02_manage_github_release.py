# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
from pathlib import Path

from s01_run_cookiecutter_maker import dir_here

dir_tmp_template = dir_here / "tmp" / "{{ cookiecutter.package_name }}-project"
dir_template = dir_here / "{{ cookiecutter.package_name }}-project"

shutil.rmtree(dir_template, ignore_errors=True)
shutil.copytree(dir_tmp_template, dir_template)


def update_and_push_main():
    args = ["git", "add", "."]
    subprocess.run(args, cwd=dir_here, check=True)

    args = ["git", "commit", "-m", "update template"]
    try:
        subprocess.run(args, cwd=dir_here, check=True)
    except Exception as e:
        print(e)

    args = ["git", "push"]
    subprocess.run(args, cwd=dir_here, check=True)


def merge_and_push_branch(branch_name: str):
    args = ["git", "checkout", branch_name]
    subprocess.run(args, cwd=dir_here, check=True)
    args = ["git", "merge", "main"]
    subprocess.run(args, cwd=dir_here, check=True)
    args = ["git", "push"]
    subprocess.run(args, cwd=dir_here, check=True)


update_and_push_main()
branch_name_list = [
    "esc-sanhe-dev",
    "bmt-sanhe-dev",
]
for branch_name in branch_name_list:
    merge_and_push_branch(branch_name=branch_name)
