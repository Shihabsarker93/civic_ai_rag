from scripts.test_source_preference import OLD, NEW, trial_prompt
from src.generation.ollama_generator import build_prompt


def test_baseline_is_exact_existing_prompt():
    contexts = [{"id": "s1", "content": "source content", "metadata": {}}]
    assert trial_prompt("question", contexts) == build_prompt("question", contexts)


def test_only_source_preference_instructions_change():
    contexts = [{"id": "s1", "content": "source content", "metadata": {}}]
    baseline = trial_prompt("question", contexts)
    neutral = trial_prompt("question", contexts, True)
    assert neutral.replace(NEW, OLD, 1) == baseline
    assert "Source 1 is the strongest evidence" not in neutral
    assert "[Source 1] id=s1" in neutral
