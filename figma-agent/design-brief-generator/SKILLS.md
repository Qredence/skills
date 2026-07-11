---
name: design-brief-generator
description: "Turns a rough, informal ask (a Slack message, a one-line ticket, a verbal request) into a structured design brief -- problem statement, goals, constraints, success criteria, and open questions -- ready to scope work against. Use at the start of a project when the ask is underspecified."
---

# Design Brief Generator

## Purpose
Turn a rough or underspecified ask into a structured brief that makes the actual scope of work clear.

## Operating Role
Act as a Figma design-file producer for this specific skill. Create or structure the requested artifact in the file when enough context exists; otherwise return the smallest useful plan and ask only for blocking inputs.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- A project starts from a vague or informal request and needs to be scoped before design work begins

## Required Inputs
- The raw ask (pasted message, ticket, or description)
- Any related context available via connectors (related tickets, prior discussion, existing research)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Extract the brief from evidence first. Keep goals, non-goals, audience, constraints, and success criteria separate.

## Workflow
1. Restate the problem being solved in one or two sentences, distinguishing the underlying user/business problem from any specific solution that may have been mentioned in the raw ask (a stated solution is not necessarily the right one).
2. State the goal(s): what should be true after this is shipped, ideally in terms that could be measured or at least clearly observed.
3. List known constraints: technical, timeline, platform, brand, or scope constraints mentioned or reasonably inferable -- mark inferred constraints as such.
4. List explicit non-goals: what this project is deliberately not trying to solve, to prevent scope creep (infer reasonable non-goals if none were stated, and flag them as suggested rather than confirmed).
5. Propose success criteria: how it will be evident this worked (metric, qualitative signal, or explicit stakeholder sign-off criteria).
6. List every open question the raw ask leaves unanswered, so these can be resolved before design work starts rather than discovered midway.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Do not invent scope, deadlines, or success metrics as if they were given -- clearly separate "stated", "inferred", and "open question".

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return the created or proposed Figma structure first, then list assumptions, variants/states covered, and follow-up decisions. If changes were applied, include exactly what changed.
- Skill-specific format: Problem statement -> Goals -> Constraints -> Non-goals -> Success criteria -> Open questions, each section labeled by confidence (stated/inferred).
