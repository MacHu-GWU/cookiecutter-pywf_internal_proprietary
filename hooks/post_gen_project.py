# -*- coding: utf-8 -*-

"""
Write LICENSE.txt. The template is for closed source projects, so it is
always the proprietary license, whatever the SPDX expression in ``license``,
with the current year and the project's author.
"""

from pathlib import Path

dir_project_root = Path.cwd()

proprietary_license = """
Copyright (c) {% now 'utc', '%Y' %} {{ cookiecutter.author }} <{{ cookiecutter.author_email }}>

All rights reserved.

This software is proprietary and confidential. Unauthorized copying, modification, distribution, or use of this software, in whole or in part, is strictly prohibited unless prior written permission is obtained from the copyright holder.

This software is provided "as is" without warranty of any kind, either express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement.

For licensing inquiries or commercial use, please contact: {{ cookiecutter.author }} <{{ cookiecutter.author_email }}>.
"""

dir_project_root.joinpath("LICENSE.txt").write_text(proprietary_license, encoding="utf-8")
