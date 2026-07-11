---
name: design-change-diff
description: "Summarizes what changed in a design between two points in time (e.g. two branches, two versions, or before/after a review round) in plain language useful to engineers and PMs, rather than a generic 'design updated' note. Use when communicating design changes to a broader team, especially after a branch merge or a revision round."
---

# Design Change Diff

## Purpose
Turn a design's version/branch history into a clear, plain-language summary of what actually changed and why it matters.

## Operating Role
Act as a Figma design-file reviewer for this specific skill. Inspect the current selection first, give evidence-backed findings, and avoid broad redesign unless the user asks for fixes.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- After merging a branch back into a main file
- After a revision round, to tell stakeholders/engineers what changed since they last looked

## Required Inputs
- The two points to compare (e.g. branch vs main, or two named versions) -- use version history if available
- The intended audience (engineers need implementation-relevant detail; PMs/stakeholders need product-relevant detail)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Compare frames structurally before summarizing: layout, content, components, tokens, interactions, and annotations.

## Workflow
1. Identify every screen/component that differs between the two points.
2. For each change, classify it: new screen/flow added, existing screen restructured, visual-only tweak (spacing/color/copy), content/copy change, new or removed state, or interaction/prototype change.
3. Write each change as a plain-language statement of what's different and, where relevant, why (e.g. "Checkout now shows a shipping cost estimate before payment -- addresses the surprise-cost complaint from the last round of feedback" rather than just "added text layer to Checkout").
4. Flag changes that affect implementation specifically for an engineering audience: new states, changed component props/variants, new interactions, or changed content rules.
5. Flag changes that affect scope/timeline for a PM audience: new screens, new flows, or anything that looks like scope growth relative to the original requirement.
6. Order the summary by impact (structural/flow changes first, then visual/content polish) rather than by the order changes happened to be made.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Do not just restate layer-level diffs (e.g. "moved layer X 4px") -- synthesize into what a reader actually needs to know; mention pure micro-adjustments only in a brief "minor polish" line at the end.

## Finding Quality Rules
- Lead with the highest-impact issues, not the order discovered.
- Tie each finding to a specific frame, layer, component, variable, style, comment, interaction, or supplied source.
- Include severity only when it changes priority: Blocker, High, Medium, or Low.
- Pair every finding with an exact fix, replacement, or next decision.
- Separate confirmed findings from assumptions, recommendations, and unverified areas.

## Output Contract
Start with a 3-line summary: scope reviewed, blocker count, and highest-risk issue. Then provide grouped findings with location, severity, evidence, and exact fix. End with skipped or unverified areas.
- Skill-specific format: "What changed" grouped by impact level, with a one-line "why it matters" per item, plus a short "minor polish" catch-all line.
