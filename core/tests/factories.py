import factory
from factory.faker import faker

FAKER = faker.Faker(locale='en_US')


class SeriesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "core.Series"

    name = factory.Sequence(lambda n: 'series%d' % n)
    description = factory.LazyAttribute(lambda x: FAKER.paragraph())

class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "core.BasicTag"

    name = factory.Sequence(lambda n: 'tag%d' % n)
    filterable = True
    shown = True

