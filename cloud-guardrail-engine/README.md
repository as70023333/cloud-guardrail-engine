# Cloud Guardrail Engine

A Go-based CLI tool that evaluates Terraform plan JSON output against Open Policy Agent (OPA) Rego policies to enforce cloud security guardrails before infrastructure changes are applied.

## 🎯 Overview

Cloud Guardrail Engine provides automated policy validation for Terraform plans, ensuring that infrastructure changes comply with security standards before deployment. It supports multi-cloud environments with policies for AWS and Azure.

## 📁 Project Structure

```
cloud-guardrail-engine/
├── main.go                                    # CLI entrypoint & OPA evaluation engine
├── go.mod                                     # Go module definition
├── go.sum                                     # Dependency checksums
├── Makefile                                   # Build & test automation
├── policies/
│   ├── aws_s3_encryption.rego                # AWS S3 encryption policy
│   ├── aws_s3_encryption_test.rego           # AWS policy unit tests
│   ├── azure_storage_https.rego              # Azure HTTPS enforcement policy
│   └── azure_storage_https_test.rego         # Azure policy unit tests
└── tests/
    └── mock_tfplan.json                      # Test fixture (Terraform Plan JSON)
```

## 🚀 Quick Start

### Prerequisites

- Go 1.22 or higher
- OPA CLI (for policy testing)
- Make (optional, for build automation)

### Installation

```bash
# Clone the repository
git clone https://github.com/as70023333/cloud-guardrail-engine.git
cd cloud-guardrail-engine

# Install dependencies
make deps
# or manually:
go mod download
```

### Build

```bash
# Build the binary
make build
# or manually:
go build -o bin/cloud-guardrail main.go
```

### Usage

```bash
# Run against a Terraform plan
./bin/cloud-guardrail -plan ./tests/mock_tfplan.json -policies ./policies

# Example output:
{
  "compliant": false,
  "violations": [
    "[aws] AWS S3 bucket 'unencrypted_bucket' must have server-side encryption enabled.",
    "[azure] Azure Storage Account 'insecure_storage' must enforce HTTPS traffic only."
  ]
}
```

## 📋 Available Make Commands

```bash
make all              # Run lint, test, and build
make deps             # Download Go dependencies
make build            # Build the binary
make test             # Run Go unit tests
make test-policies    # Run OPA policy unit tests
make lint             # Run linters
make run-mock         # Run against mock Terraform plan
make clean            # Clean build artifacts
```

## 🔐 Policies

### AWS S3 Encryption Policy

**File:** `policies/aws_s3_encryption.rego`

Enforces that all AWS S3 buckets have server-side encryption enabled.

**Rule:**
- Denies creation of S3 buckets without `server_side_encryption_configuration`

**Example Violation:**
```json
{
  "name": "unencrypted_bucket",
  "type": "aws_s3_bucket",
  "change": {
    "actions": ["create"],
    "after": {
      "bucket": "my-sensitive-data-bucket"
    }
  }
}
```

### Azure Storage HTTPS Policy

**File:** `policies/azure_storage_https.rego`

Enforces that all Azure Storage accounts enforce HTTPS-only traffic.

**Rule:**
- Denies creation of storage accounts with `enable_https_traffic_only != true`

**Example Violation:**
```json
{
  "name": "insecure_storage",
  "type": "azurerm_storage_account",
  "change": {
    "actions": ["create"],
    "after": {
      "name": "stmulticloudprod01",
      "enable_https_traffic_only": false
    }
  }
}
```

## 🧪 Testing

### Run OPA Policy Tests

```bash
make test-policies
# or manually:
opa test ./policies -v
```

**Expected Output:**
```
cloud.guardrail.aws_test:
  PASS: test_deny_unencrypted_s3_bucket
  PASS: test_allow_encrypted_s3_bucket

cloud.guardrail.azure_test:
  PASS: test_deny_http_azure_storage
  PASS: test_allow_https_azure_storage

--------------------------------------------------------------------------------
PASS: 4/4
```

### Test Fixtures

The `tests/mock_tfplan.json` file contains sample Terraform plan data with both compliant and non-compliant resources for testing purposes.

## 🔧 Architecture

```
Terraform Plan JSON
       ↓
┌──────────────────┐
│  OPA Rego Engine │
│  (main.go)       │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  Policy Loader   │
│  (rego.Load)     │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  Evaluation      │
│  (data.cloud.    │
│   guardrail)     │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  JSON Report     │
│  {compliant,     │
│   violations}    │
└──────────────────┘
```

## 📊 API Response Format

### Success (Compliant)
```json
{
  "compliant": true,
  "violations": []
}
```

### Failure (Non-Compliant)
```json
{
  "compliant": false,
  "violations": [
    "[aws] AWS S3 bucket 'unencrypted_bucket' must have server-side encryption enabled.",
    "[azure] Azure Storage Account 'insecure_storage' must enforce HTTPS traffic only."
  ]
}
```

## 🚢 CI/CD Integration

The engine is designed for CI/CD integration:
- Exits with code `0` when compliant
- Exits with code `1` when violations are found
- JSON output can be parsed by automation tools

### GitHub Actions Example

```yaml
- name: Run Cloud Guardrail Engine
  working-directory: cloud-guardrail-engine
  run: |
    ./bin/cloud-guardrail -plan terraform.json -policies ./policies > output.json || true
    grep -q '"compliant": false' output.json && exit 1 || exit 0
```

## 🛠️ Development

### Adding New Policies

1. Create a new `.rego` file in `policies/`
2. Use the package naming convention: `cloud.guardrail.<provider>`
3. Implement `deny` rules that return violation messages
4. Create corresponding `_test.rego` file with test cases
5. Run `make test-policies` to verify

### Policy Template

```rego
package cloud.guardrail.<provider>_test

import future.keywords.in
import data.cloud.guardrail.<provider>

test_deny_<scenario> {
    mock_plan := {
        "resource_changes": [{
            "name": "test_resource",
            "type": "<resource_type>",
            "change": {
                "actions": ["create"],
                "after": {
                    # Non-compliant configuration
                }
            }
        }]
    }

    res := <provider>.deny with input as mock_plan
    count(res) == 1
}
```

## 📚 Dependencies

- **Go 1.22+** - Programming language
- **OPA v0.60.0** - Policy engine
- **cobra** - CLI framework (optional, using stdlib flag)

## 🔒 Security Features

- ✅ Policy-as-code enforcement
- ✅ Shift-left security validation
- ✅ Multi-cloud support (AWS, Azure)
- ✅ Automated compliance checking
- ✅ JSON-formatted reports
- ✅ CI/CD friendly exit codes

## 📖 Documentation

- [Main Repository README](https://github.com/as70023333/cloud-guardrail-engine/blob/main/README.md)
- [OPA Documentation](https://www.openpolicyagent.org/docs/latest/)
- [Terraform Plan JSON Format](https://developer.hashicorp.com/terraform/internals/json-format)

## 🤝 Contributing

See the [main repository CONTRIBUTING.md](https://github.com/as70023333/cloud-guardrail-engine/blob/main/CONTRIBUTING.md) for guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/as70023333/cloud-guardrail-engine/blob/main/LICENSE) file for details.

## 🆘 Support

For issues and questions:
- [GitHub Issues](https://github.com/as70023333/cloud-guardrail-engine/issues)
- [GitHub Discussions](https://github.com/as70023333/cloud-guardrail-engine/discussions)

---

**Built with ❤️ for cloud security engineers**
