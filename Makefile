.DEFAULT_GOAL := help

include help.mk

export PROJECT := games
export APP := ${PROJECT}
export BUCKET := scrap-db-backups
export DOCKER_SECRETS_ENV_FILE := docker_secrets.env

ENV_FILE := env.sh
ENV_CUSTOM_FILE := env_custom.sh
ENV_SECRETS_FILE := env_secrets.sh
DB_ENV_PROD_FILE := db_env_prod.sh

SHELL := /bin/bash
SOURCE_CMDS := source venv/bin/activate && source $(ENV_FILE) && source $(ENV_CUSTOM_FILE) && source $(ENV_SECRETS_FILE)
CMD_FRONTEND := source $(ENV_FILE) && cd frontend
PYTHON := python3.10

#------------------------------------
# Installation
#------------------------------------
BIN_DIR := /usr/local/bin

SHFMT_VERSION := 3.4.3
SHFMT_PATH := ${BIN_DIR}/shfmt

.PHONY: install-shfmt
## Install shfmt | Installation
install-shfmt:
	sudo curl https://github.com/mvdan/sh/releases/download/v${SHFMT_VERSION}/shfmt_v${SHFMT_VERSION}_linux_amd64 -Lo ${SHFMT_PATH}
	sudo chmod +x ${SHFMT_PATH}

HADOLINT_VERSION := 2.10.0
HADOLINT_PATH := ${BIN_DIR}/hadolint

.PHONY: install-hadolint
## Install hadolint
install-hadolint:
	sudo curl https://github.com/hadolint/hadolint/releases/download/v${HADOLINT_VERSION}/hadolint-Linux-x86_64 -Lo ${HADOLINT_PATH}
	sudo chmod +x ${HADOLINT_PATH}

ACTIONLINT_VERSION := 1.6.13
ACTIONLINT_PATH := ${BIN_DIR}/actionlint
ACTIONLINT_URL := https://github.com/rhysd/actionlint/releases/download/v${ACTIONLINT_VERSION}/actionlint_${ACTIONLINT_VERSION}_linux_amd64.tar.gz
ACTIONLINT_TMP_DIR := $(shell mktemp -d)
ACTIONLINT_ARCHIVE := actionlint.tar.gz

.PHONY: install-actionlint
## Install actionlint
install-actionlint:
	cd ${ACTIONLINT_TMP_DIR} && \
	curl ${ACTIONLINT_URL} -Lo ${ACTIONLINT_ARCHIVE} && \
	tar -xvf ${ACTIONLINT_ARCHIVE} && \
	sudo mv actionlint ${ACTIONLINT_PATH}

.PHONY: install-linters-binaries
## Install linters binaries
install-linters-binaries: install-shfmt install-hadolint install-actionlint

.PHONY: install-deps
## Install dependencies
install-deps: install-linters-binaries
	# Install Python
	sudo apt install ${PYTHON} ${PYTHON}-venv ${PYTHON}-dev -y
	# Install MySQL dependencies
	sudo apt install libmysqlclient-dev -y

.PHONY: create-venv
## Create venv and install requirements
create-venv:
	${PYTHON} -m venv venv
	${SOURCE_CMDS} && \
		pip install -r requirements-dev.txt

.PHONY: create-tox-venv
## Create tox venv and install requirements
create-tox-venv:
	tox -e py-requirements

.PHONY: create-venvs
## Create venv and tox venv and install requirements
create-venvs: create-venv create-tox-venv

.PHONY: yarn-install-locked
## Run yarn install using lockfile
yarn-install-locked:
	${CMD_FRONTEND} && \
	yarn install --immutable

.PHONY: create-db
## Create db
create-db:
	source $(ENV_FILE) && \
	scripts/create_db.sh

.PHONY: load-initial-fixtures
## Load initial fixtures
load-initial-fixtures:
	$(MAKE) manage arguments="loaddata lists"
	$(MAKE) manage arguments="loaddata categories"

.PHONY: bootstrap
## Bootstrap project
bootstrap: install-deps yarn-install-locked create-env-files create-venvs create-db migrate load-initial-fixtures yarn-build

.PHONY: create-env-files
## Create env files
create-env-files: $(ENV_CUSTOM_FILE) $(ENV_SECRETS_FILE) $(DB_ENV_PROD_FILE) $(DOCKER_SECRETS_ENV_FILE)

