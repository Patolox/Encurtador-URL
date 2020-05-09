import graphene
from graphene_django import DjangoObjectType
from django.db.models import When, F, Q

from .models import URL


class URLType(DjangoObjectType):
    class Meta:
        model = URL


class Query(graphene.ObjectType):
    urls = graphene.List(URLType)

    def resolve_urls(self, info, **kwargs):
        return URL.objects.all()

    def findUrl(url_search, self, info, **kwargs):
        return URL.objects.get(full_url__exact=url_search).url_hash

class CreateURL(graphene.Mutation):
    url = graphene.Field(URLType)

    class Arguments:
        full_url = graphene.String()

    def mutate(self, info, full_url):
        url = URL(full_url=full_url)
        url.save()

        return CreateURL(url=url)


class Mutation(graphene.ObjectType):
    create_url = CreateURL.Field()