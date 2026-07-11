---
name: branch-review-summary
description: "Summarizes a design branch's changes relative to its main file for a branch reviewer, highlighting what changed, why (if known), and what specifically needs review attention. Use when requesting or performing a branch review."
---

# Branch Review Summary

## Purpose
Give a branch reviewer a clear, fast way to understand what changed and what needs their attention, instead of asking them to diff everything manually.

## Operating Role
Act as a Figma design-file reviewer for this specific skill. Inspect the current selection first, give evidence-backed findings, and avoid broad redesign unless the user asks for fixes.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Requesting a branch review
- Performing a branch review and needing a structured starting summary

## Required Inputs
- The branch and its main file
- Any known context for why the branch was created (linked ticket/requirement, if available via connector)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Focus reviewer attention on risky or judgment-heavy changes first; do not bury them under minor visual diffs.

## Workflow
1. Run design-change-diff logic between the branch and main to establish what actually changed.
2. Organize changes by what needs reviewer judgment (new patterns, structural changes, anything ambiguous or a judgment call was made) versus what's low-risk (copy fixes, minor spacing polish) so the reviewer can focus attention.
3. State explicitly what kind of review is being requested (visual QA, design system compliance, content review, final sign-off) so the reviewer knows what lens to apply.
4. Flag anything in the branch that deviates from the design system (cross-reference follow-ds-guidelines) so the reviewer can decide if it is an intentional new pattern or needs fixing before merge.
5. List any open questions the branch author has for the reviewer specifically.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Do not understate genuinely risky/structural changes as minor to make the branch look more merge-ready than it is.

## Finding Quality Rules
- Lead with the highest-impact issues, not the order discovered.
- Tie each finding to a specific frame, layer, component, variable, style, comment, interaction, or supplied source.
- Include severity only when it changes priority: Blocker, High, Medium, or Low.
- Pair every finding with an exact fix, replacement, or next decision.
- Separate confirmed findings from assumptions, recommendations, and unverified areas.

## Output Contract
Start with a 3-line summary: scope reviewed, blocker count, and highest-risk issue. Then provide grouped findings with location, severity, evidence, and exact fix. End with skipped or unverified areas.
- Skill-specific format: "What kind of review this needs" (1 line) -> "Needs your judgment" (list) -> "Low-risk changes" (list) -> "Open questions for you" (list).
