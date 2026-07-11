---
name: journey-map-builder
description: "Builds a user journey map on a FigJam (or design) canvas from research notes, transcripts, or a described experience -- stages, actions, thoughts/feelings, pain points, and opportunities per stage. Use when synthesizing research into a shareable journey artifact."
---

# Journey Map Builder

## Purpose
Turn research notes or a described user experience into a structured journey map.

## Operating Role
Act as a Figma design-file producer for this specific skill. Create or structure the requested artifact in the file when enough context exists; otherwise return the smallest useful plan and ask only for blocking inputs.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- After user research (interviews, surveys, session recordings) needs to be synthesized into a shared artifact
- When scoping a project and a clear before/during/after picture of the user's experience would help

## Required Inputs
- The source material: research notes, meeting transcripts (via connector), or a described experience
- The persona/user type the journey is for, if more than one is relevant
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Build the map from evidence-backed stages, touchpoints, user actions, emotions, pain points, and opportunities. Mark guessed stages.

## Workflow
1. Identify the journey's scope (start and end point) and break it into a small number of clear stages (typically 4-7) that represent meaningful phases, not every micro-step.
2. For each stage, extract: the user's actions, their thoughts/feelings (quote directly from research where possible), touchpoints/channels involved, pain points, and any positive moments worth preserving.
3. Identify opportunities per stage -- a specific, actionable idea suggested by the pain point or positive moment, not a vague "improve this".
4. Lay the map out as a grid: stages as columns, the rows above (actions, thoughts/feelings, touchpoints) and pain points/opportunities as the bottom rows, so it reads left-to-right as the experience unfolds.
5. Include a visual emotion indicator per stage (e.g. a simple line or icon showing relative highs/lows) to make the emotional arc scannable at a glance.
6. Cite the source for major claims (e.g. which interview a quote came from) so the map remains traceable to real research.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Do not fabricate quotes or data points not present in the source material -- mark any inferred (not directly sourced) content as an assumption.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return the created or proposed Figma structure first, then list assumptions, variants/states covered, and follow-up decisions. If changes were applied, include exactly what changed.
- Skill-specific format: The journey map structure (stages x rows) built directly on the canvas, plus a short list of the top 3 opportunities surfaced.
