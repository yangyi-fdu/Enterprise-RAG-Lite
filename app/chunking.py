import re


def split_sections(text: str) -> list[tuple[str, str]]:
    """Split a Markdown document into (heading, body) pairs on '#' headings."""
    sections = []
    heading, lines = "", []
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.*)", line)
        if match:
            if any(l.strip() for l in lines):
                sections.append((heading, " ".join(lines).strip()))
            heading, lines = match.group(1).strip(), []
        else:
            lines.append(line.strip())
    if any(l.strip() for l in lines):
        sections.append((heading, " ".join(lines).strip()))
    return sections


def split_text_with_overlap(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Sliding-window chunking over words.

    Consecutive chunks share `overlap` words, so a sentence cut by one window
    boundary still appears whole in the neighbouring chunk.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap must be in [0, chunk_size)")

    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start += chunk_size - overlap
    return chunks


def chunk_document(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Chunk each section separately and prefix chunks with their heading.

    Keeping chunks inside one section stops a window from mixing two unrelated
    policies, and the heading gives the embedding model the topic of the chunk.
    """
    chunks = []
    for heading, body in split_sections(text):
        for piece in split_text_with_overlap(body, chunk_size, overlap):
            chunks.append(f"{heading}: {piece}" if heading else piece)
    return chunks
