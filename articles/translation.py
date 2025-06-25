from modeltranslation.translator import register, TranslationOptions
from .models import Article, Category, Tag


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'annotation', "authors")


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('name', )