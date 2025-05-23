
import os
import git

def clone_and_summarize_code(repo_url: str, local_dir: str = "./repo") -> str:
    if os.path.exists(local_dir):
        return summarize_code_structure(local_dir)

    git.Repo.clone_from(repo_url, local_dir)
    return summarize_code_structure(local_dir)

def summarize_code_structure(root_dir: str) -> str:
    summary = ""
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".py"):
                filepath = os.path.join(dirpath, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        summary += f"\nFile: {os.path.relpath(filepath, root_dir)}\n"
                        for line in lines:
                            if line.strip().startswith(("def ", "class ")):
                                summary += line
                except Exception as e:
                    summary += f"\nError reading {filepath}: {e}\n"
    return summary or "No Python files found."
