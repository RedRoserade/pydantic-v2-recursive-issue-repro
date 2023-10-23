from typing import TYPE_CHECKING, List, Literal, Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from .enums import HeadingType
from .text import TextModel


_ParagraphNodeModelWithType = Annotated[
    Union[
        "ParagraphModel",
        "HeadingModel",
    ],
    Field(discriminator="type"),
]
ParagraphNodeModel = Annotated[
    Union[TextModel, _ParagraphNodeModelWithType], Field(discriminator="object")
]


class ParagraphModel(BaseModel):
    object: Literal["block"] = "block"
    type: Literal["paragraph"] = "paragraph"
    nodes: List[ParagraphNodeModel]


_HeadingNodeModelWithType = Annotated[
    Union[
        ParagraphModel,
        "HeadingModel",
    ],
    Field(discriminator="type"),
]
HeadingNodeModel = Annotated[
    Union[TextModel, _HeadingNodeModelWithType], Field(discriminator="object")
]


if TYPE_CHECKING:
    _HeadingTypeField = HeadingType
else:
    _HeadingTypeField = Literal[tuple(HeadingType)]


class HeadingModel(BaseModel):
    object: Literal["block"] = "block"
    type: _HeadingTypeField
    nodes: List[HeadingNodeModel]
