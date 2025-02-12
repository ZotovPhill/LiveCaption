from pydantic import BaseModel

from ..enums.language import LanguageEnum


class Settings(BaseModel):
    language: LanguageEnum
