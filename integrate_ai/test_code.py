import openai

# Set up your OpenAI API key
openai.api_key = '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'

def generate_curriculum(topic):
    """Generate curriculum content based on the given study topic."""
    prompt = f"Generate a curriculum for studying {topic}."
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=300
    )
    return response.choices[0].text.strip()

def organize_curriculum(content):
    """Organize the generated curriculum into separate sections."""
    sections = content.split("**")
    return [section.strip() for section in sections if section.strip()]

def main():
    study_topic = input("Enter the study topic: ")
    curriculum_content = generate_curriculum(study_topic)
    sections = organize_curriculum(curriculum_content)

    print("\nGenerated Curriculum:")
    for section in sections:
        print(section)

    # Storing sections into a list
    sections_list = [""] * len(sections)
    for i, section in enumerate(sections):
        sections_list[i] = section

    print("\nSections List:")
    print(sections_list)

if __name__ == "__main__":
    main()
