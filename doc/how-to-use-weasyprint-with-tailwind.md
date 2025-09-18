# How to use weasyprint with tailwind

Weasyprint does not support all CSS features a browser might support and also supports some working-draft
CSS-Specifications not yet supported by major browsers.
This leads to some incompatibilities between weasyprint and tailwind.

## Weasyprint does not support some selectors

Most notably simply compling the tailwind css to css creates some css rules that weasyprint ignores as they include
selectors weasyprint does not understand. This includes all selectors of which weasyprint doesn't understand a single 
part of. This is especially problematic as it includes the `:host` pseudo-class, that is part of the selector for the
block defining most css-variables.

To solve this the tailwind-generated-CSS needs to be post-processed to remove these problematic selectors. One way of
doing this is to replace the unsupported selectors by `:not(*)` as that matches no element. With this weasyprint then
at least uses the other parts of the selector. And e.g. a rule with the selector `:root, :host` is still applied to the
root element instead of being completely ignored.

Selectors we think should be replaced by `:not(*)`:
- `:host`
- `::backdrop`
- `::file-selector-button`

There are further selectors in the tailwind-generated-CSS but those should only be used in rules that are not applied
anyway.

One way to do these replacements is by defining a custom vite plugin:
```ts
export default defineConfig({
  plugins: [
    {
      name: 'remove-cssselectors-not-supported-by-weasyprint',
      transform(src, id) {
        if (id.endsWith('css')) {
          return {
            code: src
              .replaceAll(/:host/g, ':not(*)')
              .replaceAll(/::backdrop/g, ':not(*)')
              .replaceAll(/::file-selector-button/g, ':not(*)'),
            map: null,
          }
        }
      },
    }
  ]
})
```

## Weasyprint does not support `@layer`-rules

Weasyprint does not support `@layer`-rules. When using the "normal" way of importing tailwind into a css file it uses
`@layer`-rules. When importing the individual css files it does not. Therefore, the css files must be imported
individually:

```diff
- @import "tailwindcss";
+ @import "tailwindcss/theme.css";
+ @import "tailwindcss/preflight.css";
+ @import "tailwindcss/utilities.css";
```

## Tailwind removes `@page` rules

When tailwind is used with the optimization logic activated (it's the case by default) it removes all `@page` rules.
The optimization must therefore be deactivated.

Example for deactivating optimization for using tailwind with postcss:
```ts
export default {
  plugins: {
    "@tailwindcss/postcss": {
      optimize: false
    },
  }
}
```