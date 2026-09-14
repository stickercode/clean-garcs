"""
import_epub.py

Import an EPUB book into the GARCS SQLite database.

Usage:

    python import_epub.py path/to/book.epub --grade-band 2

Grade bands:
    1 = Grades 3–5
    2 = Grades 6–8
    3 = Grades 9–12

Optional:

    python import_epub.py book.epub \
        --grade-band 2 \
        --category Adventure \
        --featured

The importer:
    1. Opens the EPUB.
    2. Extracts title and author metadata.
    3. Extracts the cover image.
    4. Attempts to identify actual reading chapters.
    5. Creates one Passage record.
    6. Creates one Chapter record for each chapter.
    7. Stores the chapter text in the database.

The EPUB file itself is NOT stored inside SQLite.
"""

import argparse
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from ebooklib import epub, ITEM_DOCUMENT, ITEM_IMAGE

# Import your existing Flask application and database/models.
#
# This assumes import_epub.py is inside the same backend/ directory
# as app.py.
from app import app, db, Passage, Chapter


# ============================================================
# CONFIGURATION
# ============================================================

GRADE_BANDS = {
    1: "Grades 3–5",
    2: "Grades 6–8",
    3: "Grades 9–12",
}


# Words commonly found in EPUB files that are NOT actual
# reading chapters.
IGNORED_TITLES = {
    "cover",
    "title page",
    "titlepage",
    "copyright",
    "copyright page",
    "contents",
    "table of contents",
    "toc",
    "dedication",
    "about the author",
    "about the publisher",
    "also by",
    "acknowledgments",
    "acknowledgements",
    "colophon",
    "the full project gutenberg license",
    "project gutenberg license",
    "license",
    "legal notice",
}


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(html_content):
    """
    Convert XHTML/HTML chapter content into clean plain text.
    """

    soup = BeautifulSoup(html_content, "html.parser")

    # Remove elements that should not become reading text.
    for tag in soup([
        "script",
        "style",
        "nav",
        "noscript"
    ]):
        tag.decompose()

    text = soup.get_text("\n")

    # Normalize whitespace while preserving paragraphs.
    lines = []

    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()

        if line:
            lines.append(line)

    return "\n\n".join(lines).strip()


# ============================================================
# TITLE CLEANING
# ============================================================

def clean_title(title):
    """
    Clean an EPUB document title.
    """

    if not title:
        return ""

    title = re.sub(r"\s+", " ", title).strip()

    return title


# ============================================================
# DETERMINE WHETHER A DOCUMENT IS A CHAPTER
# ============================================================

def looks_like_chapter(title, text):
    """
    Decide whether an EPUB document appears to be a real
    reading chapter.

    This intentionally uses heuristics because EPUB files
    differ considerably in structure.
    """

    normalized_title = clean_title(title).lower()

    # Ignore known front/back matter.
    if normalized_title in IGNORED_TITLES:
        return False

    # Ignore very short documents.
    word_count = len(text.split())

    if word_count < 100:
        return False

    # Common chapter naming patterns.
    chapter_patterns = [
        r"^chapter\s+\d+",
        r"^chapter\s+[ivxlcdm]+",
        r"^part\s+\d+",
        r"^part\s+[ivxlcdm]+",
        r"^\d+[\s.:\-]",
        r"^[ivxlcdm]+[\s.:\-]",
    ]

    for pattern in chapter_patterns:
        if re.search(pattern, normalized_title, re.IGNORECASE):
            return True

    # If there is no useful title but the document has
    # substantial text, it may still be a chapter.
    if not normalized_title and word_count >= 300:
        return True

    # Long documents are often chapter-like even when the
    # EPUB has poor metadata.
    if word_count >= 300:
        return True

    return False


# ============================================================
# EXTRACT DOCUMENT TITLE
# ============================================================

def extract_document_title(item):
    """
    Try to find a useful title for an EPUB document.
    """

    soup = BeautifulSoup(item.get_content(), "html.parser")

    # First try headings.
    for tag_name in ["h1", "h2", "h3"]:
        heading = soup.find(tag_name)

        if heading:
            title = clean_title(heading.get_text(" ", strip=True))

            if title:
                return title

    # Then try the HTML title.
    if soup.title:
        title = clean_title(soup.title.get_text(" ", strip=True))

        if title:
            return title

    return ""


