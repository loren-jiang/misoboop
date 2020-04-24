from factory import faker
import factory

class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'recipe.Recipe'

    name = factory.Sequence(lambda n: 'recipe%d' % n)
    description = factory.LazyAttribute(lambda obj: f'description for ${obj.name}')
