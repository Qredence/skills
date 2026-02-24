---
on:
  issue_comment:
    types: [created]
permissions:
  contents: write
  issues: write
  pull-requests: write
tools:
  github:
  bash:
env:
  LITELLM_PROXY_URL: ${{ secrets.LITELLM_PROXY_URL }}
  LITELLM_API_KEY: ${{ secrets.LITELLM_API_KEY }}
  LITELLM_DEFAULT_MODEL: ${{ vars.LITELLM_DEFAULT_MODEL }}
  LITELLM_SMALL_MODEL: ${{ vars.LITELLM_SMALL_MODEL }}
---

# PR Babysitter

If a user comments `@skills/babysit-pr` on a Pull Request:
1. Check out the repository.
2. Read the instructions and guidelines from `skills/babysit-pr/SKILL.md`.
3. Analyze the PR's code changes, commits, and description.
4. Follow the skill's instructions to provide a comprehensive review, comment on specific lines, and optionally fix issues by pushing commits if instructed by the skill.
5. Provide a summary comment when finished.