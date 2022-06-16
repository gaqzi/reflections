#################################
### Pelican
#################################
PY?=python3
PELICAN?=pelican
PELICANOPTS=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py

GITHUB_PAGES_BRANCH=gh-pages


DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICANOPTS += --relative-urls
endif

SERVER ?= "0.0.0.0"

PORT ?= 0
ifneq ($(PORT), 0)
	PELICANOPTS += -p $(PORT)
endif

help: ## Show this help message.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


html: ## (Re)generate the web site
	"$(PELICAN)" "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

clean: ## Remove the generated files.
	[ ! -d "$(OUTPUTDIR)" ] || rm -rf "$(OUTPUTDIR)"

regenerate: ## Regenerate and serve on '0.0.0.0'
	"$(PELICAN)" -r "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

serve: ## Serve site at 'http://localhost:5000'.
	"$(PELICAN)" -l "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

serve-global: ## Serve (as root) to '$(SERVER):80'
	"$(PELICAN)" -l "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS) -b $(SERVER)

devserver: ## Serve and regenerate together.
	"$(PELICAN)" -lr "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

devserver-global: ## regenerate and serve on '0.0.0.0'.
	$(PELICAN) -lr $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS) -b 0.0.0.0

publish: ## Generate using production settings.
	"$(PELICAN)" "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(PUBLISHCONF)" $(PELICANOPTS)

github: publish ## Upload the web site via gh-pages.
	ghp-import -m "Generate Pelican site" -b $(GITHUB_PAGES_BRANCH) "$(OUTPUTDIR)" -f
	git push origin $(GITHUB_PAGES_BRANCH) -f


#################################
### Local Dev
#################################
path := .

## Init
init:
	@echo
	@echo "Initializing..."
	@echo "==============="
	@python3.10 -m venv .venv
	@.venv/bin/python -m pip install -r requirements.txt
	@.venv/bin/python -m pip install -r requirements-dev.txt
	@.venv/bin/pelican-themes --install theme/elegant || exit 0
	@.venv/bin/pre-commit install
	@.venv/bin/pre-commit run --all || exit 0


## Lint
lint: black blacken-docs isort flake mypy	## Apply all the linters.

lint-check:  ## Check whether the codebase satisfies the linter rules.
	@echo
	@echo "Checking linter rules..."
	@echo "========================"
	@echo
	@black --check $(path)
	@isort --check $(path)
	@flake8 $(path)
	@mypy $(path)

black: ## Apply black.
	@echo
	@echo "Applying black..."
	@echo "================="
	@echo
	@black --fast $(path) -l 80
	@echo


blacken-docs: ## Apply black.
	@echo
	@echo "Applying blacken docs..."
	@echo "========================"
	@echo
	@blacken-docs -E content/python/*.md -l 79
	@echo


isort: ## Apply isort.
	@echo "Applying isort..."
	@echo "================="
	@echo
	@isort $(path)

flake: ## Apply flake8.
	@echo
	@echo "Applying flake8..."
	@echo "================="
	@echo
	@flake8 $(path)

mypy: ## Apply mypy.
	@echo
	@echo "Applying mypy..."
	@echo "================="
	@echo
	@mypy $(path)


dep-lock: ## Freeze deps in 'requirements.txt' file.
	@pip-compile requirements.in \
			-o requirements.txt \
			--no-emit-options \
			--no-emit-index-url
	@pip-compile requirements-dev.in \
			-o requirements-dev.txt \
			--no-emit-options \
			--no-emit-index-url


.PHONY: html help clean regenerate serve serve-global devserver \
        publish github lint lint-check black blacken-docs isort flake mypy \
        dep-lock
