from gencontent import extract_title

def test_extract_title():
    markdown = """# My Title
This is the content."""
    assert extract_title(markdown) == "My Title"

def test_extract_title_no_title():
    markdown = """This is the content."""
    try:
        extract_title(markdown)
        assert False, "Expected exception not raised"
    except Exception as e:
        assert str(e) == "No title found in markdown content"

def test_extract_title_after_other_text():
    markdown = """Some intro text

# Real Title

More text"""
    assert extract_title(markdown) == "Real Title"