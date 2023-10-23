# Reproduction repository for `RootModel` parsing of unions

This repository provides a way to reproduce the issue where `Union` types aren't parsed properly under the context of a `RootModel` in Pydantic v2.

## Context

The setup is rather large, but represents a realistic scenario of rich text modelling based on [Slate](https://docs.slatejs.org/).

The library allows nesting paragraphs and headings inside each other, so you can effectively have such data structure:

```python
ParagraphModel(
    nodes=[
        ParagraphModel(nodes=[TextModel(...)])
    ]
)
```

We represent this as follows:

- A paragraph has `nodes`. Each node can be a `TextModel`, a `ParagraphModel`, or a `HeadingModel`.
- Because of the way data is modelled in Slate, we do this with two `Unions`, one between `ParagraphModel` and `HeadingModel`, and the other between `TextModel` and the previous `Union` (see [this](./minimal/models/paragraph.py#L17))

A `TextModel` can have `ranges`, which are segments of text, and `marks`, which hold information about suggestions, formatting, etc. There are several kinds of marks, and a fallback `MarkModel` that's a catch-all for everything else. All [marks](./minimal/models/text.py#L46) have discriminators except `MarkModel`.

## Setup

- Create a virtual environment with Python 3.8 or above (tested on 3.8 and 3.11)
- Install the requirements

## Running and results

When running the [script](./minimal/run.py):

```shell
python -m minimal.run
```

I expect both cases (parsing via a `RootModel` of the `Union` and via the concrete type, `ParagraphModel`) to produce the same exact output. However, by default, parsing via `RootModel` causes `result_1.nodes[0].ranges[0].marks[1]` to be a bare `MarkModel` (the fallback) rather than `ExternalMarkModel` (the expected type based on the discriminator).

This causes the assertion to fail:

```text
python -m minimal.run
Via RootModel: ParagraphModel(object='block', type='paragraph', nodes=[TextModel(object='text', ranges=[TextItemModel(marks=[EmptyMarkModel(type='empty-mark'), MarkModel(type='external-mark', data=MarkDataModel(value=''))])])])
-----------------
Via ParagraphModel: ParagraphModel(object='block', type='paragraph', nodes=[TextModel(object='text', ranges=[TextItemModel(marks=[EmptyMarkModel(type='empty-mark'), ExternalMarkModel(type='external-mark', data=SuggestionExternalMarkDataModel(type=<ExternalMarkType.SUGGESTION: 'suggestion'>, kind=<TextItemSuggestionKind.REMOVE_TEXT: 'remove_text'>))])])])
-----------------
Traceback (most recent call last):
  File "/Users/val/.pyenv/versions/3.8.15/lib/python3.8/runpy.py", line 194, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/Users/val/.pyenv/versions/3.8.15/lib/python3.8/runpy.py", line 87, in _run_code
    exec(code, run_globals)
  File "/Users/val/repos/personal/pydantic-v2-slate-demo/minimal/run.py", line 50, in <module>
    main()
  File "/Users/val/repos/personal/pydantic-v2-slate-demo/minimal/run.py", line 46, in main
    assert result_1 == result_2
AssertionError
```

## Things known to work, and other notes

The following "work" but aren't valid options:

- If `ParagraphNodeModel` is modified to not include itself, the model parses properly.
- If [this line](./minimal/models/text.py#L16) is removed, the model parses properly.

A [patch](./fix.patch) fixes the situation by defining the recursive model _after_ the `ParagraphModel` and `HeadingModel` types, and rebuilding these types, without modifying the actual data representation.

Modifying [this `Union`](./minimal/models/text.py#L59) to use `smart` mode (the default) causes _both_ models to parse incorrectly (they use `MarkModel`).
