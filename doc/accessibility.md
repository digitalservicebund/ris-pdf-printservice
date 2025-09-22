# Accessibility

## Do not have `<a>`-tags nested in other elements

Weasyprint does not support creating `<a>`-tags that surround multiple elements in a PDF/UA compliant way.
This is actively being worked on by weasyprint.

Sometimes it also works to replicate the `<a>`-tag in every nesting layer. E.g. instead of `<a><h2><span>bla</span></h2></a>` use `<a><h2><a><span><a>bla</a></span></a></h2></a>`

- https://github.com/Kozea/WeasyPrint/issues/2482
- https://github.com/Kozea/WeasyPrint/issues/185

## Do not use `<span>` as immediate child of `<section>`
tbd.

## Footnotes

I'm very unsure of how the footnotes should work in an accessible pdf, but I'm mostly sure the current implementation is
not that accessible (the footnotes are in the flow where they are in the page not where they are references.
Not yet sure how to fix this.

## Do not use a `<h2>` element as direct child of `<article>`

This nests an `<Art>` within an `<Art>`. This is not allowed by https://pdfa.org/resource/iso-32005

