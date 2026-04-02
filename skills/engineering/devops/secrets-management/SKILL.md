---
name: secrets-management
description: "Implement secrets management for CI/CD with Vault, AWS Secrets Manager, or native tools"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /secrets-management
metadata:
  openclaw:
    emoji: "🔒"
    requires:
      bins: []
      env: []
---

# Secrets Management

Implement secure secrets management for CI/CD pipelines using HashiCorp Vault, AWS Secrets Manager, or native platform solutions. Use when handling sensitive credentials, implementing secret rotation, or securing CI/CD environments.

## When to Use

- Storing and rotating API keys and credentials
- Managing database passwords across environments
- Handling TLS certificates lifecycle
- Implementing least-privilege access to secrets
- Setting up secret scanning in CI/CD pipelines

## Secrets Management Tools

| Tool | Best For | Key Feature |
|---|---|---|
| HashiCorp Vault | Centralized, multi-cloud | Dynamic secrets, fine-grained ACLs |
| AWS Secrets Manager | AWS-native workloads | Automatic rotation, RDS integration |
| Azure Key Vault | Azure workloads | HSM-backed keys, RBAC |
| Google Secret Manager | GCP workloads | Versioning, IAM integration |

## Integration Patterns

### GitHub Actions with Vault
Use `hashicorp/vault-action@v2` to import secrets at workflow runtime. Map Vault paths to environment variables with `::add-mask::` for log safety.

### AWS Secrets Manager in CI
Configure AWS credentials, retrieve secrets with `aws secretsmanager get-secret-value`, mask in logs, export to environment.

### Kubernetes External Secrets
ExternalSecret CRD syncs secrets from Vault/AWS/Azure into Kubernetes Secrets with configurable refresh intervals.

## Secret Rotation

**Automated (AWS):** Lambda function triggered by rotation schedule — generate new password, update database, update secret store.
**Manual process:** Generate new secret → update store → update applications → verify → revoke old secret.

## Secret Scanning

**Pre-commit hook:** TruffleHog filesystem scan before each commit. Block commit if secrets detected.
**CI/CD pipeline:** Automated scanning on every push with `trufflehog filesystem .` — fail pipeline on detection.

## Best Practices

1. Never commit secrets to Git
2. Use different secrets per environment (dev/staging/prod)
3. Rotate secrets regularly (monthly minimum)
4. Implement least-privilege access
5. Enable audit logging for all secret access
6. Use secret scanning tools (GitGuardian, TruffleHog)
7. Mask secrets in CI/CD logs
8. Use short-lived tokens when possible
9. Encrypt secrets at rest
10. Document secret requirements per service
