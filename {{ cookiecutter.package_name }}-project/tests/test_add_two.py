# -*- coding: utf-8 -*-

from {{ cookiecutter.package_name }}.add_two import add_two


def test_add_two():
    assert add_two(1, 2) == 3


if __name__ == "__main__":
    from {{ cookiecutter.package_name }}.tests import run_cov_test

    run_cov_test(
        __file__,
        "{{ cookiecutter.package_name }}.add_two",
        preview=False,
    )
