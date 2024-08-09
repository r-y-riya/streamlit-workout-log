import os


def generate_md_file():
    md_filename = "codebse.md"
    with open(md_filename, "w") as md_file:
        md_file.write("# List of Python Scripts\n\n")
        md_file.write("```\n")  # Start the code block
        for file in os.listdir("."):
            if file.endswith(".py"):
                md_file.write(f"- {file}\n")
        md_file.write("```\n")  # End the code block


if __name__ == "__main__":
    generate_md_file()
