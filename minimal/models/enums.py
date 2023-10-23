from enum import Enum, unique


@unique
class TextItemSuggestionKind(str, Enum):
    INSERT_TEXT = "insert_text"
    REMOVE_TEXT = "remove_text"
    FORMAT_TEXT = "format_text"


class ExternalMarkType(str, Enum):
    INLINE_COMMENT = "inline-comment"
    SUGGESTION = "suggestion"


@unique
class HeadingType(str, Enum):
    HEADING_1 = "header-one"
    HEADING_2 = "header-two"
    HEADING_3 = "header-three"
    HEADING_4 = "header-four"
    HEADING_5 = "header-five"
