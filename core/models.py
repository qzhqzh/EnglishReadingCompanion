from py2neo.ogm import RelatedFrom, Property, Model, RelatedTo


class Word(Model):
    __primarykey__ = "spell"

    spell = Property()
    include = RelatedFrom("Article", "INCLUDE")


class Article(Model):
    __primarykey__ = "title"

    title = Property()
    actors = RelatedTo(Word)
