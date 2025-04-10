import openai

def generate_overview(topic: str) -> str:
    """Generate a brief overview for the given topic using OpenAI."""
    prompt = f"Provide a brief overview of the topic '{topic}'. Keep it concise and informative."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        # Extract the generated text
        overview = response.choices[0].message.content.strip()
    except Exception as e:
        overview = f"An error occurred while generating overview: {e}"
    return overview

def generate_subtopic(topic: str, subtopic: str) -> str:
    """Generate text focusing on a specific subtopic of the given topic."""
    # Adjust prompt phrasing for certain common subtopics:
    sub = subtopic.lower()
    if sub == "present":
        aspect = f"the current state of {topic}"
    elif sub == "future":
        aspect = f"the future prospects of {topic}"
    elif sub == "history":
        aspect = f"the history of {topic}"
    else:
        aspect = f"{subtopic} of {topic}"
    prompt = f"Provide a concise explanation about {aspect}."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        content = response.choices[0].message.content.strip()
    except Exception as e:
        content = f"An error occurred while generating subtopic content: {e}"
    return content
