---
on:
  workflow_run:
    workflows: ["Python CI", "CI", "ci"]
    types:
      - completed
permissions:
  issues: write
  actions: read
tools:
  github:
env:
  LITELLM_PROXY_URL: ${{ secrets.LITELLM_PROXY_URL }}
  LITELLM_API_KEY: ${{ secrets.LITELLM_API_KEY }}
  LITELLM_DEFAULT_MODEL: ${{ vars.LITELLM_DEFAULT_MODEL }}
  LITELLM_SMALL_MODEL: ${{ vars.LITELLM_SMALL_MODEL }}
---

# Automated Test Failure Analysis
Analyze the failed test logs from the completed CI workflow.
- If the workflow failed, read the logs to identify the root cause of the test failures.
- Create a new issue describing the failure, the suspected cause, and potential fixes.
- If it's a known flaky test, note that in the issue.
