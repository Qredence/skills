"""
Golden evaluation examples for doc_transformer
"""

# Define golden examples as a list of (input, expected_output) tuples
GOLDEN_EXAMPLES = [
    (
        {
            "document": "# Heading\n\nThis is a paragraph.",
            "source_format": "markdown",
            "target_format": "html",
            "style": "formal"
        },
        {
            "transformed_document": "<h1>Heading</h1><p>This is a paragraph.</p>",
            "metadata": {
                "word_count": 5,
                "changes_made": ["Converted markdown to HTML", "Applied formal style"]
            }
        }
    ),
    (
        {
            "document": "Casual text here",
            "source_format": "plain",
            "target_format": "markdown",
            "style": "technical"
        },
        {
            "transformed_document": "Technical description of the text content.",
            "metadata": {
                "word_count": 6,
                "changes_made": ["Applied technical terminology"]
            }
        }
    ),
]


def get_golden_examples():
    """Return golden evaluation examples"""
    return GOLDEN_EXAMPLES
