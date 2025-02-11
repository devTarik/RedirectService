import factory
from django.contrib.auth.models import User
from django.utils import timezone

from apps.redirect.models import RedirectRule


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@gmail.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User


class RedirectRuleFactory(factory.django.DjangoModelFactory):
    id = factory.Faker("uuid4")
    owner = factory.SubFactory(UserFactory)
    redirect_url = factory.Faker("url")
    is_private = False
    redirect_identifier = factory.Faker("pystr", max_chars=16)
    created = factory.LazyFunction(timezone.now)
    modified = factory.LazyFunction(timezone.now)

    class Meta:
        model = RedirectRule
