# from database2prompt.markdown.markdown_generator import MarkdownGenerator

# def test_should_generate_database_table_of_contents():
#     generator = MarkdownGenerator({
#         "tables": {
#             "table_a": {},
#             "table_b": {},
#             "table_c": {}
#         },
#         "views": {}
#     })
#     markdown = generator.generate()

#     lines = markdown.splitlines()
#     assert len(lines) == 13
#     assert lines[0] == "# Table of contents"
#     assert lines[1] == "- table_a"
#     assert lines[2] == "- table_b"
#     assert lines[3] == "- table_c" 
