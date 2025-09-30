# Accessibility

In general a properly accessible HTML should also create an accessible PDF file. There are some potential problems
listed down below.

Do not forget to check your created files using a validator like [VeraPDF](https://verapdf.org/software/),
[PDF4WCAG](https://pdf4wcag.com/validate/new-job/settings) or [PAC](https://pac.pdf-accessibility.org/de) (Windows only)

The created files should be *PDF/A-2a* compliant. They should also comply with *PDF/UA-1* (except for the metadata
indicating this compliance). Compliance  with *PDF/UA-2* is not possible as we create *PDF 1.7* files and *PDF/UA-2*
requires *PDF-2.0*. *PDF-2.0* is not compatible with *PDF/A-2a*.

## Do not have `<a>`-tags nested in other elements

Weasyprint does not support creating `<a>`-tags that surround multiple elements in a PDF/UA compliant way.
This is actively being worked on by weasyprint.

Sometimes it also works to replicate the `<a>`-tag in every nesting layer. E.g. instead of
`<a><h2><span>bla</span></h2></a>` use `<a><h2><a><span><a>bla</a></span></a></h2></a>`

- https://github.com/Kozea/WeasyPrint/issues/2482
- https://github.com/Kozea/WeasyPrint/issues/185

## Footnotes

I'm very unsure of how the footnotes should work in an accessible pdf, but I'm mostly sure the current implementation is
not that accessible (the footnotes are in the flow where they are in the page not where they are references.
Not yet sure how to fix this.
