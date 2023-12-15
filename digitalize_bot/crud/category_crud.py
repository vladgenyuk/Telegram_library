from .base_crud import BaseCrud

from digitalize_bot.models.categories import Category


class CategoryCrud(BaseCrud):
    pass


category = CategoryCrud(Category)
