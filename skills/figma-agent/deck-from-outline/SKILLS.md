---
name: deck-from-outline
description: "Turns a text outline, bullet list, or document into a structured Figma Slides deck -- one slide per section, using consistent layout patterns and the file's existing slide template/theme. Use when the content already exists (as an outline or doc) and needs to become a presentable deck."
---

# Deck From Outline

## Purpose
Convert an existing outline or document into a structured, presentable Figma Slides deck.

## Operating Role
Act as a Figma design-file producer for this specific skill. Create or structure the requested artifact in the file when enough context exists; otherwise return the smallest useful plan and ask only for blocking inputs.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Content already exists as an outline, doc, or bullet list and needs to become slides

## Required Inputs
- The source outline/document (pasted or via connector)
- The existing deck template/theme to use, if one exists in the file; otherwise ask about the intended audience/purpose to pick an appropriate structure (pitch, update, training, etc.)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Turn each outline section into one slide or a small slide group; preserve narrative pacing rather than dumping bullets.

## Workflow
1. Read the outline and identify natural slide breaks: typically one slide per top-level section or major point, not one slide per sentence.
2. For each slide, choose a layout appropriate to its content type: title/section-divider layout for section breaks, a single-strong-statement layout for key takeaways, a list/comparison layout for enumerated points, a data/chart layout for anything quantitative mentioned in the source.
3. Reduce each slide's text to presentation-appropriate density -- headlines and short supporting points, not paragraphs copied verbatim from the source document; note any place where meaningful nuance from the source was cut so it can be added as speaker notes instead of on-slide text.
4. Apply the deck's existing template/theme (fonts, colors, logo placement) consistently across every slide rather than reinventing layout per slide.
5. Add a clear opening slide (title, presenter/date if relevant) and a closing slide (summary or call to action) even if the source outline didn't explicitly include them.
6. Where the source had supporting detail that shouldn't be cut but also does not belong on-slide, add it as speaker notes on the relevant slide.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Never fabricate data or claims not present in the source outline to "fill out" a slide -- a shorter, accurate slide is better than a padded, inaccurate one.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return the created or proposed Figma structure first, then list assumptions, variants/states covered, and follow-up decisions. If changes were applied, include exactly what changed.
- Skill-specific format: The built deck, plus a slide-by-slide map back to the source outline section it came from.
