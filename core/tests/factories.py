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

class PublicImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "core.PublicImage"
    name = factory.Sequence(lambda n: 'public_image%d' %n)
    upload = factory.django.ImageField(filename="black_square.jpg", from_path="fixtures/black_square.jpg")