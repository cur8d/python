# Sentinel Security Journal

This journal contains critical security learnings specific to this project.

## 2025-02-14 - Supply Chain Hardening via Action Pinning & Least-Privilege Permissions
**Vulnerability:** Workflows referenced a mutable and non-existent version tag (`@v7`) for `actions/checkout` and lacked explicit token permissions, leaving them open to potential tag-hijacking supply-chain attacks and overly permissive default GITHUB_TOKEN write access.
**Learning:** Using tags like `@v4` or `@v7` is insecure because tag references are mutable and can be modified or spoofed by malicious actors in the upstream dependency repository, leading to code injection during CI/CD runs.
**Prevention:** Always pin third-party GitHub Actions to their secure, immutable full-length commit SHAs and explicitly restrict permissions to `contents: read` at the job level.
