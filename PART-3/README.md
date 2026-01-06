# Integration Test: Project Creation (API + Web + Mobile)

This test validates the complete project lifecycle across layers:

1. Create a project via API
2. Verify the project appears in the Web UI
3. Validate accessibility on mobile (BrowserStack)
4. Ensure tenant isolation (project not visible to other company)

Key assumptions:
- Token comes from secrets storage in real systems
- Test data cleanup handled by nightly jobs or API cleanup
- BrowserStack credentials configured via environment variables
- UI may need waits due to async loading
