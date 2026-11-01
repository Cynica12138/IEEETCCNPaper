# IEEETCCNPaper

Final revision of **Hierarchical Load Balancing and Cooperative Beam Hopping for Multi-Satellite Direct-to-Cell LEO Networks**.

Manuscript ID: TCCN-TP-26-1155. Revision date: 2026-11-01.

## Documents

- [Clean revised manuscript](Revised_Manuscript_Clean.pdf)
- [Marked manuscript with reviewer-comment tags](Revised_Manuscript_Marked_Reviewers.pdf)
- [Combined response to all three reviewers](Response_to_Reviewers_EN.pdf)

The combined response covers all 19 comments and includes selected revised manuscript passages, formulas, five supporting figures, and the hotspot-reversal results table. Revision page references use the clean manuscript.

## Editable sources

- `Revised_Manuscript_Clean.tex`: clean manuscript.
- `Revised_Manuscript_Marked.tex`: manuscript with revision coloring.
- `Response_to_Reviewers_EN.tex`: combined response.
- `Response_to_Reviewers_EN.md`: readable response text.
- `Fig files/` and `response_assets/`: required figures.
- `IEEEtran.cls`: IEEE document class.
- `tools/add_reviewer_tags.py`: reviewer margin-tag generation.
- `SHA256SUMS.txt`: checksums of the uploaded files.

## Build

Run `./build.ps1` in PowerShell. Requirements: TeX Live (`pdflatex`, `xelatex`), Times New Roman, Poppler (`pdftotext`), and Python with `pypdf` and `reportlab`.

The script compiles the manuscript and response and generates the tagged marked PDF. Build intermediates are stored in `build/`. All source asset paths are relative.
