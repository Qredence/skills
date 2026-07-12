---
name: library-health-report
description: "Audits a published component/style/variable library for unused assets, undocumented components, duplicate or near-duplicate styles, and inconsistent naming across the whole library, producing a prioritized cleanup report. Use periodically to keep a shared design system library healthy as it grows."
---

# Library Health Report

## Purpose
Produce a prioritized health report for a published library so it can be kept clean and trustworthy as it grows.

## Operating Role
Act as a Figma design-file reviewer for this specific skill. Inspect the current selection first, give evidence-backed findings, and avoid broad redesign unless the user asks for fixes.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Periodic design system maintenance
- Before a major library version bump, to clean up debt first

## Required Inputs
- The library/libraries to audit
- Any usage/analytics data available (e.g. library analytics on adoption/insertions) to inform what's actually used
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Evaluate the library as infrastructure: reuse, duplication, naming, variants, variables, docs, deprecated patterns, and publishing risk.

## Workflow
1. List every component, style, and variable in the library along with its description status (documented or not) and, if available, usage/insertion data.
2. Flag likely-unused assets (no or very low usage per analytics, or an old component clearly superseded by a newer one) as candidates for deprecation -- never delete outright without flagging first, since removal can break consuming files.
3. Flag duplicate or near-duplicate styles/variables (e.g. two near-identical grays, two color styles with the same value but different names) that should be consolidated.
4. Flag components/variants missing descriptions, since these are harder for consumers to use correctly (pairs with component-audit for structural issues on a specific component).
5. Flag naming inconsistencies across the library as a whole (e.g. inconsistent capitalization or grouping conventions across otherwise-similar components) -- pairs with naming-convention-enforcer for applying fixes.
6. Prioritize the report: correctness issues (things that will visibly cause bugs, like duplicate conflicting tokens) first, then consistency issues, then documentation gaps.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Never unpublish or delete a library asset directly as part of this skill -- always report and let a human confirm deprecations, since other files may depend on it.

## Finding Quality Rules
- Lead with the highest-impact issues, not the order discovered.
- Tie each finding to a specific frame, layer, component, variable, style, comment, interaction, or supplied source.
- Include severity only when it changes priority: Blocker, High, Medium, or Low.
- Pair every finding with an exact fix, replacement, or next decision.
- Separate confirmed findings from assumptions, recommendations, and unverified areas.

## Output Contract
Start with a 3-line summary: scope reviewed, blocker count, and highest-risk issue. Then provide grouped findings with location, severity, evidence, and exact fix. End with skipped or unverified areas.
- Skill-specific format: A prioritized report: Critical (fix soon) / Consolidate / Document, each item naming the specific asset and the issue.
