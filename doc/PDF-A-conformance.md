# PDF/A conformance

There are different PDF/A conformance levels and versions.

The Bundesarchive recommends using PDF/A-2a, PDF/A-2u, PDF/A-2b, PDF/A-1a, ... in that order.[^1]
Weasyprint does not support creating PDF/A-2a files. We therefore looked at creating **PDF/A-2u** conforming files.

If the PDF-Version is set to 2.0 they can no longer be valid PDF/A-2u files. We therefore need to use **PDF 1.7**.

If the PDF-file is tagged it should in theory also confirm to PDF/A-2a. But the metadata indicating this is not set. We
would need to do this our-self in a post-processing step.

[^1]: https://www.bundesarchiv.de/assets/bundesarchiv/de/Downloads/Erklaerungen/beratungsangebote-grundl-sgv-empfehlungen-pdf-a-versionen.pdf
