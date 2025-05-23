
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
import os
from modules.readme_scraper import scrape_github_readme
from modules.code_parser import clone_and_summarize_code
from modules.slides import generate_presentation
from modules.component_detector import read_all_code, detect_components_regex, detect_components_llm
from modules.diagram_generator import generate_architecture_diagram

GITHUB_REPO_URL = "https://github.com/nickperugini/agent-repo-test"

def main():
    llm = ChatOpenAI(temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

    readme_content = scrape_github_readme(GITHUB_REPO_URL)
    clone_and_summarize_code(GITHUB_REPO_URL)  # download the repo
    full_code = read_all_code()

    # Run both regex and LLM detectors
    components = detect_components_regex(full_code)
    components.update(detect_components_llm(full_code, llm))

    diagram_path = generate_architecture_diagram(components)

    repo_name = GITHUB_REPO_URL.rstrip("/").split("/")[-1]

    slide_prompts = {
        "title": f"{repo_name}",
        "Objective of the application": f"Summarize the purpose of this project based on the README below. Write clearly and concisely for a technical audience:\n\n{readme_content}",
        "Solution Architecture of the code": f"Based on the following code structure, describe how the major components of the project work together. Format your response as a bullet list of components and their responsibilities:\n\n{full_code[:2000]}"
    }

    generated_content = {}
    for key, prompt in slide_prompts.items():
        response = llm.invoke(prompt)
        generated_content[key] = response.content if hasattr(response, "content") else str(response)

    generate_presentation(generated_content, diagram_path=diagram_path)

if __name__ == "__main__":
    main()
