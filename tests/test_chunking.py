import pytest

from app.chunking import chunk_document, split_sections, split_text_with_overlap


def test_windows_overlap_by_the_requested_number_of_words():
    words = [f"w{i}" for i in range(25)]
    chunks = split_text_with_overlap(" ".join(words), chunk_size=10, overlap=3)
    assert chunks[0].split() == words[0:10]
    assert chunks[1].split() == words[7:17]
    assert chunks[-1].split()[-1] == "w24"


def test_every_word_is_covered_and_last_chunk_is_not_duplicated():
    text = " ".join(str(i) for i in range(100))
    chunks = split_text_with_overlap(text, chunk_size=20, overlap=5)
    covered = {w for c in chunks for w in c.split()}
    assert covered == set(text.split())
    assert chunks[-1] != chunks[-2]


def test_short_text_gives_one_chunk():
    assert split_text_with_overlap("only five words in here", 10, 2) == ["only five words in here"]


@pytest.mark.parametrize("size,overlap", [(0, 0), (10, 10), (10, -1)])
def test_invalid_arguments(size, overlap):
    with pytest.raises(ValueError):
        split_text_with_overlap("a b c", size, overlap)


def test_chunks_do_not_cross_sections_and_carry_the_heading():
    doc = "# Leave\nYou get 15 days.\n\n# Travel\nBook 14 days ahead."
    assert split_sections(doc) == [("Leave", "You get 15 days."), ("Travel", "Book 14 days ahead.")]
    assert chunk_document(doc, chunk_size=50, overlap=5) == [
        "Leave: You get 15 days.",
        "Travel: Book 14 days ahead.",
    ]
