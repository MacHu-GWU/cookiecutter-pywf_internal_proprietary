# -*- coding: utf-8 -*-

help: ## ** Show this help message
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}'


venv-create: ## ** Create Virtual Environment
	~/.pyenv/shims/python ./bin/s01_1_venv_create.py


venv-remove: ## ** Remove Virtual Environment
	~/.pyenv/shims/python ./bin/s01_2_venv_remove.py


poetry-source-add: ## Add AWS CodeArtifact as secondary source in poetry
	python ./bin/s02_0_poetry_source_add.py


poetry-lock: poetry-source-add ## Resolve dependencies using poetry, update poetry.lock file
	~/.pyenv/shims/python ./bin/s02_0_poetry_lock.py


install-root: ## Install Package itself without any dependencies
	~/.pyenv/shims/python ./bin/s02_1_install_only_root.py


install: ## ** Install main dependencies and Package itself
	~/.pyenv/shims/python ./bin/s02_2_install.py


install-dev: ## Install Development Dependencies
	~/.pyenv/shims/python ./bin/s02_3_install_dev.py


install-test: ## Install Test Dependencies
	~/.pyenv/shims/python ./bin/s02_4_install_test.py


install-doc: ## Install Document Dependencies
	~/.pyenv/shims/python ./bin/s02_5_install_doc.py


install-automation: ## Install Dependencies for Automation Script
	~/.pyenv/shims/python ./bin/s02_6_install_automation.py


install-all: ## Install All Dependencies
	~/.pyenv/shims/python ./bin/s02_7_install_all.py


poetry-export: ## Export dependencies to requirements.txt
	~/.pyenv/shims/python ./bin/s02_8_poetry_export.py


test: install install-test test-only ## ** Run test


test-only: ## Run test without checking test dependencies
	~/.pyenv/shims/python ./bin/s03_1_run_unit_test.py


cov: install install-test cov-only ## ** Run code coverage test


cov-only: ## Run code coverage test without checking test dependencies
	~/.pyenv/shims/python ./bin/s03_2_run_cov_test.py


int: install install-test int-only ## ** Run integration test


int-only: ## Run integration test without checking test dependencies
	~/.pyenv/shims/python ./bin/s03_3_run_int_test.py


view-cov: ## View code coverage test report
	~/.pyenv/shims/python ./bin/s03_3_view_cov_result.py


build-doc: install install-doc ## Build documentation website locally
	~/.pyenv/shims/python ./bin/s04_1_build_doc.py


view-doc: ## View documentation website locally
	~/.pyenv/shims/python ./bin/s04_2_view_doc.py


deploy-versioned-doc: install install-doc ## Deploy documentation website to AWS S3 with version
	./.venv/bin/python ./bin/s04_3_deploy_versioned_doc.py


deploy-latest-doc: install install-doc ## Deploy documentation website to AWS S3 as latest version
	./.venv/bin/python ./bin/s04_4_deploy_latest_doc.py


view-latest-doc: install install-doc ## View latest version of documentation website on AWS S3
	./.venv/bin/python ./bin/s04_5_view_latest_doc.py


create-pages-project: ## Create Cloudflare pages project
	./.venv/bin/python ./bin/s04_6_create_cloudflare_pages_project.py


deploy-pages: ## Deploy Cloudflare pages project from docs/build/html folder
	./.venv/bin/python ./bin/s04_7_deploy_cloudflare_pages.py


build: ## Build Python library distribution package
	~/.pyenv/shims/python ./bin/s05_1_build_package.py


publish: build ## Publish Python library to AWS CodeArtifact
	~/.pyenv/shims/python ./bin/s05_2_publish_package.py


remove: ## Remove Python package version from AWS CodeArtifact
	~/.pyenv/shims/python ./bin/s05_3_remove_package_version.py


release: ## Create Github Release using current version
	~/.pyenv/shims/python ./bin/s05_4_create_release.py


setup-codecov: ## Setup Codecov Upload Token in GitHub Action Secrets
	~/.pyenv/shims/python ./bin/s06_1_setup_codecov.py


setup-cloudflare-token: ## Setup Cloudflare Pages Upload Token in GitHub Action Secrets
	./.venv/bin/python ./bin/s06_2_setup_cloudflare_pages_upload_token_on_github.py
