# Security Policy

## Supported Versions

We release patches for security vulnerabilities. The following versions are currently being supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of PolicyMind AI seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email at [contact@policymind.ai](mailto:contact@policymind.ai) or create a private vulnerability report on GitHub.

### What to Include

Please include the following information in your report:

- Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the issue
- Location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### Response Timeline

- We will acknowledge receipt of your vulnerability report within 48 hours
- We will send you a more detailed response within 7 days indicating the next steps
- We will keep you informed of our progress towards a fix and full announcement
- We may ask for additional information or guidance

### Security Best Practices

When using PolicyMind AI, please follow these security best practices:

1. **API Keys**: Never commit API keys or tokens to the repository
2. **Environment Variables**: Use environment variables for sensitive configuration
3. **Dependencies**: Keep dependencies updated with security patches
4. **Docker**: Run containers with minimal privileges
5. **Input Validation**: Validate all user inputs in production deployments

## Security Measures

### Code Security

- All dependencies are regularly scanned for known vulnerabilities
- Code is reviewed for security issues before release
- Static analysis tools are used to identify potential security flaws

### Infrastructure Security

- Docker containers are built with minimal base images
- Containers run with non-root users where possible
- Health checks are implemented for monitoring

## Known Limitations

- This is a research/hackathon project and may not have enterprise-grade security features
- API keys must be managed by the user (not stored in the repository)
- Network security is the responsibility of the deployer

## Recognition

We believe in recognizing security researchers who help improve our security. Contributors who report valid security issues will be acknowledged (unless they prefer to remain anonymous).

---

Thank you for helping keep PolicyMind AI and our users safe!