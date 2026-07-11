---
name: brand-kit-asset-generator
description: "Generates a set of on-brand marketing/social assets (e.g. social post variants, banner sizes, a simple one-pager) from a project's brand kit (colors, fonts, logo, existing templates), for use in Figma Buzz or general marketing asset production. Use when a brand kit exists and multiple sized/format variants of an asset are needed quickly."
---

# Brand Kit Asset Generator

## Purpose
Produce multiple on-brand marketing asset variants quickly and consistently from an existing brand kit.

## Operating Role
Act as a Figma design-file producer for this specific skill. Create or structure the requested artifact in the file when enough context exists; otherwise return the smallest useful plan and ask only for blocking inputs.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Multiple sizes/formats of the same core asset are needed (e.g. a social campaign across several platforms)
- A brand kit (colors, type, logo, templates) already exists to pull from

## Required Inputs
- The brand kit source (existing library/styles/variables, logo assets, and any existing templates to match)
- The exact set of sizes/formats needed (ask for the list if not given -- common social sizes vary significantly by platform and shouldn't be guessed silently)
- The core message/content that should appear across variants
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Keep the same message hierarchy across sizes. Recompose layouts per aspect ratio instead of scaling one frame blindly.

## Workflow
1. Identify the brand's core visual system from the kit: primary/secondary colors as variables or styles, approved fonts and their hierarchy, logo lockup(s) and their minimum clear space/size rules, and any existing template layouts to follow.
2. For each required size/format, adapt the core layout to fit -- this usually means re-flowing, not just scaling, since aspect ratio changes need different compositional choices (e.g. a square post vs. a tall story format).
3. Keep messaging hierarchy consistent across variants (the same primary message should be the most prominent element in every size) even as the layout adapts.
4. Apply brand colors/fonts/logo exactly from the kit -- no ad hoc substitutions, even for a size where the exact brand color combination feels visually awkward; flag that tension instead of quietly deviating.
5. Name and organize each variant clearly (by platform/size) for easy export.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Do not alter the logo (recoloring, stretching, cropping) beyond what the brand kit is usage guidelines explicitly allow.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return the created or proposed Figma structure first, then list assumptions, variants/states covered, and follow-up decisions. If changes were applied, include exactly what changed.
- Skill-specific format: The generated variants, organized and named by size/platform, plus a note on any brand-kit ambiguity encountered.
