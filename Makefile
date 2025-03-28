SHELL := /bin/bash -o pipefail -o errexit

help:  ## Display help for the Makefile targets
	@@grep -h '^[a-zA-Z]' $(MAKEFILE_LIST) | awk -F ':.*?## ' 'NF==2 {printf "   %-20s%s\n", $$1, $$2}' | sort

dev:  ## Serve them in live-reload mode
	@echo "Starting all processes..."
	@trap 'kill 0' EXIT; \
	{ \
	  conda run --prefix ./env --live-stream pyscript run --port 8001 --no-view & \
	  sleep 3 && \
	  npx browser-sync start \
		--files "**/*.html" \
		--files "**/*.js" \
		--files "**/*.css" \
		--files "**/*.svg" \
		--files "**/*.py" \
		--no-inject-changes \
		--open external \
		--host "127.0.0.1" \
		--no-notify \
        --port 3002 \
		--proxy "http://127.0.0.1:8001" & \
	  wait; \
	}

.PHONY: $(MAKECMDGOALS)
