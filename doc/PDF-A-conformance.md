# PDF/A conformance

There are different PDF/A conformance levels and versions.

The Bundesarchive recommends using PDF/A-2a, PDF/A-2u, PDF/A-2b, PDF/A-1a, ... in that order.[^1]
Weasyprint does not support creating **PDF/A-2a** files. We therefore create **PDF/A-2u** conforming files.

If the PDF-Version is set to 2.0 they can no longer be valid **PDF/A-2u** files. We therefore need to use **PDF 1.7**.

If the PDF-file is properly tagged it should also confirm to most of **PDF/A-2a**. But the metadata indicating this is not set. We
therefore adjust the metadata in a post-processing step. This way we create **PDF/A-2a** files.

TODO: can we also add the metadata for indicating PDF/UA-1 support? The file should also confirm to the requirements for
it, and it should be possible to support PDF/A-2a and PDF/UA-1 at the same time.

[^1]: https://www.bundesarchiv.de/assets/bundesarchiv/de/Downloads/Erklaerungen/beratungsangebote-grundl-sgv-empfehlungen-pdf-a-versionen.pdf
