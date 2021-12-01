from . import create_index as main
import pytest
from dataclasses import is_dataclass, asdict, astuple
from unittest.mock import patch


@pytest.fixture
def notes_dir(tmp_path):
    """Dummy 'notes' directory with markdown files."""

    # Create root directory.
    notes_path = tmp_path / "notes"
    topic_a_path = notes_path / "topic_a"

    notes_path.mkdir()
    topic_a_path.mkdir()

    # Create markdown file paths.
    topic_a_md = topic_a_path / "topic_a.md"

    topic_a_content = """# Test Topic A Header

    Hello world, some content
    """

    topic_a_md.write_text(topic_a_content)

    return notes_path


@pytest.fixture
def markdown_file(tmp_path):
    """A dummy markdown file to test with."""

    # Create root directory.
    notes_path = tmp_path / "notes"
    topic_path = notes_path / "topic"

    notes_path.mkdir(exist_ok=True)
    topic_path.mkdir()

    markdown_file = topic_path / "markdown_file.md"

    return markdown_file


@pytest.fixture
def index():
    """A dummy instance of the Index dataclass."""

    return main.Index(
        index_header="test_header",
        markdown_title="# test_markdown_title",
        markdown_path="./notes/path/to/test/mardown/file.md",
    )


def test_seen_headers():
    """Test the 'seen_headers' set."""

    # Arrange
    seen_headers = main.seen_headers

    # Act
    seen_headers.add("a")
    seen_headers.update({"b", "c"})

    # Assert
    assert isinstance(seen_headers, set)
    assert isinstance(next(iter(seen_headers)), str)


def test_title_not_found():
    with pytest.raises(main.TitleNotFound):
        raise main.TitleNotFound("no title found in file")


def test_index(index):
    """Test 'Index' dataclass."""

    target_index = main.Index(
        index_header=index.index_header,
        markdown_title=index.markdown_title,
        markdown_path=index.markdown_path,
    )

    # Assert
    assert is_dataclass(target_index) is True
    assert asdict(target_index) == asdict(index)
    assert astuple(target_index) == astuple(index)


def test_discover_markdowns(notes_dir):
    # Arrange
    root_dir = str(notes_dir)

    # Act
    md_filepaths = main.discover_markdowns(root_dir=root_dir)

    # Assert
    assert isinstance(md_filepaths, set) is True
    assert len(md_filepaths) == len(list(notes_dir.iterdir()))
    for md_filepath in md_filepaths:
        assert "/notes/topic_a/topic_a.md" or "/notes/topic_a/topic_b.md" in md_filepath


def test_get_index(notes_dir, markdown_file, index):
    # Arrange
    md_filepaths = main.discover_markdowns(root_dir=notes_dir)
    md_filepaths = iter(md_filepaths)
    topic_a_path = next(md_filepaths)

    # This is a faulty markdown file, should raise error.
    markdown_file.write_text(
        """

    # hello
    """
    )

    # Act
    index_topic_a = main.get_index(src_filepath=topic_a_path)

    # Assert
    assert isinstance(index, main.ProtoIndex)  # make sure index satisfies ProtoIndex
    assert is_dataclass(index_topic_a) is True
    assert list(asdict(index_topic_a).keys()) == [
        "index_header",
        "markdown_title",
        "markdown_path",
    ]

    with pytest.raises(main.TitleNotFound):
        main.get_index(src_filepath=markdown_file)


def test_save_index_header(markdown_file, index):
    # Arrange
    markdown_file.write_text("")

    # Act
    main.save_index_header(index=index, dest_filepath=markdown_file)

    # Assert
    assert index.header_formatted == markdown_file.read_text()


def test_save_index_entry(markdown_file, index):
    # Arrange
    markdown_file.write_text(index.header_formatted)

    # Act
    main.save_index_entry(index=index, dest_filepath=markdown_file)

    # Assert
    assert index.entry_formatted in markdown_file.read_text()


def test_clear_destination(markdown_file):
    # Arrange
    markdown_file.write_text("test_header_formatted\n")

    # Act
    main.clear_destination(dest_filepath=markdown_file)

    # Assert
    assert markdown_file.read_text() == ""


def test_sort_index_header(markdown_file):
    # Arrange
    markdown_file.write_text("test_header_formatted\n avracadavra\n")

    # Act
    main.sort_index_header(dest_filepath=markdown_file)

    # Assert
    markdown_file.read_text().split("\n") == ["avracadavra", "test_header_formatted"]


def test_main_real(notes_dir, markdown_file):
    """Test main function with real methods."""

    # Arrange
    markdown_file.write_text("# Test Main Title")

    # Act
    main.main(root_dir=notes_dir, dest_filepath=markdown_file)

    # Assert
    assert "* [Test Topic A Header]" in markdown_file.read_text()


@patch.object(main, "seen_headers", {"header 1", "header 2"})
@patch("scripts.create_index.save_index_entry", autospec=True)
@patch("scripts.create_index.sort_index_header", autospec=True)
@patch("scripts.create_index.save_index_header", autospec=True)
@patch("scripts.create_index.get_index", autospec=True)
@patch("scripts.create_index.discover_markdowns", autospec=True)
@patch("scripts.create_index.clear_destination", autospec=True)
def test_main_mock(
    # mocks
    mock_clear_destination,
    mock_discover_markdowns,
    mock_get_index,
    mock_save_index_header,
    mock_sort_index_header,
    mock_save_index_entry,
    # fixtures
    notes_dir,
    markdown_file,
    index,
):
    """Test nain function with mocked methods."""

    # Arrange
    mock_discover_markdowns.return_value = ["hello.md", "world.md"]
    mock_get_index.return_value = index

    # Act
    main.main(root_dir=notes_dir, dest_filepath=markdown_file)

    # Assert
    mock_clear_destination.assert_called_once_with(markdown_file)
    mock_discover_markdowns.assert_called_once_with(notes_dir)
    mock_sort_index_header.assert_called_once_with(markdown_file)
    mock_get_index.assert_called_with("world.md")
    mock_save_index_header.assert_called_with(index, markdown_file)
    mock_save_index_entry.assert_called_with(index, markdown_file)
