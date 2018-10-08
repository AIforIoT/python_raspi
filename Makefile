include makefile.env

ROOT_DIR=$(shell pwd)/

.PHONY: up rpc_up

up:
	@echo "******Starting application******"
	./bootstrap.sh "--host=$(HOST) --port=$(APP_PORT)" $(ENVIRONMENT) $(FLASK_APP)


rpc_up:
	@echo "******Starting RPC application******"
	./bootstrap.sh "--host=$(HOST) --port=$(RPC_API_PORT)" $(ENVIRONMENT) $(FLASK_APP_RPC)