include makefile.env

ROOT_DIR=$(shell pwd)/

.PHONY: run

run:
	@echo "******Starting application******"
	./bootstrap.sh "--host=$(HOST) --port=$(PORT)" $(ENVIRONMENT)



