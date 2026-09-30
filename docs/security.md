# Security

Credentials are never committed or copied from raw evidence into normalized artifacts. Acquisition uses
environment variables, Databricks secret scopes, or Azure Key Vault integrations chosen by the platform
team. Static assessment redacts keys matching password, token, secret, API key, credential, authorization,
cookie, or private key. External calls always require explicit authorization.
