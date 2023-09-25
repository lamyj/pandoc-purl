# pandoc-purl

![PyPI](https://img.shields.io/pypi/v/pandoc-purl)

_pandoc-purl_ is [Pandoc](https://pandoc.org) filter for literate programming and dynamic document generation in Python. It is similar in spirit to [Knitr](https://yihui.org/knitr/) or [Pweave](https://mpastell.com/pweave/).

_pandoc-purl_ can be installed through _pip_ (e.g. `python3 -m pip install pandoc-purl`), and used like other Pandoc filters, e.g. `pandoc --filter pandoc-purl document.md -o document.tex`.

## Code chunks

_pandoc-purl_ will process code blocks tagged with the `python` class or inline code tagged with the `p` or `python` classes.

**Note** This _README.md_ file has been generated from the _README.in.md_ using _pandoc-purl_.

### Code blocks

Code blocks marked with the `python` class will behave as if executed in an interactive Python shell: they execute their content, display the content and, in a following paragraph, display any printed value as well as the value of the last expression (see below for options controlling this behavior).

+------------------------------+----------------------------+
| Input                        | Rendered                   |
+==============================+============================+
| ~~~~~~~~~~                   | ```python                  |
| ```python                    | print("Hello pandoc-purl") |
| print("Hello pandoc-purl")   | 42                         |
| 42                           | ```                        |
| ```                          |                            |
| ~~~~~~~~~~                   |                            |
+------------------------------+----------------------------+

If the last statement is not an expression, the code is still executed and displayed, but no result is printed

+------------------------------+----------------------------+
| Input                        | Rendered                   |
+==============================+============================+
| ~~~~~~~~~~                   | ```python                  |
| ```python                    | a = 3.14                   |
| a = 3.14                     | ```                        |
| ```                          |                            |
| ~~~~~~~~~~                   |                            |
+------------------------------+----------------------------+

### Inline code

Inline code marked with the `p` or `python` classes should contain only a single expression, and will display the value of that expression in the text.

+------------------------------+----------------------------+
| Input                        | Rendered                   |
+==============================+============================+
| ~~~~~~~~~~                   | The answer is `6*7`{.p}    |
| The answer is `6*7`{.p}      |                            |
| ~~~~~~~~~~                   |                            |
+------------------------------+----------------------------+

## Chunk options

Options can be passed to code chunks using the `key=value` syntax. The following options are available:

- `eval`: whether to run the code chunk (`true` or `false`, defaults to `true`)
  
  +------------------------------------+------------------------------------+
  | Input                              | Rendered                           |
  +====================================+====================================+
  | ~~~~~~~~~~                         | The answer is `6*7`{.p}            |
  | The answer is `6*7`{.p}            |                                    |
  | ~~~~~~~~~~                         |                                    |
  +------------------------------------+------------------------------------+
  | ~~~~~~~~~~                         | The answer is `6*7`{.p eval=false} |
  | The answer is `6*7`{.p eval=false} |                                    |
  | ~~~~~~~~~~                         |                                    |
  +------------------------------------+------------------------------------+
  
- `echo`: whether to show the code (code blocks only, `true` or `false`, defaults to `true`)
  
  +------------------------------+----------------------------+
  | Input                        | Rendered                   |
  +==============================+============================+
  | ~~~~~~~~~~                   | ```python                  |
  | ```python                    | print("Hello pandoc-purl") |
  | print("Hello pandoc-purl")   | ```                        |
  | ```                          |                            |
  | ~~~~~~~~~~                   |                            |
  +------------------------------+----------------------------+
  | ~~~~~~~~~~                   | ```{.python echo=false}    |
  | ```{.python echo=false}      | print("Hello pandoc-purl") |
  | print("Hello pandoc-purl")   | ```                        |
  | ```                          |                            |
  | ~~~~~~~~~~                   |                            |
  +------------------------------+----------------------------+
  
- `results`: how to show the result of the last expression
  - `asis`: show the result as a pre-formatted code block or inline (default)
  - `markup`: process the result through Pandoc before showing it
  - `hide`: hide the result
  
  +-------------------------------------+-------------------------------------+
  | Input                               | Rendered                            |
  +=====================================+=====================================+
  | ~~~~~~~~~~                          | I'm `"**bold**"`{.p}                |
  | I'm `"**bold**"`{.p}                |                                     |
  | ~~~~~~~~~~                          |                                     |
  +-------------------------------------+-------------------------------------+
  | ~~~~~~~~~~                          | I'm `"**bold**"`{.p results=markup} |
  | I'm `"**bold**"`{.p results=markup} |                                     |
  | ~~~~~~~~~~                          |                                     |
  +-------------------------------------+-------------------------------------+

## Changing the defaults

The default chunk options can also be changed globally by modifying `chunk_defaults` in the `pandoc_purl` module:
    
    ```{.python echo=false}
    import pandoc_purl
    pandoc_purl.chunk_defaults["echo"] = False
    ```