$(DOCKER_SECRETS_ENV_FILE):
	cp "${DOCKER_SECRETS_ENV_FILE}.tpl" $(DOCKER_SECRETS_ENV_FILE)

$(ENV_CUSTOM_FILE):
	cp $(ENV_CUSTOM_FILE).tpl $(ENV_CUSTOM_FILE)

$(ENV_SECRETS_FILE):
	cp $(ENV_SECRETS_FILE).tpl $(ENV_SECRETS_FILE)

$(DB_ENV_PROD_FILE):
	cp $(DB_ENV_PROD_FILE).tpl $(DB_ENV_PROD_FILE)
#------------------------------------

#------------------------------------
# Scripts
#------------------------------------
.PHONY: pydiatra-script
pydiatra-script:
	scripts/pydiatra.sh

.PHONY: backup-db
backup-db:
	scripts/backup_db.sh

.PHONY: upload-backup
upload-backup:
	scripts/upload_backup.sh

.PHONY: flush-cdn-cache
flush-cdn-cache:
	scripts/flush_cdn_cache.sh
#------------------------------------

#------------------------------------
# Tests
#------------------------------------
.PHONY: test
## Run tests | Tests
test: shellcheck hadolint shfmt actionlint tox eslint prettier-json-lint prettier-scss-lint \
	prettier-yaml-lint prettier-ts-lint prettier-html-lint prettier-vue-lint

.PHONY: tox
## Run tox
tox:
	tox

.PHONY: pydiatra
## Run pydiatra linter
pydiatra:
	tox -e py-pydiatra

.PHONY: pylint
## Run pylint linter
pylint:
	tox -e py-pylint

.PHONY: flake8
## Run flake8 linter
flake8:
	tox -e py-flake8

.PHONY: isort
## Run isort linter
isort:
	tox -e py-isort

.PHONY: bandit
## Run bandit linter
bandit:
	tox -e py-bandit

.PHONY: rstlint
## Run rstlint linter
rstlint:
	tox -e py-rstlint

.PHONY: pydocstyle
## Run pydocstyle linter
pydocstyle:
	tox -e py-pydocstyle

.PHONY: safety
## Run safety linter
safety:
	tox -e py-safety

.PHONY: pytest
## Run pytest
pytest:
	tox -e py-pytest

.PHONY: black
## Run black linter
black:
	tox -e py-black

.PHONY: mypy
## Run mypy linter
mypy:
	tox -e py-mypy

.PHONY: eslint
## Run eslint linter
eslint:
	${CMD_FRONTEND} && \
	yarn run eslint src/**/*.ts src/*.ts ./*.ts src/App.vue src/components/*.vue src/views/*.vue

.PHONY: shfmt
## Run shfmt linter
shfmt:
	shfmt -l -d ./*.sh scripts/*.sh

.PHONY: shellcheck
## Run shellcheck linter
shellcheck:
	shellcheck scripts/*.sh ./*.sh

.PHONY: hadolint
## Run hadolint linter
hadolint:
	hadolint Dockerfile

.PHONY: actionlint
## Run actionlint linter
actionlint:
	actionlint

.PHONY: prettier-html-lint
## Run html linter.
prettier-html-lint:
	${CMD_FRONTEND} && \
	yarn run prettier --check ./*.html

.PHONY: prettier-ts-lint
## Format ts files
prettier-ts-lint:
	${CMD_FRONTEND} && \
	yarn run prettier --check src/**/*.ts src/*.ts ./*.ts

.PHONY: prettier-scss-lint
## Run scss linter
prettier-scss-lint:
	${CMD_FRONTEND} && \
	yarn run prettier --check ./src/styles/*.scss

.PHONY: prettier-json-lint
## Run json linter
prettier-json-lint:
	${CMD_FRONTEND} && \
	yarn run prettier --check ../**/*.json

.PHONY: prettier-yaml-lint
## Run yaml linter
prettier-yaml-lint:
	${CMD_FRONTEND} && \
	yarn run prettier --check ../deployment/*.yaml ../.github/**/*.yaml

