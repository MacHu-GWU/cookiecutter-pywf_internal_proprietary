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

args = [
    "git", "add", "."
]
subprocess.run(args, cwd=dir_here, check=True)
args = ["git", "commit", "-m", "update template"]
subprocess.run(args, cwd=dir_here, check=True)