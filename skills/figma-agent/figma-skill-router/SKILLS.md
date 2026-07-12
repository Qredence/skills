---
name: figma-skill-router
description: "Use when a Figma Design agent must choose among installed Figma skills for a request or design-file context."
---

# Figma Skill Router

Select and hand off to one installed Figma skill. Skip it when a narrower matching skill is already invoked.

## Route

1. Read the goal and strongest context: selection, page, library, comments, branch, PRD, code, or none.
2. Choose the narrowest index entry. Use check skills for “audit”, “review”, or “find”; use apply skills for “fix”, “apply”, “migrate”, or “standardize”.
3. Return one primary skill and only one dependent next skill. Ask once only for missing required input.

## Capability Gate

Treat prototype or interaction work as a plan unless interaction editing is supported. State limits for exports, vector editing, or diagrams/data visualizations; use external context only when supplied.

## Catalogue Index

Use the request noun and verb to choose within the relevant group.

| Area | Installed skills |
| --- | --- |
| Discover and define | `design-brief-generator`, `build-from-prd`, `persona-builder`, `journey-map-builder`, `workshop-facilitator`, `affinity-mapping`, `sticky-synthesis`, `competitive-teardown`, `deck-from-outline` |
| Content and brand | `content-inventory`, `content-tone-review`, `microcopy-generator`, `localization-readiness`, `brand-kit-asset-generator` |
| Layout and construction | `container-layout-normalizer`, `responsive-breakpoint-check`, `spacing-scale-enforcer`, `figma-to-code-component`, `base-ui-primitive-composition`, `shadcn-component-structure`, `cva-variant-generator` |
| Components and libraries | `component-audit`, `component-naming-sync`, `library-health-report`, `follow-ds-guidelines`, `design-tokens-sync`, `legacy-styles-to-variables`, `apply-color-variables`, `color-token-format-normalizer`, `semantic-color-audit` |
| Review and quality | `accessibility-audit`, `heuristic-evaluation`, `design-crit`, `visual-consistency-check`, `states-completeness-check`, `site-launch-checklist`, `prototype-qa`, `animation-consistency-check` |
| Prototypes and motion | `prototype-from-flow`, `wire-up-interactions`, `variable-driven-prototype`, `motion-spec-generator` |
| Code, changes, and handoff | `code-connect-mapper`, `dev-handoff-prep`, `handoff-summary`, `token-tailwind-theme-sync`, `tailwind-class-order-check`, `design-change-diff`, `branch-review-summary` |
| File operations | `file-cleanup`, `rename-layers-batch`, `naming-convention-enforcer` |
| Collaboration and utilities | `comment-triage`, `plugin-widget-recommender` |

## Tie-Breakers

Use `component-audit` for one set, `library-health-report` library-wide; `microcopy-generator` writes, `content-inventory` enumerates. `design-crit` is broad feedback, `heuristic-evaluation` usability, `accessibility-audit` access; `journey-map-builder` maps experience, `prototype-from-flow` plans screens. For unmatched requests: `design-brief-generator` (new) or `design-crit` (improve).

## Handoff

Return only:

```markdown
Primary skill: `<skill-name>`
Why: <request and context in one sentence>
Scope: <selection, page, file, or assumption>
Next skill: `<skill-name>` — <only when needed>
Capability note: <only when relevant>
```

Do not list alternatives, perform the work, or send two skills to the same artifact.
