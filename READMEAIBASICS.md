### The Chain-of-Thought (CoT) 
    approach is a prompting technique used in Large Language Models (LLMs) where the model explains intermediate reasoning steps before giving the final answer. This helps the model solve complex problems step by step, improving accuracy.

    Normal Prompt
        Q: If a book costs ₹200 and you buy 3 books, how much do you pay?
        A: 600

    Chain-of-Thought Prompt
        Q: If a book costs ₹200 and you buy 3 books, how much do you pay?

        Let's think step by step:
        1. Cost of one book = ₹200
        2. Number of books = 3
        3. Total cost = 200 × 3
        4. Total = ₹600

        Answer: ₹600    

        Here the model shows reasoning steps → then final answer.

### Chain-of-Thought in LLM Architecture

        Question
            ↓
        Tokenization
            ↓
        Transformer Layers
            ↓
        Intermediate reasoning tokens
            ↓
        Final answer

### Chain-of-Thought Example in Python (LLM)
    prompt = """
        Solve step by step.

        If a train travels 60 km per hour for 3 hours,
        how far does it travel?

        Show reasoning.
    """
    