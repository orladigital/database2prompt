import markdown

def generate_markdown(content: str, output_file: str):
    """Gera um arquivo Markdown a partir de uma string."""
    md_content = markdown.markdown(content)
    with open(output_file, "w") as file:
        file.write(md_content)
