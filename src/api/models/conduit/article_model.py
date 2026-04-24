from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class ArticleModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    body: str = Field(min_length=1)
    tag_list: list[str] = []
