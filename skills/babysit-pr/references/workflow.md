# PR Babysitter — Detailed Workflow

## Core Workflow (Detailed)

1. When asked to "monitor"/"watch"/"babysit" a PR, start with `--watch` unless doing a one-shot diagnostic.
2. Run the watcher script to snapshot PR/CI/review state (or consume each streamed snapshot from `--watch`).
3. Inspect the `actions` list in the JSON response.
4. If `diagnose_ci_failure` is present, inspect failed run logs and classify the failure.
5. If the failure is likely caused by the current branch, patch code locally, commit, and push.
6. If `process_review_comment` is present, inspect surfaced review items and decide whether to address them.
7. If a review item is actionable and correct, patch code locally, commit, and push.
8. If the failure is likely flaky/unrelated and `retry_failed_checks` is present, rerun failed jobs with `--retry-failed-now`.
9. If both actionable review feedback and `retry_failed_checks` are present, prioritize review feedback first; a new commit will retrigger CI.
10. On every loop, verify mergeability / merge-conflict status (e.g., via `gh pr view`).
11. After any push or rerun action, immediately return to step 1 and continue polling on the updated SHA/state.
12. If using `--watch` before pausing to patch/commit/push, relaunch `--watch` immediately after the push in the same turn.
13. Repeat polling until the PR is green + review-clean + mergeable, `stop_pr_closed` appears, or a user-help-required blocker is reached.
14. Maintain terminal/session ownership: while babysitting is active, keep consuming watcher output in the same turn.

## CI Failure Classification

Use `gh` commands to inspect failed runs before deciding to rerun:

- `gh run view <run-id> --json jobs,name,workflowName,conclusion,status,url,headSha`
- `gh run view <run-id> --log-failed`

**Branch-related**: logs point to changed code (compile/test/lint/typecheck/snapshots/static analysis in touched areas).

**Flaky/unrelated**: logs show transient infra/external issues (timeouts, runner provisioning failures, registry/network outages, GitHub Actions infra errors).

If classification is ambiguous, perform one manual diagnosis attempt before choosing rerun.

See `heuristics.md` for a concise checklist.

## Review Comment Handling

The watcher surfaces review items from:
- PR issue comments
- Inline review comments
- Review submissions (COMMENT / APPROVED / CHANGES_REQUESTED)

It surfaces Codex reviewer bot feedback and trusted human review authors (repo OWNER/MEMBER/COLLABORATOR, plus the authenticated operator).

On a fresh watcher state file, existing pending review feedback may be surfaced immediately.

When agreeing with an actionable comment:
1. Patch code locally.
2. Commit with `codex: address PR review feedback (#<n>)`.
3. Push to the PR head branch.
4. Resume watching on the new SHA immediately.
5. If in `--watch` mode, restart `--watch` immediately after the push.

If resolved in GitHub, treat as non-actionable unless new unresolved follow-up appears.

## Git Safety Rules

- Work only on the PR head branch.
- Avoid destructive git commands.
- Do not switch branches unless necessary to recover context.
- Before editing, check for unrelated uncommitted changes. If present, stop and ask the user.
- After each successful fix, commit and `git push`, then re-run the watcher.
- Do not run multiple concurrent `--watch` processes for the same PR/state file.
- A push is not a terminal outcome; continue the monitoring loop.

Commit message defaults:
- `codex: fix CI failure on PR #<n>`
- `codex: address PR review feedback (#<n>)`

## Monitoring Loop Pattern

1. Run `--once`.
2. Read `actions`.
3. Check if PR is merged/closed; if so, report and stop.
4. Check CI summary, new review items, and mergeability/conflict status.
5. Diagnose CI failures and classify branch-related vs flaky/unrelated.
6. Process actionable review comments before flaky reruns.
7. Retry failed checks only when `retry_failed_checks` is present and not about to replace the current SHA.
8. If pushed a commit or triggered a rerun, report briefly and continue polling.
9. After a review-fix push, restart `--watch` in the same turn.
10. If everything is passing, mergeable, not blocked on review, and no unaddressed items, report success and stop.
11. If blocked on a user-help-required issue, report the blocker and stop.
12. Otherwise sleep per polling cadence and repeat.

Prefer `--watch` for monitoring requests. Use repeated `--once` only for debugging or explicit one-shot checks.
Do not stop to ask whether to continue; continue autonomously until a strict stop condition or explicit user interruption.

## Polling Cadence

- While CI is not green: poll every 1 minute.
- After CI turns green: start at 1m, back off exponentially (1m, 2m, 4m, 8m, 16m, 32m), cap at 1 hour.
- Reset to 1m whenever anything changes (new commit, check status, review comments, mergeability).
- If CI stops being green: return to 1-minute polling.
- If PR is merged/closed: stop immediately.

## Output Expectations

- Provide concise progress updates; full summary only at terminal state.
- During long unchanged periods, summarize only status changes plus occasional heartbeats.
- Push confirmations and intermediate CI snapshots are progress updates only.
- When CI first goes all green, emit one celebratory update: `🚀 CI is all green! X/X passed. Still on watch for review approval.`
- Do not send final summary while watcher is still running unless a strict stop condition is confirmed.
