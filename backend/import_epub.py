"""
import_epub.py

Import an EPUB book into the GARCS LIBRARY.

IMPORTANT:
    EPUB files are imported into:
        LibraryBook
        LibraryChapter

They are NOT imported into:
        Passage
        Chapter

Assessment passages remain managed exclusively by seed.py.

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
    4. Identifies likely reading chapters.
    5. Creates ONE LibraryBook record.
    6. Creates LibraryChapter records for each chapter.
    7. Stores chapter text in the database.

The EPUB binary itself is NOT stored in SQLite.
"""

import argparse
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from ebooklib import epub, ITEM_DOCUMENT, ITEM_IMAGE

# IMPORTANT:
# These are the LIBRARY models.
# Do NOT change these to Passage / Chapter.
from app import app, db, LibraryBook, LibraryChapter


# ============================================================
# CONFIGURATION
# ============================================================

GRADE_BANDS = {
    1: "Grades 3–5",
    2: "Grades 6–8",
    3: "Grades 9–12",
}


# EPUB documents that should not become reading chapters.
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
    "project gutenberg",
    "license",
    "legal notice",
    "terms of use",
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
        "noscript",
        "svg"
    ]):
        tag.decompose()

    text = soup.get_text("\n")

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
    Determine whether an EPUB document appears to contain
    actual reading content.
    """

    normalized_title = clean_title(title).lower()

    # Ignore known front/back matter.
    if normalized_title in IGNORED_TITLES:
        return False

    word_count = len(text.split())

    # Ignore extremely short documents.
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
        if re.search(
            pattern,
            normalized_title,
            re.IGNORECASE
        ):
            return True

    # If there is no useful title but substantial text exists,
    # treat it as likely reading content.
    if not normalized_title and word_count >= 300:
        return True

    # Long documents are usually reading chapters even when
    # their EPUB metadata is poor.
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

    soup = BeautifulSoup(
        item.get_content(),
        "html.parser"
    )

    # First try headings.
    for tag_name in ["h1", "h2", "h3"]:

        heading = soup.find(tag_name)

        if heading:
            title = clean_title(
                heading.get_text(
                    " ",
                    strip=True
                )
            )

            if title:
                return title

    # Then try HTML title.
    if soup.title:

        title = clean_title(
            soup.title.get_text(
                " ",
                strip=True
            )
        )

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

    title_values = book.get_metadata(
        "DC",
        "title"
    )

    if title_values:

        title = title_values[0][0]

    author_values = book.get_metadata(
        "DC",
        "creator"
    )

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

def extract_cover(
    book,
    output_directory,
    book_id
):
    """
    Attempt to extract the EPUB cover image.

    Returns:
        A frontend-relative path such as:

            /static/covers/1_cover.jpg

        or None if no cover is found.
    """

    output_directory = Path(
        output_directory
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    cover_item = None

    # --------------------------------------------------------
    # Method 1:
    # EPUB metadata cover reference
    # --------------------------------------------------------

    metadata = book.get_metadata(
        "OPF",
        "cover"
    )

    if metadata:

        for value, attributes in metadata:

            cover_id = attributes.get(
                "content"
            )

            if cover_id:

                cover_item = (
                    book.get_item_with_id(
                        cover_id
                    )
                )

                if cover_item:
                    break

    # --------------------------------------------------------
    # Method 2:
    # Search image filenames for "cover"
    # --------------------------------------------------------

    if cover_item is None:

        for item in book.get_items_of_type(
            ITEM_IMAGE
        ):

            name = item.get_name().lower()

            if "cover" in name:

                cover_item = item
                break

    # --------------------------------------------------------
    # Method 3:
    # Use first image as fallback
    # --------------------------------------------------------

    if cover_item is None:

        images = list(
            book.get_items_of_type(
                ITEM_IMAGE
            )
        )

        if images:

            cover_item = images[0]

    if cover_item is None:
        return None

    image_name = Path(
        cover_item.get_name()
    ).name

    # Prevent problematic filenames.
    image_name = re.sub(
        r"[^A-Za-z0-9._-]",
        "_",
        image_name
    )

    output_path = (
        output_directory
        / f"{book_id}_{image_name}"
    )

    with open(
        output_path,
        "wb"
    ) as file:

        file.write(
            cover_item.get_content()
        )

    return (
        f"/static/covers/{output_path.name}"
    )


# ============================================================
# EXTRACT CHAPTERS
# ============================================================

def extract_chapters(book):
    """
    Extract likely reading chapters from the EPUB.

    Returns:

        [
            {
                "title": "...",
                "content": "..."
            },
            ...
        ]
    """

    chapters = []

    # EPUB spine represents the intended reading order.
    spine_items = []

    for spine_entry in book.spine:

        item_id = spine_entry[0]

        item = book.get_item_with_id(
            item_id
        )

        if (
            item
            and item.get_type() == ITEM_DOCUMENT
        ):

            spine_items.append(item)

    for item in spine_items:

        content = clean_text(
            item.get_content()
        )

        if not content:
            continue

        title = extract_document_title(
            item
        )

        if not looks_like_chapter(
            title,
            content
        ):
            continue

        if not title:

            title = (
                f"Chapter {len(chapters) + 1}"
            )

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
    Import one EPUB into LibraryBook and LibraryChapter.

    Assessment Passage/Chapter records are never modified.
    """

    epub_path = Path(
        epub_path
    )

    # --------------------------------------------------------
    # Validate file
    # --------------------------------------------------------

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
            "Invalid grade band. "
            "Use 1, 2, or 3."
        )

    print()
    print("=" * 60)
    print("GARCS EPUB LIBRARY IMPORTER")
    print("=" * 60)
    print(f"File:       {epub_path}")
    print(
        f"Grade band: {GRADE_BANDS[grade_band]}"
    )
    print(
        f"Category:   {category or 'Reading'}"
    )
    print(
        f"Featured:   {featured}"
    )
    print("=" * 60)

    # --------------------------------------------------------
    # Read EPUB
    # --------------------------------------------------------

    print("\nReading EPUB...")

    try:

        book = epub.read_epub(
            str(epub_path)
        )

    except Exception as exc:

        raise RuntimeError(
            f"Could not read EPUB: {exc}"
        ) from exc

    # --------------------------------------------------------
    # Metadata
    # --------------------------------------------------------

    title, author = extract_metadata(
        book
    )

    if not title:

        title = epub_path.stem

    print(
        f"Title:      {title}"
    )

    print(
        f"Author:     {author or 'Unknown'}"
    )

    # --------------------------------------------------------
    # Prevent duplicate library books
    # --------------------------------------------------------

    existing = (
        LibraryBook.query
        .filter_by(title=title)
        .first()
    )

    if existing:

        raise RuntimeError(
            f"A library book titled "
            f"'{title}' already exists "
            f"(ID {existing.id}). "
            f"Import cancelled."
        )

    # --------------------------------------------------------
    # Extract chapters BEFORE touching database
    # --------------------------------------------------------

    print("\nExtracting chapters...")

    chapters = extract_chapters(
        book
    )

    if not chapters:

        raise RuntimeError(
            "No chapters could be detected "
            "in this EPUB.\n"
            "The EPUB may use an unusual "
            "structure and will need to be "
            "inspected manually."
        )

    print(
        f"Detected {len(chapters)} chapters."
    )

    for index, chapter in enumerate(
        chapters,
        start=1
    ):

        word_count = len(
            chapter["content"].split()
        )

        print(
            f"  {index:>3}. "
            f"{chapter['title']} "
            f"({word_count:,} words)"
        )

    # --------------------------------------------------------
    # Create LibraryBook
    # --------------------------------------------------------

    library_book = LibraryBook(
        title=title,
        author=author or None,
        description=(
            f"{title}"
            + (
                f" by {author}"
                if author
                else ""
            )
        ),
        category=category or "Reading",
        grade_band=grade_band,
        is_featured=featured,
    )

    db.session.add(
        library_book
    )

    # Generate the LibraryBook ID.
    db.session.flush()

    print(
        f"\nCreated LibraryBook ID: "
        f"{library_book.id}"
    )

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
            library_book.id
        )

        if cover_path:

            print(
                f"Cover:      {cover_path}"
            )

            library_book.cover_image = (
                cover_path
            )

        else:

            print(
                "Cover:      No cover found"
            )

    except Exception as exc:

        print(
            f"Warning: could not extract "
            f"cover: {exc}"
        )

    # --------------------------------------------------------
    # Create LibraryChapter records
    # --------------------------------------------------------

    print(
        "\nCreating library chapters..."
    )

    for number, chapter_data in enumerate(
        chapters,
        start=1
    ):

        chapter = LibraryChapter(
            book_id=library_book.id,
            chapter_number=number,
            title=chapter_data["title"],
            content=chapter_data["content"],
        )

        db.session.add(
            chapter
        )

    # --------------------------------------------------------
    # Commit
    # --------------------------------------------------------

    try:

        db.session.commit()

    except Exception:

        db.session.rollback()

        raise

    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("LIBRARY IMPORT SUCCESSFUL")
    print("=" * 60)
    print(
        f"LibraryBook ID: {library_book.id}"
    )
    print(
        f"Title:          {library_book.title}"
    )
    print(
        f"Author:         "
        f"{author or 'Unknown'}"
    )
    print(
        f"Chapters:       {len(chapters)}"
    )
    print(
        f"Grade band:     "
        f"{GRADE_BANDS[grade_band]}"
    )
    print(
        "Destination:    LibraryBook / "
        "LibraryChapter"
    )
    print("=" * 60)
    print()


# ============================================================
# COMMAND-LINE INTERFACE
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Import an EPUB into the "
            "GARCS library."
        )
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
        help=(
            "Book category, e.g. "
            "Adventure, Science, History"
        )
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