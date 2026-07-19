# Qredence Skills

Practical Figma design and product skills for AI agents.

This repository is a curated catalogue you can install with [`skills.sh`](https://www.skills.sh/docs). Each skill is a single `SKILL.md` with a clear trigger description and an evidence-backed workflow agents can follow inside Figma.

---

## Quickstart

```bash
npx skills@latest add qredence/skills
```

1. Choose skills from the Figma catalogue.
2. Choose the agents where you want them installed.
3. Invoke a skill by name or by describing the task it covers.

List discoverable skills from a clean directory:

```bash
npx skills@latest add qredence/skills --list
```

Only packages under [`skills/figma-agent/`](skills/figma-agent/) should appear.

---

## How skills work

| Piece | Role |
| --- | --- |
| `skills/figma-agent/<name>/SKILL.md` | Canonical, installable skill document |
| YAML frontmatter (`name`, `description`) | Discovery and routing for agents |
| Workflow sections | Concrete steps, limits, and output shape |

There is no duplicate upload document. `SKILL.md` is the only skill file.

Skills are scoped for Figma design work: selection-first by default, evidence tied to layers/frames/variables, and clear limits when code or admin context is unavailable.

---

## Catalogue

**57 skills** in [`skills/figma-agent/`](skills/figma-agent/). Grouped by job below; open a folder for the full `SKILL.md`.

### Accessibility & usability

| Skill | Use when |
| --- | --- |
| [`accessibility-audit`](skills/figma-agent/accessibility-audit/) | Checking WCAG-oriented issues visible in Figma before handoff |
| [`heuristic-evaluation`](skills/figma-agent/heuristic-evaluation/) | Running a Nielsen-heuristics usability pass on a flow |
| [`localization-readiness`](skills/figma-agent/localization-readiness/) | Catching clipping, RTL, and translation risks before localization |
| [`states-completeness-check`](skills/figma-agent/states-completeness-check/) | Verifying empty, loading, error, and interaction states exist |
| [`visual-consistency-check`](skills/figma-agent/visual-consistency-check/) | Unifying spacing, alignment, and style across a multi-screen flow |

### Design system & tokens

| Skill | Use when |
| --- | --- |
| [`apply-color-variables`](skills/figma-agent/apply-color-variables/) | Binding hard-coded colors to existing Color variables |
| [`component-audit`](skills/figma-agent/component-audit/) | Health-checking a component set before publish |
| [`design-tokens-sync`](skills/figma-agent/design-tokens-sync/) | Reconciling Figma variables with code tokens |
| [`follow-ds-guidelines`](skills/figma-agent/follow-ds-guidelines/) | Auditing a frame against the published design system |
| [`legacy-styles-to-variables`](skills/figma-agent/legacy-styles-to-variables/) | Migrating hard-coded styles onto shared variables |
| [`library-health-report`](skills/figma-agent/library-health-report/) | Cleaning unused, duplicate, or undocumented library assets |
| [`naming-convention-enforcer`](skills/figma-agent/naming-convention-enforcer/) | Renaming layers and components to a stated convention |
| [`rename-layers-batch`](skills/figma-agent/rename-layers-batch/) | Bulk renaming with a simple rule or find/replace |
| [`semantic-color-audit`](skills/figma-agent/semantic-color-audit/) | Catching raw palette usage where semantic tokens belong |
| [`shadcn-theme-variables`](skills/figma-agent/shadcn-theme-variables/) | Creating or repairing semantic shadcn theme variables in Figma |
| [`spacing-scale-enforcer`](skills/figma-agent/spacing-scale-enforcer/) | Mapping arbitrary spacing onto the project scale |

### Components & code mapping

| Skill | Use when |
| --- | --- |
| [`base-ui-primitive-composition`](skills/figma-agent/base-ui-primitive-composition/) | Composing overlays from Base UI / Radix-style primitives |
| [`code-connect-mapper`](skills/figma-agent/code-connect-mapper/) | Planning Figma ↔ code mappings for Code Connect |
| [`component-naming-sync`](skills/figma-agent/component-naming-sync/) | Aligning Figma and code component/prop naming |
| [`cva-variant-generator`](skills/figma-agent/cva-variant-generator/) | Generating `cva` configs from Figma variants |
| [`figma-to-code-component`](skills/figma-agent/figma-to-code-component/) | Translating a selected frame into a first-pass implementation |
| [`screenshot-to-component`](skills/figma-agent/screenshot-to-component/) | Recreating a UI screenshot as a structured Figma component |
| [`shadcn-component-structure`](skills/figma-agent/shadcn-component-structure/) | Matching shadcn/ui component conventions in generated code |
| [`tailwind-class-order-check`](skills/figma-agent/tailwind-class-order-check/) | Cleaning Tailwind class order and conflicts |
| [`token-tailwind-theme-sync`](skills/figma-agent/token-tailwind-theme-sync/) | Syncing Figma variables into a Tailwind/shadcn theme |

### Layout & responsive

| Skill | Use when |
| --- | --- |
| [`container-layout-normalizer`](skills/figma-agent/container-layout-normalizer/) | Normalizing container widths, max-width, and padding |
| [`responsive-breakpoint-check`](skills/figma-agent/responsive-breakpoint-check/) | Verifying auto layout and constraints across breakpoints |
| [`site-launch-checklist`](skills/figma-agent/site-launch-checklist/) | Pre-publish review for a Figma Sites project |

### Prototyping & motion

| Skill | Use when |
| --- | --- |
| [`animation-consistency-check`](skills/figma-agent/animation-consistency-check/) | Auditing easing, duration, and motion character across a file |
| [`motion-spec-generator`](skills/figma-agent/motion-spec-generator/) | Documenting duration/easing specs for engineering |
| [`prototype-from-flow`](skills/figma-agent/prototype-from-flow/) | Wiring screens into an end-to-end clickable prototype |
| [`prototype-qa`](skills/figma-agent/prototype-qa/) | Walking every prototype link for dead ends and broken paths |
| [`variable-driven-prototype`](skills/figma-agent/variable-driven-prototype/) | Building stateful prototypes with variables and conditions |
| [`wire-up-interactions`](skills/figma-agent/wire-up-interactions/) | Adding or fixing specific prototype interactions |

### Research, workshops & strategy

| Skill | Use when |
| --- | --- |
| [`affinity-mapping`](skills/figma-agent/affinity-mapping/) | Clustering open-ended qualitative data into themes |
| [`competitive-teardown`](skills/figma-agent/competitive-teardown/) | Extracting actionable insights from a competitor flow |
| [`design-brief-generator`](skills/figma-agent/design-brief-generator/) | Turning a vague ask into a structured design brief |
| [`journey-map-builder`](skills/figma-agent/journey-map-builder/) | Building a journey map from research or a described experience |
| [`persona-builder`](skills/figma-agent/persona-builder/) | Creating an evidence-grounded persona from research |
| [`sticky-synthesis`](skills/figma-agent/sticky-synthesis/) | Clustering FigJam stickies into themes and takeaways |
| [`workshop-facilitator`](skills/figma-agent/workshop-facilitator/) | Structuring a FigJam board for a workshop format |

### Content

| Skill | Use when |
| --- | --- |
| [`content-inventory`](skills/figma-agent/content-inventory/) | Exporting every user-facing string for review or translation |
| [`content-tone-review`](skills/figma-agent/content-tone-review/) | Checking copy against voice-and-tone guidelines |
| [`microcopy-generator`](skills/figma-agent/microcopy-generator/) | Drafting buttons, empty states, errors, and tooltips |

### Delivery & collaboration

| Skill | Use when |
| --- | --- |
| [`figma-skill-router`](skills/figma-agent/figma-skill-router/) | Choosing the right installed Figma skill for a request |
| [`branch-review-summary`](skills/figma-agent/branch-review-summary/) | Summarizing a design branch for reviewers |
| [`build-from-prd`](skills/figma-agent/build-from-prd/) | Turning a PRD into screens, states, and flows |
| [`comment-triage`](skills/figma-agent/comment-triage/) | Sorting open comments into actionable buckets |
| [`deck-from-outline`](skills/figma-agent/deck-from-outline/) | Building a Figma Slides deck from an outline |
| [`design-change-diff`](skills/figma-agent/design-change-diff/) | Explaining what changed between two design versions |
| [`design-crit`](skills/figma-agent/design-crit/) | Getting a structured critique before a wider review |
| [`dev-handoff-prep`](skills/figma-agent/dev-handoff-prep/) | Final Dev Mode readiness pass before engineering |
| [`file-cleanup`](skills/figma-agent/file-cleanup/) | Reorganizing pages and archiving stale exploration |
| [`handoff-summary`](skills/figma-agent/handoff-summary/) | Writing a concise context handoff for a teammate |
| [`brand-kit-asset-generator`](skills/figma-agent/brand-kit-asset-generator/) | Generating on-brand marketing/social asset variants |
| [`plugin-widget-recommender`](skills/figma-agent/plugin-widget-recommender/) | Recommending plugins/widgets for a workflow need |
| [`color-token-format-normalizer`](skills/figma-agent/color-token-format-normalizer/) | Aligning colors to shadcn CSS-variable / HSL format |

---

## Suggested starting set

If you are installing for the first time, these cover the most common loops:

| Skill | Why |
| --- | --- |
| [`accessibility-audit`](skills/figma-agent/accessibility-audit/) | Catch checkable a11y issues early |
| [`component-audit`](skills/figma-agent/component-audit/) | Keep shared components healthy |
| [`design-tokens-sync`](skills/figma-agent/design-tokens-sync/) | Keep design and code tokens aligned |
| [`figma-to-code-component`](skills/figma-agent/figma-to-code-component/) | Bridge a selected design into code |
| [`prototype-from-flow`](skills/figma-agent/prototype-from-flow/) | Make flows testable quickly |
| [`dev-handoff-prep`](skills/figma-agent/dev-handoff-prep/) | Close the loop before engineering |

---

## Repository layout

```text
skills/figma-agent/<skill-name>/SKILL.md   # installable catalogue (source of truth)
archive/                                   # historical material (not installable)
scripts/                                   # init + validate helpers
tests/                                     # catalogue integrity checks
AGENTS.md                                  # maintainer workflow
```

| Path | Audience |
| --- | --- |
| [`skills/figma-agent/`](skills/figma-agent/) | Users and agents — active skills |
| [`archive/`](archive/) | Maintainers — historical packages as `README.md` only |
| [`AGENTS.md`](AGENTS.md) | Contributors — create, validate, release |
| [`SECURITY.md`](SECURITY.md) | Vulnerability reporting |

---

## Contributing

New skills belong under `skills/figma-agent/` as a kebab-case directory with a matching frontmatter `name`.

```bash
uv run python scripts/init_skill.py my-new-skill
# edit skills/figma-agent/my-new-skill/SKILL.md
uv run python scripts/validate_skills.py
```

Full workflow: [AGENTS.md](AGENTS.md) and [CONTRIBUTING](.github/CONTRIBUTING.md).

---

## License

[MIT](LICENSE)
