"""
Real DSPy signatures from fleet-rlm.

These examples show production-ready signatures used in fleet-rlm's
DSPy modules. They demonstrate best practices for signature design,
type safety, and structured outputs.

Source: src/fleet_rlm/dspy_modules/signatures.py
"""

import dspy

# Note: These use Pydantic models for type-safe outputs
# See typed_models.py for the output model definitions

class TaskAnalysis(dspy.Signature):
    """Analyze a task with structured output.

    Returns a validated TaskAnalysisOutput with type-safe fields.
    """

    task: str = dspy.InputField(desc="The user's task description")
    analysis: TaskAnalysisOutput = dspy.OutputField(
        desc="Structured analysis of task including complexity, capabilities, and tool needs"
    )


class TaskRouting(dspy.Signature):
    """Route a task to agents with structured output.

    CRITICAL: Assign minimum necessary agents to complete task efficiently.
    Do not over-assign. For simple tasks, a single agent is preferred.

    Returns a validated RoutingDecisionOutput with type-safe fields.
    """

    task: str = dspy.InputField(desc="The task to route")
    team: str = dspy.InputField(desc="Description of available agents")
    context: str = dspy.InputField(desc="Optional execution context")
    current_date: str = dspy.InputField(desc="Current date for time-sensitive decisions")

    decision: RoutingDecisionOutput = dspy.OutputField(
        desc="Structured routing decision with agents, mode, subtasks, and tools"
    )


class EnhancedTaskRouting(dspy.Signature):
    """Advanced task routing with structured output.

    Optimizes for latency and token usage by pre-planning tool usage
    and setting execution constraints.

    Returns a validated RoutingDecisionOutput with all routing fields.
    """

    task: str = dspy.InputField(desc="Task to be routed")
    team_capabilities: str = dspy.InputField(desc="Capabilities of available agents")
    available_tools: str = dspy.InputField(desc="List of available tools")
    current_context: str = dspy.InputField(desc="Execution context")
    handoff_history: str = dspy.InputField(desc="History of agent handoffs")
    workflow_state: str = dspy.InputField(desc="Current state of workflow")

    decision: RoutingDecisionOutput = dspy.OutputField(
        desc="Complete routing decision with agents, mode, tools, and strategy"
    )


class QualityAssessment(dspy.Signature):
    """Assess result quality with structured output.

    Returns a validated QualityAssessmentOutput with score and feedback.
    """

    task: str = dspy.InputField(desc="The original task")
    result: str = dspy.InputField(desc="The result produced by agent")

    assessment: QualityAssessmentOutput = dspy.OutputField(
        desc="Quality assessment with score (0-10), missing elements, and improvements"
    )


class ProgressEvaluation(dspy.Signature):
    """Evaluate progress with structured output.

    Returns a validated ProgressEvaluationOutput with action and feedback.
    """

    task: str = dspy.InputField(desc="The original task")
    result: str = dspy.InputField(desc="The current result")

    evaluation: ProgressEvaluationOutput = dspy.OutputField(
        desc="Progress evaluation with action (complete/refine/continue) and feedback"
    )


class ToolPlan(dspy.Signature):
    """Generate tool plan with structured output.

    Returns a validated ToolPlanOutput with ordered tool list.
    """

    task: str = dspy.InputField(desc="The task to execute")
    available_tools: str = dspy.InputField(desc="List of available tools")

    plan: ToolPlanOutput = dspy.OutputField(
        desc="Tool plan with ordered list of tools and reasoning"
    )


class WorkflowStrategy(dspy.Signature):
    """Select workflow strategy with structured output.

    Selects between:
    - 'handoff': For simple, linear, or real-time tasks (Low latency).
    - 'standard': For complex, multi-step, or quality-critical tasks (High robustness).
    - 'fast_path': For trivial queries (Instant).

    Returns a validated WorkflowStrategyOutput.
    """

    task: str = dspy.InputField(desc="The user's request or task")
    complexity_analysis: str = dspy.InputField(desc="Analysis of task complexity")

    strategy: WorkflowStrategyOutput = dspy.OutputField(
        desc="Workflow strategy with mode (handoff/standard/fast_path) and reasoning"
    )


class SimpleResponse(dspy.Signature):
    """Directly answer a simple task or query."""

    task: str = dspy.InputField(desc="The simple task or question")
    answer: str = dspy.OutputField(desc="Concise and accurate answer")


class GroupChatSpeakerSelection(dspy.Signature):
    """Select the next speaker in a group chat."""

    history: str = dspy.InputField(desc="The conversation history so far")
    participants: str = dspy.InputField(desc="List of available participants and their roles")
    last_speaker: str = dspy.InputField(desc="The name of last speaker")

    next_speaker: str = dspy.OutputField(desc="The name of next speaker, or 'TERMINATE' to end")
    reasoning: str = dspy.OutputField(desc="Reasoning for selection")


