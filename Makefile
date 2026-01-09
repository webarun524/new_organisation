.PHONY: install
install:
	poetry install

.PHONY: test
test:
	poetry run pytest tests -v

.PHONY: quality_test
quality_test:
	./buildscripts/quality.sh

.PHONY: e2e_op_tests
e2e_op_tests:
	poetry run pytest e2e -v --browser chromium -m operations_portal

.PHONY: e2e_dp_verification_tests
e2e_dp_verification_tests:
	poetry run pytest e2e -v --browser chromium -m data_portal_verification

.PHONY: e2e_dp_teardown_tests
e2e_dp_teardown_tests:
	poetry run pytest e2e -v --browser chromium -m data_portal_teardown

.PHONY: build
build:
	@echo "Building code is integrated into deploy step in this repository"

.PHONY: deploy
deploy: setup
	./buildscripts/deploy.sh

.PHONY: destroy
destroy: setup
	./buildscripts/destroy.sh

define HELP_TEXT
help:                     	Display this help message.
install:                  	Installs Python dependencies.
test:                     	Runs unit tests.
quality_test:             	Runs quality checks.
e2e_op_tests:             	Runs end-to-end tests for the Operations Portal.
e2e_dp_verification_tests:  Runs end-to-end tests for Data Portal verification.
e2e_dp_teardown_tests:  	  Runs end-to-end tests for Data Portal teardown.
build:                  	  Builds application.
deploy:                 	  Deploys application.
destroy:                	  Destroys application.
endef
export HELP_TEXT

.PHONY: help
help:
	@echo "$$HELP_TEXT"
