---
name: ci-cd-github-actions
description: "Create GitHub Actions workflows for testing, building, and deploying applications"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /ci-cd-github-actions
metadata:
  openclaw:
    emoji: "🔄"
    requires:
      bins: []
      env: []
---

# GitHub Actions CI/CD Templates

Create production-ready GitHub Actions workflows for automated testing, building, Docker image publishing, Kubernetes deployment, and security scanning. Use when setting up CI/CD, automating development workflows, or creating reusable workflow templates.

## When to Use

- Setting up automated testing and deployment pipelines
- Building and pushing Docker images to registries
- Deploying to Kubernetes clusters
- Implementing matrix builds for multiple environments
- Creating reusable workflow templates
- Adding security scanning to CI/CD

## Common Workflow Patterns

### Test Workflow
Trigger on push to main/develop and PRs to main. Matrix strategy for multiple Node/Python versions. Steps: checkout, setup runtime, install dependencies (`npm ci`), lint, test, upload coverage.

### Build and Push Docker Image
Trigger on push to main and version tags. Use `docker/metadata-action` for automatic tagging (branch, PR, semver). Use `docker/build-push-action` with GitHub Actions cache (`type=gha`).

### Kubernetes Deployment
Configure cloud credentials (AWS/GCP/Azure). Update kubeconfig. Apply manifests with `kubectl apply`. Verify with `kubectl rollout status`.

### Matrix Build
Cross-platform testing: `ubuntu-latest`, `macos-latest`, `windows-latest` with multiple runtime versions.

### Security Scanning
Trivy filesystem scan with SARIF output uploaded to GitHub Security. Snyk dependency scanning.

### Deployment with Approvals
Environment protection rules with required reviewers. Slack notification on success/failure.

## Reusable Workflows

Define with `workflow_call` trigger accepting inputs and secrets. Call with `uses: ./.github/workflows/reusable-test.yml`.

## Best Practices

1. Use specific action versions (`@v4`, not `@latest`)
2. Cache dependencies to speed up builds
3. Use GitHub secrets for sensitive data (never commit credentials)
4. Implement status checks on PRs as required
5. Use matrix builds for multi-version testing
6. Set appropriate GITHUB_TOKEN permissions per job
7. Add notification steps for failure alerting
8. Use self-hosted runners for sensitive workloads
