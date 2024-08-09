import os

def generate_codebase_file():
    codebase_filename = "codebase.md"
    with open(codebase_filename, "w") as codebase_file:
        for filename in os.listdir("."):
            if filename.endswith(".py"):
                codebase_file.write(f"```python\n")  # Start code block with language
                codebase_file.write(f"# {filename}\n\n")  # Add filename as a heading
                with open(filename, "r") as f:
                    codebase_file.write(f.read())
                codebase_file.write(f"\n```\n\n")  # End code block

if __name__ == "__main__":
    generate_codebase_file()
