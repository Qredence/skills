---
on:
  pull_request:
    paths:
      - 'skills/**'
permissions:
  pull-requests: write
  contents: read
tools:
  github:
env:
  LITELLM_PROXY_URL: ${{ secrets.LITELLM_PROXY_URL }}
  LITELLM_API_KEY: ${{ secrets.LITELLM_API_KEY }}
  LITELLM_DEFAULT_MODEL: ${{ vars.LITELLM_DEFAULT_MODEL }}
  LITELLM_SMALL_MODEL: ${{ vars.LITELLM_SMALL_MODEL }}
---

# PR Review for New Skills
Review the pull request that modifies or adds new skills in the `skills/` directory.
- Check if the skill documentation is clear and follows the expected format.
- Ensure any provided scripts in the skill are safe and correctly referenced.
- Provide actionable feedback as a PR comment.