# ============================================================
# EXTRACT BOOK METADATA
# ============================================================

def extract_metadata(book):
    """
    Extract title and author from EPUB metadata.
    """

    title = ""

    authors = []

    title_values = book.get_metadata("DC", "title")

    if title_values:
        title = title_values[0][0]

    author_values = book.get_metadata("DC", "creator")

    for value, attributes in author_values:
        if value:
            authors.append(value)

    return (
        clean_title(title),
        ", ".join(authors)
    )


# ============================================================
# EXTRACT COVER
# ============================================================

def extract_cover(book, output_directory, passage_id):
    """
    Attempt to extract the EPUB cover image.

    Returns:
        Relative path suitable for storing in Passage.cover_image
        or None if no cover is found.
    """

    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)

    cover_item = None

    # --------------------------------------------------------
    # Method 1: EPUB metadata cover reference
    # --------------------------------------------------------

    metadata = book.get_metadata("OPF", "cover")

    if metadata:
        for value, attributes in metadata:
            cover_id = attributes.get("content")

            if cover_id:
                cover_item = book.get_item_with_id(cover_id)

                if cover_item:
                    break

    # --------------------------------------------------------
    # Method 2: Find an image whose filename contains "cover"
    # --------------------------------------------------------

    if cover_item is None:
        for item in book.get_items_of_type(ITEM_IMAGE):
            name = item.get_name().lower()

            if "cover" in name:
                cover_item = item
                break

    # --------------------------------------------------------
    # Method 3: Use the first image as a fallback
    # --------------------------------------------------------

    if cover_item is None:
        images = list(book.get_items_of_type(ITEM_IMAGE))

        if images:
            cover_item = images[0]

    if cover_item is None:
        return None

    image_name = Path(cover_item.get_name()).name

    # Prevent weird filenames.
    image_name = re.sub(
        r"[^A-Za-z0-9._-]",
        "_",
        image_name
    )

    output_path = output_directory / f"{passage_id}_{image_name}"

    with open(output_path, "wb") as file:
        file.write(cover_item.get_content())

    # This path is what the frontend can use.
    return f"/static/covers/{output_path.name}"


# ============================================================
# EXTRACT CHAPTERS
# ============================================================

def extract_chapters(book):
    """
    Extract likely reading chapters from the EPUB.

    Returns a list:

        [
            {
                "title": "...",
                "content": "..."
            },
            ...
        ]
    """

    chapters = []

    # Prefer EPUB spine order because it represents the
    # intended reading order.
    spine_items = []

    for spine_entry in book.spine:
        item_id = spine_entry[0]

        item = book.get_item_with_id(item_id)

        if item and item.get_type() == ITEM_DOCUMENT:
            spine_items.append(item)

    for item in spine_items:

        content = clean_text(item.get_content())

        if not content:
            continue

        title = extract_document_title(item)

        if not looks_like_chapter(title, content):
            continue

        if not title:
            title = f"Chapter {len(chapters) + 1}"

        chapters.append({
            "title": title,
            "content": content,
        })

    return chapters


# ============================================================
# IMPORT EPUB
# ============================================================

