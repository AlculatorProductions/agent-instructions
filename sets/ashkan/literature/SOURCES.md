# SOURCES

The source manifest: every paper, book or dataset this notebook relies on. A claim tagged
`[S:Citekey]` is only valid if `Citekey` appears here **and** the local file exists.

`pixi run check` verifies that every file in `pdfs/` has a row here, that every row's SHA256 matches
its local file when present, and that every citekey used in note frontmatter resolves in
`references.bib`.

## Columns

| Column | Meaning |
|---|---|
| Citekey | `AuthorYYYYkeyword`; the same key names the PDF, the text, the notes and the BibTeX entry |
| Citation | authors, title, venue, year |
| Role | why this source is here: what it grounds |
| DOI / arXiv | persistent identifier |
| Retrieved | date acquired, and the route (arXiv / publisher / author / institutional) |
| Local path | usually `pdfs/<Citekey>.pdf`; `missing-local` if not yet acquired |
| SHA256 | `shasum -a 256 <file>`; `—` while missing-local |

A source that is wanted but not yet acquired is tracked in the source queue in the lab book
(`NB-03-OPEN-QUESTIONS`), not here. This file lists what we actually have.

## Registered sources

| Citekey | Citation | Role | DOI / arXiv | Retrieved | Local path | SHA256 |
|---|---|---|---|---|---|---|
