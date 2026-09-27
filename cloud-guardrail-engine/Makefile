# Makefile for Multi-Cloud Guardrail Engine

.PHONY: all build test test-policies lint clean run-mock deps

BINARY_NAME=cloud-guardrail
POLICIES_DIR=./policies
TEST_PLAN=./tests/mock_tfplan.json

all: lint test build

deps:
	@echo "==> Downloading Go dependencies..."
	go mod tidy
	go mod download

build:
	@echo "==> Building binary..."
	go build -o bin/$(BINARY_NAME) main.go

test:
	@echo "==> Running Go unit tests..."
	go test -v ./...

test-policies:
	@echo "==> Running OPA policy unit tests..."
	@command -v opa >/dev/null 2>&1 || { echo "opa is required but not installed."; exit 1; }
	opa test $(POLICIES_DIR) -v

lint:
	@echo "==> Running linters..."
	@command -v golangci-lint >/dev/null 2>&1 || { echo "golangci-lint is required but not installed."; exit 1; }
	golangci-lint run

run-mock: build
	@echo "==> Executing guardrail scan on mock terraform plan..."
	./bin/$(BINARY_NAME) -plan $(TEST_PLAN) -policies $(POLICIES_DIR) || true

clean:
	@echo "==> Cleaning build artifacts..."
	rm -rf bin/
