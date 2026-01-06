## Flakiness Issues

### 1. No Wait Time After Clicking the Login Button
Assertions execute before the navigation or UI finishes loading, causing false failures.

### 2. Strict URL Matching
Tests fail when the application adds query parameters to the redirect URL.

### 3. Intermittent 2FA Behavior
Two-factor authentication appears only for some sessions.  
When it shows up unexpectedly, the test crashes because the flow is not handled.

### 4. Variable Tenant Data Load Times
Tenant data loads at different speeds.  
For Company2, project cards may not be ready when assertions run.

### 5. Case-Sensitive Text Assertions
Assertions fail when the same text appears with different capitalization across environments.
