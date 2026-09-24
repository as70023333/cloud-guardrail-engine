# Cloud Guardrail Engine - Makefile
# Build & test automation for OPA-based cloud security policy evaluation

.PHONY: all build test lint clean run help install-deps check-policies

# Variables
BINARY_NAME := cloud-guardrail-engine
BUILD_DIR := ./build
POLICIES_DIR := ./policies
TESTS_DIR := ./tests
GO_FILES := $(shell find . -name '*.go' -not -path "./vendor/*")
VERSION ?= $(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")
COMMIT ?= $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")
BUILD_TIME := $(shell date -u '+%Y-%m-%dT%H:%M:%SZ')
LDFLAGS := -ldflags "-X main.version=$(VERSION) -X main.commit=$(COMMIT) -X main.buildTime=$(BUILD_TIME)"

# Default target
all: lint test build

## help: Show this help message
help:
	@echo "Cloud Guardrail Engine - Build & Test Automation"
	@echo ""
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@echo "Targets:"
	@grep -E '^## ' $(MAKEFILE_LIST) | sed -e 's/## /  /' | sort

## build: Build the binary
build:
	@echo "🔨 Building $(BINARY_NAME)..."
	@mkdir -p $(BUILD_DIR)
	go build $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME) .
	@echo "✅ Build complete: $(BUILD_DIR)/$(BINARY_NAME)"

## test: Run all tests
test:
	@echo "🧪 Running tests..."
	go test -v -race -coverprofile=coverage.out ./...
	@echo "✅ Tests passed"

## test-coverage: Run tests with coverage report
test-coverage: test
	@echo "📊 Generating coverage report..."
	go tool cover -html=coverage.out -o coverage.html
	@echo "✅ Coverage report: coverage.html"

## lint: Run linters
lint:
	@echo "🔍 Running linters..."
	@if command -v golangci-lint > /dev/null 2>&1; then \
		golangci-lint run ./...; \
	else \
		echo "⚠️  golangci-lint not found, running go vet instead"; \
		go vet ./...; \
	fi
	@echo "✅ Lint complete"

## check-policies: Validate OPA policies
check-policies:
	@echo "📋 Validating OPA policies..."
	@for policy in $(POLICIES_DIR)/*.rego; do \
		echo "  Checking $$policy..."; \
		opa check $$policy || exit 1; \
	done
	@echo "✅ All policies valid"

## test-policies: Run OPA policy tests against mock data
test-policies:
	@echo "🧪 Testing policies against mock Terraform plan..."
	@for policy in $(POLICIES_DIR)/*.rego; do \
		echo "  Evaluating $$policy..."; \
		opa eval -d $$policy -i $(TESTS_DIR)/mock_tfplan.json "data" || exit 1; \
	done
	@echo "✅ Policy tests passed"

## run: Run the guardrail engine against mock data
run: build
	@echo "🚀 Running guardrail engine..."
	$(BUILD_DIR)/$(BINARY_NAME) --policies $(POLICIES_DIR) --plan $(TESTS_DIR)/mock_tfplan.json

## run-json: Run and output JSON results
run-json: build
	$(BUILD_DIR)/$(BINARY_NAME) --policies $(POLICIES_DIR) --plan $(TESTS_DIR)/mock_tfplan.json --json

## install-deps: Install development dependencies
install-deps:
	@echo "📦 Installing dependencies..."
	go mod download
	go mod tidy
	@echo "✅ Dependencies installed"

## fmt: Format Go source code
fmt:
	@echo "📝 Formatting code..."
	gofmt -s -w $(GO_FILES)
	@echo "✅ Code formatted"

## clean: Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf $(BUILD_DIR)
	rm -f coverage.out coverage.html
	@echo "✅ Clean complete"

## docker-build: Build Docker image
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t $(BINARY_NAME):$(VERSION) .
	@echo "✅ Docker image built"

## ci: Run all CI checks
ci: install-deps fmt lint check-policies test build
	@echo "✅ All CI checks passed"
