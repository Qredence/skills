---
name: wire-up-interactions
description: "Adds or fixes specific prototype interactions (triggers, actions, animations, overlay settings) on an already-largely-connected prototype, based on a precise spec of what should happen. Use for targeted interaction work, as opposed to prototype-from-flow which builds an entire flow from scratch."
---

# Wire Up Interactions

## Purpose
Add or correct specific prototype interactions against a precise spec, without rebuilding the whole flow.

## Operating Role
Act as a Figma design-file producer for this specific skill. Create or structure the requested artifact in the file when enough context exists; otherwise return the smallest useful plan and ask only for blocking inputs.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- A prototype mostly works but a specific interaction is missing, wrong, or needs refinement
- Adding a new one-off interaction (e.g. a new overlay, a new hover state) to an existing prototype

## Required Inputs
- The exact interaction(s) needed: source element, trigger, destination, and desired feel
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Change only the named interaction unless the user asks for broader prototype QA. Verify trigger, action, destination, and transition.

## Workflow
1. Locate the source element and check for any existing conflicting interaction on the same trigger; decide whether to replace or add as an additional interaction.
2. Set the trigger precisely (On click, On hover, While hovering, On drag, While pressing, Mouse enter/leave, Key/gamepad, After delay, Mouse down/up) -- the most common source of "prototype does not feel right" bugs is the wrong trigger type.
3. Set the action (Navigate to, Open/close/swap overlay, Swap state, Change to, Scroll to, Back, Open link, Open node, Set variable, Conditional) matching the intent exactly, including any variable or condition logic required for state-driven behavior.
4. Configure animation curve and duration deliberately: prefer spring easing with tuned bounce/duration for natural motion, or ease-in-out with an explicit duration for precise, repeatable timing -- avoid leaving default "instant" when a transition is meant to feel considered.
5. If the interaction is on a component with variants/interactive-component states, confirm it swaps to the correct variant rather than a visually similar but semantically wrong one.
6. Test the specific interaction after wiring, describing exactly what happens on trigger.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Do not remove or alter unrelated existing interactions on the same frame while fixing the requested one.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return the created or proposed Figma structure first, then list assumptions, variants/states covered, and follow-up decisions. If changes were applied, include exactly what changed.
- Skill-specific format: A short list: what was added/changed, the exact trigger -> action configuration, and how to verify it.
