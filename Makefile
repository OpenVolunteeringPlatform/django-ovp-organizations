test:
	@python ovp_organizations/tests/runtests.py

lint:
	@pylint ovp_organizations

clean-pycache:
	@rm -r **/__pycache__

clean: clean-pycache

.PHONY: clean


