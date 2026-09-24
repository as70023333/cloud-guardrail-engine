# Contributing to Awesome Security Engineer

Thank you for your interest in contributing to Awesome Security Engineer! This document provides guidelines and information for contributors.

## 🎯 How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear descriptive title**
- **Detailed description** of the issue
- **Steps to reproduce** the behavior
- **Expected vs actual behavior**
- **Environment details** (OS, Go/Python version, etc.)
- **Logs or screenshots** if applicable

### Suggesting Features

Feature suggestions are welcome! Please provide:

- **Use case** for the feature
- **Expected behavior**
- **Any alternatives** you've considered
- **Additional context** or mockups

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add or update tests as needed
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📋 Development Guidelines

### Cloud Guardrail Engine (Go)

#### Code Style

- Follow standard [Go conventions](https://go.dev/doc/effective_go)
- Run `gofmt` before committing
- Use meaningful variable and function names
- Add comments for exported functions
- Keep functions small and focused

#### Testing

- Write unit tests for all new functionality
- Maintain or improve test coverage
- Use table-driven tests where appropriate
- Test both success and error cases

```bash
# Run tests
cd cloud-guardrail-engine
go test -v ./...

# Run with coverage
go test -v -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

#### OPA Rego Policies

- Follow [OPA best practices](https://www.openpolicyagent.org/docs/latest/policy-language/)
- Include unit tests for all policies
- Use descriptive rule names
- Add comments explaining policy logic
- Test with various input scenarios

```bash
# Test policies
make test-policies

# Validate policy syntax
opa check policies/
```

### Zero-Trust Quarantine Engine (Python)

#### Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use type hints for all functions
- Keep lines under 100 characters
- Use meaningful variable names
- Add docstrings for all functions and classes

#### Testing

- Write unit tests for all new functionality
- Use pytest for testing
- Mock external dependencies (AWS, Azure)
- Test both success and error cases

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest -v

# Run with coverage
pytest --cov=. --cov-report=html
```

#### API Development

- Follow RESTful API design principles
- Use Pydantic models for request/response validation
- Add proper error handling
- Include API documentation in docstrings
- Test all endpoints

```bash
# Start development server
uvicorn main:app --reload

# View API documentation
# Open http://localhost:8080/docs in browser
```

### Kubernetes Manifests

- Follow Kubernetes security best practices
- Use non-root users
- Set resource limits and requests
- Include health checks
- Use ConfigMaps and Secrets appropriately
- Test manifests with `kubectl apply --dry-run=client`

```bash
# Validate manifests
kubectl apply -f k8s/deployment.yaml --dry-run=client

# Check for security issues
kubectl get pods -o jsonpath='{range .items[*]}{.spec.securityContext}{"\n"}{end}'
```

## 🔍 Code Review Process

All submissions require review before merging. Reviewers will check:

- **Code quality** and adherence to style guidelines
- **Test coverage** for new functionality
- **Documentation** updates
- **Security implications**
- **Performance impact**
- **Backward compatibility**

## 📝 Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(cloud-guardrail): add GCP policy support

fix(quarantine): handle Azure API timeout errors

docs(readme): update installation instructions

test(cloud-guardrail): add unit tests for AWS policy
```

## 🚀 Release Process

1. Update version numbers in relevant files
2. Update CHANGELOG.md
3. Create a release branch
4. Run all tests
5. Create a GitHub release with release notes
6. Tag the release

## 🐛 Finding Issues to Work On

- Look for issues labeled `good first issue` for beginner-friendly tasks
- Check `help wanted` labels for community contributions
- Review the [Roadmap](README.md#roadmap) section in README

## 💬 Getting Help

- Check existing [documentation](README.md)
- Search [GitHub Discussions](https://github.com/as70023333/awesome-security-engineer/discussions)
- Open an issue for questions
- Reach out to maintainers

## 🏆 Recognition

Contributors will be recognized in:

- README.md contributors section
- Release notes
- Project documentation

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🎓 Learning Resources

### Go

- [Effective Go](https://go.dev/doc/effective_go)
- [Go by Example](https://gobyexample.com/)
- [OPA Documentation](https://www.openpolicyagent.org/docs/latest/)

### Python

- [Python Best Practices](https://docs.python-guide.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pytest Documentation](https://docs.pytest.org/)

### Kubernetes

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes Security](https://kubernetes.io/docs/concepts/security/)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)

### Security

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

Thank you for contributing to Awesome Security Engineer! 🎉
