import os


def generate_md_file():
    md_filename = "script_list.md"
    with open(md_filename, "w") as md_file:
        md_file.write("# List of Python Scripts\n\n")
        for file in os.listdir("."):
            for file in files:
                if file.endswith(".py"):
                    md_file.write(f"- {file}\n")


if __name__ == "__main__":
    generate_md_file()
