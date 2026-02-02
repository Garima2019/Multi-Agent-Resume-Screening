from crewai import Agent, Crew, Task, LLM


def build_crew(user_input: str, callback=None):
    llm = LLM(model="gemini/gemini-2.5-flash-lite")

    analyzer = Agent(
        role="Analyzer",
        goal="Understand user intent and identify ambiguities",
        backstory="You break down user input into clear intent and missing details.",
        llm=llm
    )

    critic = Agent(
        role="Critic",
        goal="Challenge the analyzer and find flaws",
        backstory="You aggressively question assumptions and logic.",
        llm=llm
    )

    reasoner = Agent(
        role="Domain Reasoner",
        goal="Apply domain-specific reasoning to the problem",
        backstory="You focus on technical correctness and constraints.",
        llm=llm
    )

    synthesizer = Agent(
        role="Synthesizer",
        goal="Produce a clear, final answer for the user",
        backstory="You merge insights and remove unnecessary reasoning.",
        llm=llm
    )

    tasks = [
        Task(
            description=f"Analyze the following user input and extract intent, assumptions, and missing details:\n{user_input}",
            expected_output=(
                "A structured analysis including:\n"
                "- User intent\n"
                "- Key assumptions\n"
                "- Missing or ambiguous information"
            ),
            agent=analyzer
        ),
        Task(
            description="Critically evaluate the analyzer's output and identify logical flaws or weak assumptions.",
            expected_output=(
                "A list of critiques pointing out logical gaps, weak assumptions, "
                "or incorrect interpretations in the analyzer’s output."
            ),
            agent=critic
        ),
        Task(
            description="Apply domain-specific reasoning to refine the understanding of the problem.",
            expected_output=(
                "A technically accurate refinement of the problem, "
                "including constraints, edge cases, and feasibility considerations."
            ),
            agent=reasoner
        ),
        Task(
            description="Synthesize all insights into a concise, final response for the user.",
            expected_output=(
                "A clear, actionable, and well-structured final answer "
                "that directly addresses the user’s input."
            ),
            agent=synthesizer
        ),
    ]

    crew = Crew(
        agents=[analyzer, critic, reasoner, synthesizer],
        tasks=tasks,
        verbose=True,
        callbacks=[callback] if callback else None
    )

    return crew
