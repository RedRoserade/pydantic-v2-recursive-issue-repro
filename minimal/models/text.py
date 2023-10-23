from typing import Literal, List, Union
from typing_extensions import Annotated
from pydantic import BaseModel, Field

from .enums import ExternalMarkType, TextItemSuggestionKind


class EmptyMarkModel(BaseModel):
    type: Literal["empty-mark"] = "empty-mark"


class SuggestionExternalMarkDataModel(BaseModel):
    type: Literal[ExternalMarkType.SUGGESTION] = ExternalMarkType.SUGGESTION
    # NOTE: Removing or commenting the line below allows both models to parse properly.
    #   I don't know why.
    kind: TextItemSuggestionKind


class InlineExternalMarkDataModel(BaseModel):
    type: Literal[ExternalMarkType.INLINE_COMMENT] = ExternalMarkType.INLINE_COMMENT


ExternalMarkDataModel = Annotated[
    Union[
        InlineExternalMarkDataModel,
        SuggestionExternalMarkDataModel,
    ],
    Field(discriminator="type"),
]


class ExternalMarkModel(BaseModel):
    type: Literal["external-mark"] = "external-mark"
    data: ExternalMarkDataModel


class MarkDataModel(BaseModel):
    value: str = ""


class MarkModel(BaseModel):
    type: str
    data: MarkDataModel = Field(default_factory=MarkDataModel)


MarkWithTypeModel = Annotated[
    Union[
        EmptyMarkModel,
        ExternalMarkModel,
    ],
    Field(discriminator="type"),
]


AnyMarkModel = Annotated[
    Union[MarkWithTypeModel, MarkModel],
    # Using union_mode="smart" causes both scenarios to be decoded
    # as `MarkModel`.
    Field(union_mode="left_to_right"),
]


class TextItemModel(BaseModel):
    marks: Annotated[List[AnyMarkModel], Field(default_factory=list)]


class TextModel(BaseModel):
    object: Literal["text"] = "text"
    ranges: List[TextItemModel] = Field(default_factory=list)
