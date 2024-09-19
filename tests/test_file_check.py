import os
import tempfile
from grab.utils.file_check import validate_file_format, check_required_files

def test_validate_file_format():
    # Create a temporary file with valid format
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(b"Title 1\nhttps://example.com/video1\nTitle 2\nhttps://example.com/video2\n")
        tmp_file.close()
        assert validate_file_format(tmp_file.name) == True
        os.remove(tmp_file.name)

    # Create a temporary file with invalid format (odd number of lines)
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(b"Title 1\nhttps://example.com/video1\nTitle 2\n")
        tmp_file.close()
        assert validate_file_format(tmp_file.name) == False
        os.remove(tmp_file.name)

def test_check_required_files():
    # Test with existing files
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file1, tempfile.NamedTemporaryFile(delete=False) as tmp_file2:
        assert check_required_files(tmp_file1.name, tmp_file2.name) == True
        os.remove(tmp_file1.name)
        os.remove(tmp_file2.name)

    # Test with non-existing files
    assert check_required_files("non_existing_file.txt", "non_existing_file.txt") == False
