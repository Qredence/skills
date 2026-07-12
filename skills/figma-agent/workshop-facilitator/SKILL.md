---
name: workshop-facilitator
description: "Structures a FigJam board for a specific workshop format (brainstorm, retrospective, kickoff, design studio) with sections, prompts, and suggested timing, ready for a team to fill in live or async. Use when setting up a workshop board from scratch."
---

# Workshop Facilitator

## Purpose
Set up a well-structured FigJam board for a specific workshop format, with clear sections and prompts, so participants can jump straight into contributing.

## Operating Role
Act as a Figma design-file producer for this specific skill. Create or structure the requested artifact in the file when enough context exists; otherwise return the smallest useful plan and ask only for blocking inputs.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Setting up a board ahead of a brainstorm, retro, kickoff, or design studio session

## Required Inputs
- The workshop type and goal (ask if not specified -- common types: brainstorm, sprint retro, project kickoff, design studio/crazy-8s, pre-mortem)
- Expected group size and whether the session is live/synchronous or async
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Build a board that can be explained in under a minute: goal, sections, prompts, timing, and synthesis space.

## Workflow
1. Choose a structure matching the workshop type: e.g. retro -> "What went well / What didn't / Action items" columns; kickoff -> "Goals / Non-goals / Risks / Open questions / Timeline" sections; brainstorm -> a central problem statement with radiating idea zones or "How Might We" prompts; design studio -> individual sketch zones followed by a share-and-critique zone.
2. Write a clear, specific prompt at the top of each section -- avoid vague prompts like "thoughts?" in favor of a concrete question that's easy to respond to.
3. Add a section for the session goal/objective at the top of the board so contributors know what "done" looks like.
4. If the session is timed, add a suggested agenda with rough time allocations per section as a sticky or text block.
5. For live sessions, add a few starter stickies or an icebreaker prompt to reduce blank-canvas hesitation.
6. Reserve a clearly labeled space for synthesis/next steps at the end of the board, to be filled in after the session (pairs well with sticky-synthesis and affinity-mapping once the session has content).

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Keep the structure simple enough to explain in one sentence per section -- an overly elaborate board structure suppresses participation more than it helps.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return the created or proposed Figma structure first, then list assumptions, variants/states covered, and follow-up decisions. If changes were applied, include exactly what changed.
- Skill-specific format: The board structure (sections + prompts + optional timing) ready to build directly on the canvas.
