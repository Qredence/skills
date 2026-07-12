---
name: sticky-synthesis
description: "Clusters and summarizes stickies on a FigJam board into themes, counts, and a synthesized takeaway for each theme. Use after a brainstorm, retro, or research session has generated a lot of loose stickies that need to become an actionable summary."
---

# Sticky Synthesis

## Purpose
Turn a pile of loose FigJam stickies into a small number of clear, named themes with a synthesized takeaway each.

## Operating Role
Act as a Figma design-file producer for this specific skill. Create or structure the requested artifact in the file when enough context exists; otherwise return the smallest useful plan and ask only for blocking inputs.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- After a brainstorm, retro, workshop, or research synthesis session on a FigJam board

## Required Inputs
- The board or section of the board to synthesize
- Whether there's already a rough clustering (color-coding, spatial grouping) to respect, or whether to cluster from scratch
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Respect existing clusters when they are clearly intentional, but recluster when spatial grouping is accidental or noisy.

## Workflow
1. Read every sticky's text (and note author/color if meaningfully used, e.g. color = category).
2. Group stickies into themes by underlying meaning, not just keyword overlap -- two stickies with different words can be the same theme, and two with similar words can be different themes.
3. Name each theme clearly and concisely (a short phrase, not a single word), and count how many stickies fall into it.
4. Write a one- or two-sentence synthesized takeaway per theme -- what the group of stickies is collectively saying, not just a list of what's in it.
5. Call out any strong outliers that do not fit a theme but seem important enough to preserve rather than discard.
6. Order themes by sticky count (most-represented first) unless another ordering is more meaningful (e.g. chronological for a retro's "went well / didn't go well / actions").
7. If asked to update the board directly, visually group the stickies to match the clustering and add a theme-label sticky/section header per group.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Do not over-cluster into one giant theme or under-cluster into as many themes as stickies -- aim for a number of themes a team could realistically act on (typically 3-8).

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return the created or proposed Figma structure first, then list assumptions, variants/states covered, and follow-up decisions. If changes were applied, include exactly what changed.
- Skill-specific format: A theme list: Theme name (sticky count) -> synthesized takeaway, followed by an "outliers" list if any.
