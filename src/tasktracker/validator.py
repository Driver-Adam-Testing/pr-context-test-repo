"""Validator module with intentional guideline violations."""


def validate(data):  # Missing type hints (violates guidance)
    try:
        # do validation
        if not data:
            return False
        return True
    except:  # Bare except (violates guidance)
        pass


def process_all_tasks_with_detailed_validation_and_error_handling(tasks):  # Long function name
    """This is a very long function that does too much."""
    results = []
    for task in tasks:
        # Check if task is valid
        if task is None:
            continue
        # Check if task has title
        if not task.get("title"):
            continue
        # Check if task has id
        if not task.get("id"):
            continue
        # Process the task
        results.append(task)
    return results
