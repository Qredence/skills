"""
Golden evaluation examples for task_planner
"""

# Define golden examples as a list of (input, expected_output) tuples
GOLDEN_EXAMPLES = [
    (
        {
            "goal": "Build a web application",
            "constraints": ["Limited budget", "2-week timeline"],
            "resources": ["Python", "React", "Cloud hosting"]
        },
        {
            "plan": {
                "subtasks": [
                    {
                        "id": "task1",
                        "description": "Design database schema",
                        "dependencies": [],
                        "estimated_effort": "2 days"
                    },
                    {
                        "id": "task2",
                        "description": "Implement backend API",
                        "dependencies": ["task1"],
                        "estimated_effort": "5 days"
                    },
                    {
                        "id": "task3",
                        "description": "Build frontend UI",
                        "dependencies": ["task2"],
                        "estimated_effort": "5 days"
                    },
                    {
                        "id": "task4",
                        "description": "Deploy to cloud",
                        "dependencies": ["task3"],
                        "estimated_effort": "2 days"
                    }
                ],
                "execution_order": ["task1", "task2", "task3", "task4"]
            },
            "reasoning": "Sequential approach prioritizing core infrastructure first"
        }
    ),
    (
        {
            "goal": "Organize a conference",
            "constraints": ["Virtual event", "500 attendees"],
            "resources": ["Zoom", "Marketing team", "Budget: $10k"]
        },
        {
            "plan": {
                "subtasks": [
                    {
                        "id": "task1",
                        "description": "Select conference platform",
                        "dependencies": [],
                        "estimated_effort": "1 week"
                    },
                    {
                        "id": "task2",
                        "description": "Recruit speakers",
                        "dependencies": [],
                        "estimated_effort": "3 weeks"
                    }
                ],
                "execution_order": ["task1", "task2"]
            },
            "reasoning": "Parallel tasks with platform selection as critical path"
        }
    ),
]


def get_golden_examples():
    """Return golden evaluation examples"""
    return GOLDEN_EXAMPLES
