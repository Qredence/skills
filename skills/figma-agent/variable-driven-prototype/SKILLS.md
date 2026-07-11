---
name: variable-driven-prototype
description: "Sets up Figma variables and conditional prototype logic to make a prototype genuinely stateful -- e.g. a login flow that remembers auth state, a cart that updates a count and total, or a settings toggle that persists across screens. Use when a prototype needs to demonstrate real interactive logic, not just static screen-to-screen navigation."
---

# Variable Driven Prototype

## Purpose
Make a prototype behave statefully using Figma variables, conditionals, and expressions, instead of only linear screen jumps.

## Operating Role
Act as a Figma design-file producer for this specific skill. Create or structure the requested artifact in the file when enough context exists; otherwise return the smallest useful plan and ask only for blocking inputs.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- The prototype needs to reflect state that persists or changes across screens (login status, form input echoed later, a running total, a toggle setting)
- A demo needs to show branching logic driven by user choices, not a fixed path

## Required Inputs
- What state needs to be tracked (name, type -- boolean/number/string/color -- and its possible values)
- Where the state changes (which interactions set it) and where it is read (which screens/conditions depend on it)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Model state as a small variable table before wiring. Test every branch and reset condition.

## Workflow
1. Create a variable for each piece of state needed, using a clear name and the correct type, in a collection scoped appropriately (local to the prototype unless it should be a shared design variable too).
2. Wire "Set variable" actions on the interactions that change state (e.g. a toggle's On click sets a boolean, quantity stepper's clicks increment/decrement a number).
3. Bind variables to visible properties where state should be reflected directly (e.g. binding a text layer to a number variable for a live count, or a variable-bound instance-swap for a toggle's visual state).
4. Add conditional actions where the destination or displayed content depends on a variable's value (e.g. "if isLoggedIn is true, navigate to Dashboard, else navigate to Sign in"), using expressions for any calculated logic (e.g. totals, formatted strings).
5. Verify initial variable values are set sensibly for the prototype's starting frame so the first view is correct before any interaction happens.
6. Test every branch of every conditional to confirm it resolves to the intended destination/state.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Keep variable names and structure simple enough that a teammate could understand the logic by reading the variables panel alone; avoid deeply nested conditionals where a simpler structure would do.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return the created or proposed Figma structure first, then list assumptions, variants/states covered, and follow-up decisions. If changes were applied, include exactly what changed.
- Skill-specific format: A variable table (name, type, purpose) plus a logic summary of every conditional/set-variable action added and what triggers it.
