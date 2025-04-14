import openai
import os


def generate_text(topic, subtopics=None):
    """
    Generates text for the given topic. If one or more subtopics are provided,
    it will produce a combined narrative. Otherwise, it provides an overview.

    We also ensure we start with an introductory line like:
    'Okay, let's talk about People and Technology in Cricket...' 
    and then a concise explanation.
    """

    # Handle no subtopics => general overview
    if not subtopics or len(subtopics) == 0:
        prompt = (
            f"Provide a concise overview of '{topic}'. "
            "Focus on the most important or interesting aspects. "
            "Keep your response under 150 words."
        )
    else:
        # Convert subtopics to a readable string 
        sub_list = [s.strip() for s in subtopics]
        if len(sub_list) == 1:
            subtopics_str = sub_list[0]
            # Introduction line in the prompt
            introduction_line = (
                f"Okay, let's talk about {subtopics_str} in {topic}."
            )
            prompt = (
                f"{introduction_line}\n"
                f"Give a concise explanation of how {subtopics_str} relates to {topic}. "
                "Keep the response under 150 words."
            )
        else:
            # Multiple subtopics
            if len(sub_list) > 1:
                subtopics_str = ", ".join(sub_list[:-1]) + " and " + sub_list[-1]
            else:
                subtopics_str = sub_list[0]

            introduction_line = (
                f"Okay, let's talk about {subtopics_str} in {topic}."
            )
            prompt = (
                f"{introduction_line}\n"
                f"Give a cohesive explanation that blends these subtopics together. "
                "Keep the response under 150 words."
            )

    # Use a system + user prompt approach to guide the model:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a concise assistant. You provide short, factual answers under ~150 words.Begin your answer with the provided introduction line and then explain."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,        
            temperature=0.7,        
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        result_text = response.choices[0].message.content.strip()
        return result_text
    except Exception as e:
        return f"Error generating text: {str(e)}"
