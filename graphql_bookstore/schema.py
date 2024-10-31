import graphene

from book.schema import Query1, Mutation1
from warehouse.schema import Query2, Mutation2


class Query(Query1, Query2, graphene.ObjectType):
    pass


class Mutation(Mutation1, Mutation2, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
