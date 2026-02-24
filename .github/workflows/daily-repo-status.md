---
on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:
permissions:
  contents: read
  issues: read
  pull-requests: read
safe-outputs:
  create-issue:
    title-prefix: "[repo status] "
    labels: [report]
tools:
  github:
env:
  LITELLM_PROXY_URL: ${{ secrets.LITELLM_PROXY_URL }}
  LITELLM_API_KEY: ${{ secrets.LITELLM_API_KEY }}
  LITELLM_DEFAULT_MODEL: ${{ vars.LITELLM_DEFAULT_MODEL }}
  LITELLM_SMALL_MODEL: ${{ vars.LITELLM_SMALL_MODEL }}
---

# Daily Repo Status Report
Create a daily status report for maintainers. Include
- Recent repository activity (issues, PRs, discussions, releases, code changes)
- Progress tracking, goal reminders and highlights
- Project status and recommendations
- Actionable next steps for maintainers

Keep it concise and link to the relevant issues/PRs.