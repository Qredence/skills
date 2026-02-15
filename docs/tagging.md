# Skill Tagging Taxonomy

AgenticFleet-optimized tag taxonomy for DSPy skills. Use these tags to make skills discoverable and enable semantic routing.

## Tag Format

- Lowercase
- Hyphenated for multi-word tags (e.g., `task-management`)
- Underscores acceptable for snake_case (e.g., `tool_use`)
- No spaces

## Core Reasoning

Skills that involve reasoning, planning, or decision-making:

- **`reasoning`** - General reasoning and inference
- **`planning`** - Task decomposition and planning
- **`decision`** - Decision-making and choice selection
- **`decomposition`** - Breaking down complex problems
- **`reflection`** - Self-reflection and critique
- **`evaluation`** - Evaluation and assessment

**Examples**:
- Task planner → `planning`, `decomposition`
- Code reviewer → `reasoning`, `evaluation`
- Decision maker → `decision`, `reasoning`

## Memory & Knowledge

Skills that manage or retrieve information:

- **`memory`** - Memory storage and recall
- **`retrieval`** - Information retrieval
- **`knowledge`** - Knowledge base interaction
- **`world_model`** - World modeling and simulation
- **`graph`** - Graph-based knowledge
- **`embedding`** - Vector embeddings and similarity

**Examples**:
- RAG system → `retrieval`, `knowledge`, `embedding`
- Memory manager → `memory`, `storage`
- Knowledge graph query → `knowledge`, `graph`

## Execution & Orchestration

Skills that execute tasks or orchestrate other skills:

- **`orchestration`** - Multi-skill coordination
- **`tool_use`** - External tool invocation
- **`execution`** - Task execution
- **`workflow`** - Workflow management
- **`routing`** - Request routing and delegation

**Examples**:
- Agent orchestrator → `orchestration`, `routing`
- Tool caller → `tool_use`, `execution`
- Workflow engine → `workflow`, `orchestration`

## IO & Transformation

Skills that transform or process data:

- **`transform`** - Data transformation
- **`summarization`** - Text summarization
- **`translation`** - Language translation
- **`formatting`** - Format conversion
- **`extraction`** - Information extraction
- **`classification`** - Classification and categorization

**Examples**:
- Document transformer → `transform`, `formatting`
- Web summarizer → `summarization`, `extraction`
- Language translator → `translation`, `transform`

## Safety & Governance

Skills related to safety and compliance:

- **`safety`** - Safety checks and validation
- **`validation`** - Input/output validation
- **`moderation`** - Content moderation
- **`compliance`** - Policy compliance

**Examples**:
- Content moderator → `moderation`, `safety`
- Input validator → `validation`, `safety`
- Policy checker → `compliance`, `validation`

## System-Level

Meta-skills and system components:

- **`agent`** - Agent-level functionality
- **`skill`** - Skill management
- **`planner`** - Planning systems
- **`meta`** - Meta-level operations
- **`control`** - Control flow

**Examples**:
- Skill registry → `skill`, `meta`
- Agent controller → `agent`, `control`
- Meta-planner → `planner`, `meta`

## Domain-Specific

Add domain tags for specialized areas:

### Content & Media
- **`nlp`** - Natural language processing
- **`vision`** - Computer vision
- **`audio`** - Audio processing
- **`multimodal`** - Multiple modalities

### Data & Code
- **`web`** - Web scraping and interaction
- **`documents`** - Document processing
- **`code`** - Code analysis and generation
- **`data`** - Data processing and analysis

### Applications
- **`content-creation`** - Content generation
- **`research`** - Research and investigation
- **`automation`** - Automation tasks
- **`development`** - Software development
- **`analysis`** - Analysis and insights
- **`organization`** - Organization and management

## Behavioral Tags

Describe skill characteristics:

- **`deterministic`** - Deterministic outputs
- **`streaming`** - Streaming support
- **`batch`** - Batch processing
- **`interactive`** - Interactive mode
- **`low-latency`** - Low latency optimized
- **`high-accuracy`** - High accuracy focus

## Tagging Guidelines

### Required Tags

Every skill must have **at least one tag** from:
1. Core Reasoning OR IO & Transformation
2. Optionally: Domain-Specific
3. Optionally: Behavioral

### Example Tag Sets

**Web Summarizer**:
```yaml
tags:
  - summarization
  - extraction
  - web
  - nlp
```

**Task Planner**:
```yaml
tags:
  - planning
  - decomposition
  - reasoning
  - orchestration
```

**Document Transformer**:
```yaml
tags:
  - transform
  - formatting
  - documents
```

**Code Reviewer**:
```yaml
tags:
  - evaluation
  - reasoning
  - code
  - analysis
```

### Avoid Over-Tagging

- Use 2-5 tags typically
- Focus on primary functionality
- Don't add obvious or redundant tags
- Be specific rather than generic

### Tag Consistency

- Use existing tags when possible
- Propose new tags via skill proposals
- Follow naming conventions
- Check catalog for similar skills

## Tag Discovery

Find skills by tag:

```bash
# List skills with specific tag
python tools/validate.py --list --tag nlp

# Programmatically
from skills_core import discover_skills
skills = discover_skills(Path("skills"))
nlp_skills = [s for s in skills if 'nlp' in s.tags]
```

## AgenticFleet Integration

Tags enable semantic routing in AgenticFleet:

```python
# Route based on intent and skill tags
planner.route_to_skill(
    intent="summarize web content",
    required_tags=["summarization", "web"]
)
```

## Extending the Taxonomy

To propose new tags:

1. Open a skill proposal issue
2. Justify the new tag
3. Provide example use cases
4. Show how it differs from existing tags

Maintainers will evaluate and potentially add to this taxonomy.
