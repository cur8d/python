# Sentinel Security Journal

This journal contains critical security learnings specific to this project.

## 2026-03-10 - Secure GitHub Actions Pinned to Immutable SHAs
**Vulnerability:** Workflows were referencing a non-existent version tag `actions/checkout@v7` and a mutable major version tag `jdx/mise-action@v4`. Using non-existent or moving tags exposes the repository to supply chain and tag-spoofing attacks if an attacker registers or hijacks the version tag.
**Learning:** Third-party actions should not rely on moving major version tags or non-existent tags. Moving tags are mutable, and their associated commits can change, potentially introducing untested or malicious code.
**Prevention:** Pin all third-party GitHub Actions to secure, immutable 40-character full-length commit SHAs, and append a comment indicating the human-readable version (e.g. `# v4.4.0`). Dependabot can then be configured to automatically update these SHAs.
