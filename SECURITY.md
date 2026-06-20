# Security Policy

## Educational Content Issues

If an example encourages unsafe configuration, exposes secrets, weakens access controls, or creates a credible exploitation path, report it privately rather than opening a public issue. Use GitHub's private vulnerability reporting feature when enabled.

Include the affected file, risk, reproduction conditions, and a suggested correction if possible. Do not include real credentials or customer data.

## Supported Content

The latest default branch is maintained. This repository contains educational material and synthetic data, not a supported Splunk app or production deployment package.

## Safe Use

Test administrative examples in a non-production environment. Review commands against the official documentation for your exact Splunk edition and version. Keep tokens in environment variables or a secret manager, scope service accounts narrowly, verify TLS, and never commit exported configuration containing secrets.