.PHONY: prettier-vue-lint
## Run vue linter
prettier-vue-lint:
	${CMD_FRONTEND} && \
	yarn run prettier --check src/App.vue src/components/*.vue src/views/*.vue
#------------------------------------

#------------------------------------
# Development
#------------------------------------
.PHONY: update-venvs
## Update packages in venv and tox venv with current requirements | Development
update-venvs:
	${SOURCE_CMDS} && \
	pip install -r requirements-dev.txt && \
	deactivate && \
	source .tox/py/bin/activate && \
	pip install -r requirements-dev.txt

.PHONY: delete-venvs
delete-venvs:
	rm -rf venv
	rm -rf .tox

.PHONY: recreate-venvs
## Recreate venvs
recreate-venvs: delete-venvs create-venvs

.PHONY: yarn-install
## Run yarn install
yarn-install:
	${CMD_FRONTEND} && \
	yarn install

.PHONY: yarn-upgrade
## Run yarn upgrade
yarn-upgrade:
	${CMD_FRONTEND} && \
	yarn upgrade-interactive

.PHONY: dev
## Run yarn dev
dev:
	${CMD_FRONTEND} && \
	yarn dev

.PHONY: serve
## Run yarn serve
serve:
	${CMD_FRONTEND} && \
	yarn serve

.PHONY: build
## Run yarn build
build:
	${CMD_FRONTEND} && \
	yarn build

.PHONY: drop-db
## Drop db
drop-db:
	source $(ENV_FILE) && \
	scripts/drop_db.sh

.PHONY: load-db
## Load db from today's backup
load-db: drop-db create-db
	source $(ENV_FILE) && \
	scripts/load_db.sh
#------------------------------------

#------------------------------------
# Formatting backend
#------------------------------------
.PHONY: format
## Format python code | Formatting backend
format:
	${SOURCE_CMDS} && \
	autoflake --remove-all-unused-imports --in-place -r src && \
	isort src && \
	black .

.PHONY: f
## Format python code (format alias)
f: format
#------------------------------------

#------------------------------------
# Formatting miscellaneous
#------------------------------------
.PHONY: format-misc
## Format sh, json, yaml files | Formatting miscellaneous
format-misc: format-sh format-json format-yaml

.PHONY: format-sh
## Format sh files
format-sh:
	shfmt -l -w ./*.sh scripts/*.sh

.PHONY: format-json
## Format json files
format-json:
	${CMD_FRONTEND} && \
	yarn run prettier --write ../**/*.json

.PHONY: format-yaml
## Format yaml files
format-yaml:
	${CMD_FRONTEND} && \
	yarn run prettier --write ../deployment/*.yaml ../.github/**/*.yaml
#------------------------------------

#------------------------------------
# Formatting frontend
#------------------------------------
.PHONY: format-frontend
## Format files for frontend (vue, ts, scss, html) | Formatting frontend
format-frontend: format-html format-ts format-scss format-vue

.PHONY: ff
## Format files for frontend (vue, ts, scss, html) (format-frontend alias)
ff: format-frontend

