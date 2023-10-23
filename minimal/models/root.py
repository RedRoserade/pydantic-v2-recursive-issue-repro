
from typing import Union
from typing_extensions import Annotated
from pydantic import Field, RootModel

from .paragraph import ParagraphModel, HeadingModel


RootNodeModel = RootModel[
    Annotated[
        Union[
            ParagraphModel,
            HeadingModel,
        ],
        Field(discriminator="type"),
    ]
]
