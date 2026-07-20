def choose_model(prompt):

    complex_words = [
        "analyze",
        "design",
        "develop",
        "debug",
        "strategy",
        "architecture",
        "research",
        "calculate",
        "plan"
    ]

    prompt_lower = prompt.lower()

    for word in complex_words:
        if word in prompt_lower:
            return "deepseek-r1:7b"

    return "llama3.2:latest"