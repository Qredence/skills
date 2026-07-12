---
name: prototype-from-flow
description: "Builds a clickable, connected prototype from a described user flow, a flow diagram, or a set of already-designed screens -- wiring up prototype connections, triggers, and actions end to end. Use when screens exist (or a flow is described) but aren't yet linked into a testable prototype."
---

# Prototype From Flow

## Purpose
Turn a described or diagrammed user flow, or a set of unconnected screens, into a fully wired, clickable prototype.

## Operating Role
Act as a Figma design-file producer for this specific skill. Create or structure the requested artifact in the file when enough context exists; otherwise return the smallest useful plan and ask only for blocking inputs.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Screens are designed but not yet connected
- A flow diagram (from FigJam, a PRD, or a description) needs to become a testable prototype

## Required Inputs
- The flow definition: an ordered description of screens and the decisions/actions that move between them, or a reference to a FigJam flow/diagram
- The starting frame for the prototype
- Any states that should be reflected in the flow (e.g. logged in vs out, empty cart vs full cart)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Map the full flow as nodes and decision points before wiring interactions.
- Use one canonical happy path plus explicit branches; avoid adding speculative routes.

## Workflow
1. Map every step in the flow to an existing frame; if a needed screen does not exist yet, flag it rather than inventing new UI, unless asked to also design the missing screens.
2. For each transition, pick the trigger that matches the interaction (On click/tap for buttons and links, On drag for swipe/scroll interactions, After delay for auto-advancing content, key/gamepad triggers only if explicitly relevant).
3. Choose the action that matches the intent: Navigate to for standard transitions, Open overlay for modals/menus/tooltips, Swap state for interactive component state changes, Scroll to for in-page jumps, Back for return navigation.
4. Choose an animation (Instant, Dissolve, Smart animate, Move in/out, Push, Slide) that matches the platform convention and the weight of the transition -- Smart animate for element continuity between similar frames, Push/Slide for standard mobile navigation.
5. Set overlay behavior (position, background, close-on-click-outside) explicitly for every overlay rather than leaving defaults unconsidered.
6. Wire every branch described in the flow, including error/cancel/back paths, not just the primary happy path.
7. Set the prototype's starting frame and device frame/background to match the intended viewing context.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Do not silently skip a described branch because the destination screen does not exist -- flag it explicitly so it is not mistaken for "done".

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return the created or proposed Figma structure first, then list assumptions, variants/states covered, and follow-up decisions. If changes were applied, include exactly what changed.
- Skill-specific format: A confirmation list of every connection made (from -> trigger -> action -> to) plus a list of any flow steps that couldn't be wired and why.
