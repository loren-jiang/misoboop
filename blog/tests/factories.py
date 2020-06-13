import factory
from factory.faker import faker
from core.tests.factories import SeriesFactory

FAKER = faker.Faker(locale='en_US')



class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'blog.Post'

    headline = factory.Sequence(lambda n: 'post%d' % n)
    short_description = factory.LazyAttribute(lambda x: FAKER.paragraph())
    content = factory.LazyAttribute(lambda x: FAKER.paragraph(10))

class PostWithSeriesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'blog.Post'

    headline = factory.Sequence(lambda n: 'post%d' % n)
    short_description = factory.LazyAttribute(lambda x: FAKER.paragraph())
    content = factory.LazyAttribute(lambda x: FAKER.paragraph(10))
    series = factory.SubFactory(SeriesFactory)