class AgentInstructionSignature(dspy.Signature):
    """Generate instructions for an agent based on its role and context."""

    role: str = dspy.InputField(desc="The role of agent (e.g., 'coder', 'researcher')")
    description: str = dspy.InputField(desc="Description of agent's responsibilities")
    task_context: str = dspy.InputField(desc="Context of current task or workflow")

    agent_instructions: str = dspy.OutputField(desc="Detailed system instructions for agent")


class PlannerInstructionSignature(dspy.Signature):
    """Generate specialized instructions for Planner/Orchestrator agent."""

    available_agents: str = dspy.InputField(desc="List of available agents and their descriptions")
    workflow_goal: str = dspy.InputField(desc="The goal of current workflow")

    agent_instructions: str = dspy.OutputField(desc="Detailed instructions for Planner agent")


class WorkflowNarration(dspy.Signature):
    """Transform raw workflow events into a user-friendly narrative."""

    events_log: str = dspy.InputField(desc="Chronological log of workflow events")
    narrative: str = dspy.OutputField(
        desc="Concise, natural language summary of workflow execution"
    )


# Key Design Patterns Demonstrated

# 1. Type-Safe Outputs with Pydantic Models
#    All signatures use Pydantic models for output validation
#    Example: analysis: TaskAnalysisOutput = dspy.OutputField(...)

# 2. Clear Field Descriptions
#    Every field has a descriptive purpose
#    Example: task: str = dspy.InputField(desc="The user's task description")

# 3. Critical Constraints in Docstrings
#    Important constraints are documented in the signature docstring
#    Example: "CRITICAL: Assign minimum necessary agents to complete task efficiently."

# 4. Multiple Input Contexts
#    Signatures accept various context inputs for better decisions
#    Example: team, context, current_date, handoff_history

# 5. Specialized Signatures for Specific Tasks
#    Each signature has a single, clear purpose
#    Example: TaskAnalysis, TaskRouting, QualityAssessment

# 6. Backward Compatibility Aliases
#    Aliases for old signature names maintain compatibility
#    Example: TypedTaskAnalysis = TaskAnalysis


# Usage Examples

def example_task_analysis():
    """Example of using TaskAnalysis signature."""
    from fleet_rlm.signatures import TaskAnalysis

    # Create module with signature
    analyze_task = dspy.Predict(TaskAnalysis)

    # Use the signature
    result = analyze_task(
        task="Write a Python function to calculate Fibonacci numbers"
    )

    # Access structured output
    print(f"Analysis: {result.analysis}")
    print(f"Complexity: {result.analysis.complexity}")
    print(f"Required tools: {result.analysis.required_tools}")


def example_task_routing():
    """Example of using TaskRouting signature."""
    from fleet_rlm.signatures import TaskRouting

    # Create module with signature
    route_task = dspy.Predict(TaskRouting)

    # Use the signature
    result = route_task(
        task="Research quantum computing applications",
        team="Researcher: web search and information gathering, Coder: code generation",
        context="Academic research project",
        current_date="2024-01-15"
    )

    # Access routing decision
    print(f"Agents: {result.decision.agents}")
    print(f"Mode: {result.decision.mode}")
    print(f"Confidence: {result.decision.confidence}")


def example_quality_assessment():
    """Example of using QualityAssessment signature."""
    from fleet_rlm.signatures import QualityAssessment

    # Create module with signature
    assess_quality = dspy.Predict(QualityAssessment)

    # Use the signature
    result = assess_quality(
        task="Summarize the document",
        result="This is a brief summary of the document..."
    )

    # Access quality assessment
    print(f"Score: {result.assessment.score}")
    print(f"Missing elements: {result.assessment.missing_elements}")
    print(f"Improvements: {result.assessment.improvements}")


# Best Practices from fleet-rlm

# 1. Always use Pydantic models for structured outputs
#    This ensures type safety and validation

# 2. Include all necessary context in input fields
#    Don't rely on implicit context

# 3. Document critical constraints in signature docstrings
#    Helps LLMs understand important rules

# 4. Keep signatures focused on a single purpose
#    Don't create "do everything" signatures

# 5. Use clear, descriptive field names
#    Avoid abbreviations and vague names

# 6. Provide examples in descriptions when helpful
#    Example: "Type: 'handoff', 'standard', or 'fast_path'"

# 7. Maintain backward compatibility when refactoring
#    Use aliases for old signature names

if __name__ == "__main__":
    print("fleet-rlm DSPy Signature Examples")
    print("=" * 60)
    print("\nThese are real signatures from fleet-rlm.")
    print("See src/fleet_rlm/dspy_modules/signatures.py for the source.")