.PHONY: format-ts
## Format ts files
format-ts:
	${CMD_FRONTEND} && \
	yarn run prettier --write src/**/*.ts src/*.ts ./*.ts

.PHONY: format-scss
## Format scss files
format-scss:
	${CMD_FRONTEND} && \
	yarn run prettier --write ./src/styles/*.scss

.PHONY: format-vue
## Format vue files
format-vue:
	${CMD_FRONTEND} && \
	yarn run prettier --write src/App.vue src/components/*.vue src/views/*.vue

.PHONY: format-html
## Format html files
format-html:
	${CMD_FRONTEND} && \
	yarn run prettier --write ./*.html
#------------------------------------

#------------------------------------
# Formatting all
#------------------------------------
.PHONY: format-all
## Format code | Formatting all
format-all: format format-sh format-json format-yaml format-frontend

.PHONY: fa
## Format code (format-all alias)
fa: format-all
#------------------------------------

#------------------------------------
# Django management commands
#------------------------------------
MANAGE_CMD := src/manage.py

.PHONY: runserver
## Run server for development
runserver:
	${SOURCE_CMDS} && \
	${MANAGE_CMD} runserver 0.0.0.0:8000

.PHONY: run
## Run server for development
run: runserver

.PHONY: migrate
## Run data migration
migrate:
	${SOURCE_CMDS} && \
	${MANAGE_CMD} migrate

.PHONY: collectstatic
## Collect static files
collectstatic:
	${SOURCE_CMDS} && \
	export IS_DEV= && \
	${MANAGE_CMD} collectstatic --no-input

.PHONY: createsuperuser
## Create super user
createsuperuser:
	${SOURCE_CMDS} && \
	${MANAGE_CMD} createsuperuser

.PHONY: shell
## Run shell
shell:
	${SOURCE_CMDS} && \
	${MANAGE_CMD} shell

.PHONY: makemigrations
## Run makemigrations command. Usage: make makemigrations arguments="[arguments]"
makemigrations:
	${SOURCE_CMDS} && \
	${MANAGE_CMD} makemigrations $(arguments) ${APP}

ifeq (manage,$(firstword $(MAKECMDGOALS)))
  # Use the rest as arguments
  MANAGE_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # Turn them into do-nothing targets
  $(eval $(MANAGE_ARGS):;@:)
endif

.PHONY: manage
## Run management command. Usage: make manage [command] arguments="[arguments]"
manage:
	${SOURCE_CMDS} && \
	${MANAGE_CMD} ${MANAGE_ARGS} $(arguments)
#------------------------------------

#------------------------------------
# Docker commands
#------------------------------------
export DOCKER_ENV_FILE := docker.env

.PHONY: docker-build-dev
## Build docker images | Docker
docker-build-dev: docker-build-backend docker-build-frontend-dev

.PHONY: docker-build-backend
## Build docker backend image | Docker
docker-build-backend:
	scripts/docker_build_backend.sh

.PHONY: docker-build-frontend-dev
## Build docker frontend image | Docker
docker-build-frontend-dev:
	export VITE_BACKEND_URL=http://localhost:8000/ && \
	scripts/docker_build_frontend.sh

.PHONY: docker-run
## Run server in docker
docker-run: collectstatic
	docker-compose up

.PHONY: docker-sh
## Run docker shell
docker-sh:
	docker run -ti --env-file ${DOCKER_ENV_FILE} --env-file $(DOCKER_SECRETS_ENV_FILE) ${PROJECT} sh
#------------------------------------

#------------------------------------
# Production commands
#------------------------------------
.PHONY: prod-create-db
## Create prod db | Production
prod-create-db:
	source $(DB_ENV_PROD_FILE) && \
	scripts/create_db.sh

.PHONY: prod-drop-db
## Drop prod db
prod-drop-db:
	source $(DB_ENV_PROD_FILE) && \
	scripts/drop_db.sh

.PHONY: prod-load-db
## Load db to prod from today's backup
prod-load-db: prod-drop-db prod-create-db
	source $(DB_ENV_PROD_FILE) && \
	scripts/load_db.sh

.PHONY: prod-connect-db
## Connect to prod db
prod-connect-db:
	source $(DB_ENV_PROD_FILE) && \
	scripts/connect_db.sh

ifeq (prod-manage,$(firstword $(MAKECMDGOALS)))
  # Use the rest as arguments
  PROD_MANAGE_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # Turn them into do-nothing targets
  $(eval $(PROD_MANAGE_ARGS):;@:)
endif

.PHONY: prod-manage
## Run management command in prod. Usage: make prod-manage [command] arguments="[arguments]"
prod-manage:
	scripts/run_management_command_prod.sh ${PROD_MANAGE_ARGS} $(arguments)

ifeq (prod-manage-interactive,$(firstword $(MAKECMDGOALS)))
  # Use the rest as arguments
  PROD_MANAGE_INTERACTIVE_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # Turn them into do-nothing targets
  $(eval $(PROD_MANAGE_INTERACTIVE_ARGS):;@:)
endif

.PHONY: prod-manage-interactive
## Run management command in prod (interactive). Usage: make prod-manage [command] arguments="[arguments]"
prod-manage-interactive:
	scripts/run_management_command_interactive_prod.sh ${PROD_MANAGE_INTERACTIVE_ARGS} $(arguments)

.PHONY: prod-shell
## Run shell in prod
prod-shell:
	scripts/run_shell_prod.sh

.PHONY: prod-migrate
## Run data migration for prod
prod-migrate:
	scripts/run_management_command_prod.sh migrate

.PHONY: prod-enable-debug
## Enable debug in prod. It will be reset with the next deployment
prod-enable-debug:
	yq eval '.data.DEBUG="True"' deployment/configmap.yaml | kubectl apply -f -
	kubectl rollout restart "deployment/${PROJECT}"

.PHONY: prod-load-initial-fixtures
## Load initial fixtures in prod
prod-load-initial-fixtures:
	$(MAKE) prod-manage arguments="loaddata lists"
	$(MAKE) prod-manage arguments="loaddata categories"
#------------------------------------
