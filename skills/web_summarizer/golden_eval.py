"""
Golden evaluation examples for web_summarizer
"""

# Define golden examples as a list of (input, expected_output) tuples
GOLDEN_EXAMPLES = [
    (
        {
            "url": "https://example.com/article1",
            "max_length": 100
        },
        {
            "summary": "A concise summary of the article discussing key concepts...",
            "key_points": ["Key point 1", "Key point 2", "Key point 3"]
        }
    ),
    (
        {
            "url": "https://example.com/article2",
            "max_length": 150
        },
        {
            "summary": "An informative summary covering the main topics...",
            "key_points": ["Important finding", "Notable conclusion"]
        }
    ),
]


def get_golden_examples():
    """Return golden evaluation examples"""
    return GOLDEN_EXAMPLES
