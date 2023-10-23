from uuid import UUID

from minimal.models.text import ExternalMarkModel

from .models.paragraph import ParagraphModel

from .models.root import RootNodeModel


def main():
    data = {
        "type": "paragraph",
        "object": "block",
        "nodes": [
            {
                "object": "text",
                "ranges": [
                    {
                        "marks": [
                            {"type": "empty-mark"},
                            {
                                "type": "external-mark",
                                "data": {"type": "suggestion", "kind": "remove_text"},
                            },
                        ],
                    }
                ],
            }
        ],
    }

    result_1 = RootNodeModel.model_validate(data).root

    print(f"Via RootModel: {result_1!r}")
    # assert isinstance(result_1.nodes[0].ranges[0].marks[1], ExternalMarkModel)

    print("-----------------")

    result_2 = ParagraphModel.model_validate(data)

    print(f"Via ParagraphModel: {result_2!r}")
    assert isinstance(result_2.nodes[0].ranges[0].marks[1], ExternalMarkModel)

    print("-----------------")

    assert result_1 == result_2


if __name__ == "__main__":
    main()
