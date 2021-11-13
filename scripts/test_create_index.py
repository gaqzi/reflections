from . import create_index as main
import pytest
from dataclasses import is_dataclass, asdict, astuple
from unittest.mock import patch


@pytest.fixture
def til_dir(tmp_path):
    """Dummy TIL directory with markdown files."""

    # Create root directory.
    til_path = tmp_path / "til"
    topic_a_path = til_path / "topic_a"

    til_path.mkdir()
    topic_a_path.mkdir()

    # Create markdown file paths.
    topic_a_md = topic_a_path / "topic_a.md"

    topic_a_content = """# Test Topic A Header

    Hello world, some content
    """

    topic_a_md.write_text(topic_a_content)

    return til_path


@pytest.fixture
def markdown_file(tmp_path):
    """A dummy markdown file to test with."""

    # Create root directory.
    til_path = tmp_path / "til"
    topic_path = til_path / "topic"

    til_path.mkdir(exist_ok=True)
    topic_path.mkdir()

    markdown_file = topic_path / "markdown_file.md"

    return markdown_file


@pytest.fixture
def index():
    """A dummy instance of the Index dataclass."""

    return main.Index(
        header="test_header",
        header_formatted="test_header_formatted",
        body="test_body",
        body_formatted="test_body_formatted",
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

    # Arrange

    # Act
    target_index = main.Index(
        header=index.header,
        header_formatted=index.header_formatted,
        body=index.body,
        body_formatted=index.body_formatted,
    )

    # Assert
    assert is_dataclass(target_index) is True
    assert asdict(target_index) == asdict(index)
    assert astuple(target_index) == astuple(index)


def test_discover_markdowns(til_dir):
    # Arrange
    root_dir = str(til_dir)

    # Act
    md_filepaths = main.discover_markdowns(root_dir=root_dir)

    # Assert
    assert isinstance(md_filepaths, set) is True
    assert len(md_filepaths) == len(list(til_dir.iterdir()))
    for md_filepath in md_filepaths:
        assert "/til/topic_a/topic_a.md" or "/til/topic_a/topic_b.md" in md_filepath


def test_get_index(til_dir, markdown_file):
    # Arrange
    md_filepaths = main.discover_markdowns(root_dir=til_dir)
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
    assert is_dataclass(index_topic_a) is True
    assert list(asdict(index_topic_a).keys()) == [
        "header",
        "header_formatted",
        "body",
        "body_formatted",
    ]

    with pytest.raises(main.TitleNotFound):
        main.get_index(src_filepath=markdown_file)


def test_save_index_header(markdown_file, index):
    # Arrange
    markdown_file.write_text("")

    # Act
    main.save_index_header(index=index, dest_filepath=markdown_file)

    # Assert
    assert "test_header_formatted" == markdown_file.read_text()


def test_save_index_body(markdown_file, index):
    # Arrange
    markdown_file.write_text("test_header_formatted\n")

    # Act
    main.save_index_body(index=index, dest_filepath=markdown_file)

    # Assert
    assert "test_body_formatted" in markdown_file.read_text()


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


def test_main_real(til_dir, markdown_file):
    """Test main function with real methods."""

    # Arrange
    markdown_file.write_text("# Test Main Title")

    # Act
    main.main(root_dir=til_dir, dest_filepath=markdown_file)

    # Assert
    assert "* [Test Topic A Header]" in markdown_file.read_text()


@patch.object(main, "seen_headers", {"header 1", "header 2"})
@patch("scripts.create_index.save_index_body", autospec=True)
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
    mock_save_index_body,
    # fixtures
    til_dir,
    markdown_file,
    index,
):
    """Test nain function with mocked methods."""

    # Arrange
    mock_discover_markdowns.return_value = ["hello.md", "world.md"]
    mock_get_index.return_value = index

    # Act
    main.main(root_dir=til_dir, dest_filepath=markdown_file)

    # Assert
    mock_clear_destination.assert_called_once_with(markdown_file)
    mock_discover_markdowns.assert_called_once_with(til_dir)
    mock_sort_index_header.assert_called_once_with(markdown_file)
    mock_get_index.assert_called_with("world.md")
    mock_save_index_header.assert_called_with(index, markdown_file)
    mock_save_index_body.assert_called_with(index, markdown_file)
