import factory
from factory.faker import faker

FAKER = faker.Faker(locale='en_US')

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'blog.Post'

    headline = factory.Sequence(lambda n: 'post%d' % n)
    short_description = factory.lazy_attribute(lambda x: FAKER.paragraph())
    content = factory.lazy_attribute(lambda x: FAKER.paragraph(10))
