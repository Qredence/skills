---
name: prototype-qa
description: "Walks every connection in a prototype end to end, testing that each leads where intended, has no dead ends, and that overlays/back actions behave correctly, then reports every broken or missing link. Use before sharing a prototype for testing, review, or a stakeholder demo."
---

# Prototype QA

## Purpose
Catch every broken, missing, or misbehaving connection in a prototype before it is shared or demoed.

## Operating Role
Act as a Figma design-file reviewer for this specific skill. Inspect the current selection first, give evidence-backed findings, and avoid broad redesign unless the user asks for fixes.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Before sending a prototype link to stakeholders, researchers, or reviewers
- After a round of screen additions/edits that could have silently broken existing connections

## Required Inputs
- The prototype's starting frame (or all starting frames, if there are multiple flows in one file)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Test paths as a user would: start frame, happy path, branch paths, overlays, back behavior, dead ends, and state resets.

## Workflow
1. Enumerate every frame in the prototype and every outgoing connection from it (trigger, action, destination).
2. From the starting frame, walk each path exhaustively, following every button/link/interactive element, including overlays, nested overlays, and back actions.
3. Flag dead ends: interactive-looking elements (buttons, links, list items) with no connection at all.
4. Flag broken destinations: connections pointing to a frame that's been deleted, renamed out of the flow, or clearly the wrong target for the label (e.g. a "Cancel" button that navigates forward instead of back).
5. Flag overlay issues: overlays with no close action, or an "outside click closes" setting that conflicts with the intended behavior (e.g. a confirmation dialog that should require an explicit choice but can be dismissed by clicking outside).
6. Flag orphaned frames: frames that exist in the file but are never reached by any connection from the starting frame.
7. Check state-driven logic (variables/conditionals) actually branches into every intended state at least once during the walk.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Report the exact frame and element for every issue so it can be found and fixed quickly, not just "some links are broken".

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Start with a 3-line summary: scope reviewed, blocker count, and highest-risk issue. Then provide grouped findings with location, severity, evidence, and exact fix. End with skipped or unverified areas.
- Skill-specific format: A findings list grouped as: Dead ends, Broken destinations, Overlay issues, Orphaned frames, State-logic gaps -- each with frame/element names.
