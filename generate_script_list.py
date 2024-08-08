import os

def generate_md_file():
    md_filename = "script_list.md"
    with open(md_filename, "w") as md_file:
        md_file.write("# List of Python Scripts\n\n")
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    md_file.write(f"- {file_path}\n")

if __name__ == "__main__":
    generate_md_file()
