"""
Task Planner skill implementation
"""
from typing import Type, List
from pathlib import Path
import dspy

from skills.core.base import Skill


class TaskPlannerSignature(dspy.Signature):
    """DSPy signature for task planning"""
    
    goal: str = dspy.InputField(desc="High-level goal or objective to plan for")
    constraints: str = dspy.InputField(desc="Constraints as comma-separated list")
    resources: str = dspy.InputField(desc="Available resources as comma-separated list")
    plan: str = dspy.OutputField(desc="Generated execution plan with subtasks")
    reasoning: str = dspy.OutputField(desc="Explanation of the planning approach")


class TaskPlannerModule(dspy.Module):
    """DSPy module for task planning"""
    
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought(TaskPlannerSignature)
    
    def forward(
        self,
        goal: str,
        constraints: List[str] = None,
        resources: List[str] = None
    ) -> dspy.Prediction:
        """
        Create a task plan
        
        Args:
            goal: High-level goal or objective
            constraints: List of constraints
            resources: List of available resources
            
        Returns:
            DSPy prediction with plan and reasoning
        """
        if constraints is None:
            constraints = []
        if resources is None:
            resources = []
        
        # Convert lists to comma-separated strings for DSPy
        constraints_str = ", ".join(constraints) if constraints else "None"
        resources_str = ", ".join(resources) if resources else "None"
        
        result = self.prog(
            goal=goal,
            constraints=constraints_str,
            resources=resources_str
        )
        
        return result


class TaskPlanner(Skill):
    """
    Plans and breaks down complex tasks into actionable subtasks
    """
    
    def __init__(self, metadata_path: Path = None):
        if metadata_path is None:
            metadata_path = Path(__file__).parent / "skill.yaml"
        super().__init__(metadata_path)
        self._module = TaskPlannerModule()
        self._signature = TaskPlannerSignature
    
    def get_module(self) -> dspy.Module:
        """Return the DSPy Module"""
        return self._module
    
    def get_signature(self) -> Type[dspy.Signature]:
        """Return the DSPy Signature"""
        return self._signature
