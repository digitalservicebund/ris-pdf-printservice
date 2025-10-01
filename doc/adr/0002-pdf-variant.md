# 2. PDF-Variant & Version

Date: 2025-10-01

## Status

Accepted

## Context

There are different kinds of PDF files. We need to decide which one we want to comply with.

There are different **PDF/A** conformance levels and versions.
The Bundesarchive recommends using PDF/A-2a, PDF/A-2u, PDF/A-2b, PDF/A-1a, ... in that order.[^1]
Weasyprint does not support creating *PDF/A-2a* files. It can create *PDF/A-2u* conforming files.

The newest PDF-Version supported by *PDF/A-2u* and *PDF/A-2a* is *PDF 1.7*. *PDF 2.0* is not compatible with
*PDF/A-2u* or *PDF/A-2a*.

If a *PDF/A-2u*-file is properly tagged for accessibility it should also confirm to most of *PDF/A-2a*. But the
metadata indicating this is not set by weasyprint. We can adjust the metadata in a post-processing step.

For accessibility there are also the PDF variants *PDF/UA-1* and *PDF/UA-2*. *PDF/UA-2* requires *PDF 2.0*.

## Decision

We create **PDF/A-2a** files in **PDF-Version 1.7**. We use weasyprint to create *PDF/A-2u* files and then adjust the 
metadata to indicate that it is a *PDF/A-2a* compliant. We ensure this compliance by setting up weasyprint to created
tagged-PDFs.

We do not indicate *PDF/UA-1* compliance, even though the created files comply to it (with the exception to the rule
checking that the metadata indicate *PDF/UA-1* compliance).
Setting these metadata in a *PDF/A-2a* compliant way is not that simple and would require a lot more work.

## Consequences

We create PDF-files in a version that is both accessible and also long-term-archivable.

[^1]: https://www.bundesarchiv.de/assets/bundesarchiv/de/Downloads/Erklaerungen/beratungsangebote-grundl-sgv-empfehlungen-pdf-a-versionen.pdf