def import_epub(
    epub_path,
    grade_band,
    category=None,
    featured=False,
):
    """
    Import one EPUB into the database.
    """

    epub_path = Path(epub_path)

    if not epub_path.exists():
        raise FileNotFoundError(
            f"EPUB file not found: {epub_path}"
        )

    if epub_path.suffix.lower() != ".epub":
        raise ValueError(
            "The selected file is not an EPUB."
        )

    if grade_band not in GRADE_BANDS:
        raise ValueError(
            "Invalid grade band. Use 1, 2, or 3."
        )

    print()
    print("=" * 60)
    print("GARCS EPUB IMPORTER")
    print("=" * 60)
    print(f"File:       {epub_path}")
    print(f"Grade band: {GRADE_BANDS[grade_band]}")
    print(f"Category:   {category or 'Reading'}")
    print(f"Featured:   {featured}")
    print("=" * 60)

    # --------------------------------------------------------
    # Read EPUB
    # --------------------------------------------------------

    print("\nReading EPUB...")

    try:
        book = epub.read_epub(str(epub_path))
    except Exception as exc:
        raise RuntimeError(
            f"Could not read EPUB: {exc}"
        ) from exc

    # --------------------------------------------------------
    # Metadata
    # --------------------------------------------------------

    title, author = extract_metadata(book)

    if not title:
        title = epub_path.stem

    print(f"Title:      {title}")
    print(f"Author:     {author or 'Unknown'}")

    existing = Passage.query.filter_by(
        title=title
    ).first()

    if existing:
        raise RuntimeError(
            f"A passage titled '{title}' already exists "
            f"(ID {existing.id}). Import cancelled."
        )

    # --------------------------------------------------------
    # Extract chapters BEFORE modifying database
    # --------------------------------------------------------

    print("\nExtracting chapters...")

    chapters = extract_chapters(book)

    if not chapters:
        raise RuntimeError(
            "No chapters could be detected in this EPUB.\n"
            "The EPUB may use an unusual structure and will "
            "need to be inspected manually."
        )

    print(f"Detected {len(chapters)} chapters.")

    for index, chapter in enumerate(chapters, start=1):
        word_count = len(chapter["content"].split())

        print(
            f"  {index:>3}. "
            f"{chapter['title']} "
            f"({word_count:,} words)"
        )

    # --------------------------------------------------------
    # Create Passage
    # --------------------------------------------------------

    passage = Passage(
        title=title,
        grade_band=grade_band,
    )

    # These fields only exist if you've added them to Passage.
    if hasattr(Passage, "author"):
        passage.author = author

    if hasattr(Passage, "category"):
        passage.category = category or "Reading"

    if hasattr(Passage, "is_featured"):
        passage.is_featured = featured

    # Store a basic description if your Passage model has it.
    if hasattr(Passage, "description"):
        passage.description = (
            f"{title}"
            + (f" by {author}" if author else "")
        )

    db.session.add(passage)

    # Flush so SQLite gives us the Passage ID.
    db.session.flush()

    print(f"\nCreated Passage ID: {passage.id}")

    # --------------------------------------------------------
    # Cover
    # --------------------------------------------------------

    cover_directory = (
        Path(__file__).resolve().parent.parent
        / "frontend"
        / "static"
        / "covers"
    )

    try:
        cover_path = extract_cover(
            book,
            cover_directory,
            passage.id
        )

        if cover_path:
            print(f"Cover:      {cover_path}")

            if hasattr(Passage, "cover_image"):
                passage.cover_image = cover_path

    except Exception as exc:
        print(
            f"Warning: could not extract cover: {exc}"
        )

    # --------------------------------------------------------
    # Create Chapters
    # --------------------------------------------------------

    print("\nCreating chapters...")

    for number, chapter_data in enumerate(chapters, start=1):

        chapter = Chapter(
            passage_id=passage.id,
            chapter_number=number,
            title=chapter_data["title"],
            content=chapter_data["content"],
        )

        db.session.add(chapter)

    # --------------------------------------------------------
    # Commit
    # --------------------------------------------------------

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    print()
    print("=" * 60)
    print("IMPORT SUCCESSFUL")
    print("=" * 60)
    print(f"Passage ID: {passage.id}")
    print(f"Title:      {passage.title}")
    print(f"Author:     {author or 'Unknown'}")
    print(f"Chapters:   {len(chapters)}")
    print(f"Grade band: {GRADE_BANDS[grade_band]}")
    print("=" * 60)
    print()


# ============================================================
# COMMAND-LINE INTERFACE
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="Import an EPUB into the GARCS library."
    )

    parser.add_argument(
        "epub",
        help="Path to the .epub file"
    )

    parser.add_argument(
        "--grade-band",
        type=int,
        required=True,
        choices=[1, 2, 3],
        help=(
            "1 = Grades 3–5, "
            "2 = Grades 6–8, "
            "3 = Grades 9–12"
        )
    )

    parser.add_argument(
        "--category",
        default="Reading",
        help="Book category, e.g. Adventure, Science, History"
    )

    parser.add_argument(
        "--featured",
        action="store_true",
        help="Mark this book as featured"
    )

    args = parser.parse_args()

    with app.app_context():

        try:
            import_epub(
                epub_path=args.epub,
                grade_band=args.grade_band,
                category=args.category,
                featured=args.featured,
            )

        except Exception as exc:

            print()
            print("IMPORT FAILED")
            print("-" * 60)
            print(str(exc))
            print("-" * 60)
            print()

            sys.exit(1)


if __name__ == "__main__":
    main()