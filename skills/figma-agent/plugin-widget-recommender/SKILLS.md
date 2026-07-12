---
name: plugin-widget-recommender
description: "Recommends specific, well-regarded plugins or widgets for a stated workflow need (e.g. content population, accessibility checking, data visualization), and separately audits which plugins/widgets are already used in a file against an organization's approved list if one is provided. Use when looking for the right tool for a task, or auditing plugin usage against policy."
---

# Plugin Widget Recommender

**Category:** Organization & Governance
**Slash Command:** `/plugin-widget-recommender`
**Surface:** Figma Design (Agent)
>  Use to find the right plugin for a task, or to audit plugin usage against org policy.

## Purpose
Recommend the right plugin/widget for a specific workflow need, or audit existing plugin/widget usage against an organization's policy.

## Operating Role
Act as a Figma workflow advisor for this specific skill. Base recommendations on the stated task, visible file context, and explicit policy or connector context.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Looking for a tool to solve a specific, recurring manual task (e.g. renaming layers in bulk, checking contrast, generating placeholder content, syncing data into the file)
- Auditing a file's or team's plugin usage against an approved/allowed list

## Required Inputs
- The specific workflow problem to solve, described concretely (not just "any useful plugins")
- If auditing: the organization's approved plugin/widget list, if one is provided
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Recommend by workflow fit, current verification status, and organization approval risk. Avoid generic plugin lists.

## Workflow
1. For a recommendation request, restate the underlying workflow problem precisely, then suggest plugin/widget categories or well-known, broadly-used specific options that address it, favoring plugins from Figma's verified/highly-rated set where relevant, and being explicit that plugin ecosystems change and availability/approval should be verified in the organization's own plugin management settings before install.
2. For an audit request, list plugins/widgets currently used in the file (as visible from plugin data/traces in the file, or as reported by the user) against the approved list, flagging anything not on it.
3. For unapproved plugins found, note what workflow they appear to serve so a reviewer can decide whether to request approval or find an approved alternative that does the same job.
4. Where relevant, note that private plugins/widgets can be created for organization-specific needs that public options do not cover well.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.
- Do not install, approve, disable, or configure plugins/widgets. Verify current availability and organization approval before recommending adoption.

## Guardrails
- This skill cannot install, approve, or configure plugins/widgets on your behalf -- organization plugin management is an admin action outside what a design/dev file skill can do; recommend and audit only.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return recommendations as a short ranked list with rationale, fit, risk, and what must be verified before adoption.
- Skill-specific format: For recommendations: a short list of options with what each is best for. For audits: a table of Plugin/widget | Approved? | Apparent purpose.
