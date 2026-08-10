# literature/

Papers, their metadata, whatever source material came with them, and our reading notes.

One paper, one **citekey** (`AuthorYYYYkeyword`, e.g. `Author2024keyword`), used everywhere:

| Path | Contents | Tracked? |
|---|---|---|
| `references.bib` | BibTeX entry — the single bibliography, shared with the lab book | yes |
| `SOURCES.md` | the manifest: role, DOI, retrieval date, local path, SHA256 | yes |
| `pdfs/<Citekey>.pdf` | the PDF | **no** — see below |
| `text/<Citekey>.md` | extracted text, for grepping | yes |
| `src/<Citekey>/` | upstream LaTeX / code / data that came with the paper | **no** by default |
| `notes/<Citekey>.md` | our reading notes | yes |

## Why PDFs are not in git

They are large, often not redistributable, and they are not the record — the *notes* are. The
manifest makes them re-acquirable: `SOURCES.md` carries the DOI/arXiv ID, the URL, the retrieval
date and the SHA256, so anyone can fetch the same file and verify it is the same file.

`src/` follows the same rule. A small text file from an upstream repository that directly backs a
claim may be force-added (`git add -f literature/src/<Key>/thefile.py`); tarballs, binaries and
large datasets stay out.

## Adding a source

```bash
# 1. put the PDF in place (lawful route: arXiv, publisher, author, institutional access)
cp ~/Downloads/paper.pdf literature/pdfs/Author2024keyword.pdf

# 2. hash it for the manifest
shasum -a 256 literature/pdfs/Author2024keyword.pdf

# 3. ALWAYS try for the upstream source too — for arXiv, the e-print tarball.
#    This is the thing you actually read; see "Reading notes" below.
mkdir -p literature/src/Author2024keyword
curl -sSL -o /tmp/eprint.tar.gz https://arxiv.org/e-print/<arxiv-id>
tar xzf /tmp/eprint.tar.gz -C literature/src/Author2024keyword

# 4. add the BibTeX entry to references.bib, with DOI or arXiv ID
# 5. add the row to SOURCES.md
#    NB: the Citekey, Local path and SHA256 cells are parsed literally by
#    scripts/check.py — write them bare, no backticks, or the gate will fail.
# 6. optionally extract text (needs poppler: `brew install poppler`)
pdftotext -layout literature/pdfs/Author2024keyword.pdf literature/text/Author2024keyword.md

# 7. write the notes
cp literature/_template.md literature/notes/Author2024keyword.md
```

Not every paper ships source. Journal supplementary material, an authors' GitHub or Zenodo, or the
code/data repository named in the paper are the other routes worth trying. When nothing is
available, record that in the notes rather than leaving it ambiguous.

`pixi run check` fails if a PDF has no manifest row, if a hash does not match, or if a note cites a
citekey that is not in `references.bib`.

## Reading notes

Notes separate three things, and the separation is the point:

1. **What the paper says** — with section, equation, figure or table numbers, tagged `[S:Key §2.3]`.
2. **What it assumes** — approximations, regimes of validity, the conventions it uses (which go
   into `../CONVENTIONS.md` if we adopt or translate them).
3. **What we make of it** — our reading, tagged `[I]`, and our open questions, tagged `[?]`.

Do not paste long copyrighted excerpts. Cite the location, paraphrase, quote briefly.

**Read `src/<Key>/` in preference to `pdfs/<Key>.pdf` whenever the source exists.** The LaTeX is
the authoritative form: exact equations rather than glyphs recovered from a rendering, real
`\label{}`s to cite, the authors' own bibliography to mine for follow-up sources, and it greps. For
a preprint with auto-numbered equations, cite section plus label (`SM §II.A eq:cond`) — that is
reproducible for the next reader in a way "page 7" is not.

Extracted text in `text/` is a convenience for searching, and ranks below both. Equations and
numbers taken from it are confirmed against the source or the PDF before they are tagged `[S:...]`;
OCR and PDF-to-text output routinely mangle signs, subscripts and exponents.
