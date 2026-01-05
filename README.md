# starlink_connectivity_tools.py

## Starlink Enterprise API

Official API for managing Starlink accounts and devices, primarily targeted at enterprise users. It allows programmatic control over subscriptions, service lines, user terminals, and more.

### Description

**Purpose:** Manage accounts, addresses, data usage, routers, service lines, subscriptions, TLS configurations, and user terminals.

**Base URL:** `https://web-api.starlink.com/enterprise`

**Documentation:** 
- Available via Swagger UI at [https://web-api.starlink.com/enterprise/swagger/index.html](https://web-api.starlink.com/enterprise/swagger/index.html)
- Interactive endpoints can be explored there or at related documentation sites

### Authentication

The Starlink Enterprise API uses **OpenID Connect (OIDC)** for authentication.

**Well-known configuration URL:** `https://web-api.starlink.com/enterprise/api/auth/.well-known/openid-configuration`

**Authentication Process:**
1. Obtain tokens from the OIDC provider
2. Attach tokens to API requests using Bearer token in headers

**Service Accounts:**
- Service accounts can be created in the Starlink account settings under "Service Accounts"
- These accounts are specifically designed for API access
- Use service account credentials to authenticate and make API calls programmatically