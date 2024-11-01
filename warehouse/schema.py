import graphene
from graphene_django.types import DjangoObjectType

from .models import Warehouse, Shelf
from book.models import Book


class WarehouseType(DjangoObjectType):
    class Meta:
        model = Warehouse


class ShelfType(DjangoObjectType):
    class Meta:
        model = Shelf
        fields = ("id", "warehouse", "capacity", "name", "books")


class Query2(graphene.ObjectType):
    all_warehouses = graphene.List(WarehouseType)
    shelves_by_warehouse = graphene.List(ShelfType, warehouse_id=graphene.Int())

    def resolve_all_warehouses(root, info):
        return Warehouse.objects.all()
    
    def resolve_shelves_by_warehouse(root, info, warehouse_id):
        return Shelf.objects.filter(warehouse_id=warehouse_id)
    

class CreateWarehouse(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    
    warehouse = graphene.Field(WarehouseType)

    def mutate(root, info, name):
        warehouse = Warehouse.objects.create(name=name)
        return CreateWarehouse(warehouse=warehouse)
    

class UpdateWarehouse(graphene.Mutation):
    class Arguments:
        warehouse_id = graphene.Int(required=True)
        name = graphene.String()
    
    warehouse = graphene.Field(WarehouseType)

    def mutate(root, info, warehouse_id, name):
        warehouse = Warehouse.objects.get(id=warehouse_id)
        if warehouse:
            warehouse.name = name
            warehouse.save()
        return UpdateWarehouse(warehouse=warehouse)
    

class DeleteWarehouse(graphene.Mutation):
    class Arguments:
        warehouse_id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(root, info, warehouse_id):
        Warehouse.objects.get(id=warehouse_id).delete()
        return DeleteWarehouse(success=True)
    
class CreateShelf(graphene.Mutation):
    class Arguments:
        warehouse_id = graphene.Int(required=True)
        capacity = graphene.Int(required=True)
        name = graphene.String(required=True)
        book_ids = graphene.List(graphene.Int, required=False)
    
    shelf = graphene.Field(ShelfType)

    def mutate(root, info, warehouse_id, capacity, name, book_ids=None):
        try:
            warehouse = Warehouse.objects.get(id=warehouse_id)
            shelf = Shelf.objects.create(
                warehouse=warehouse,
                capacity=capacity,
                name=name
            )
            if book_ids:
                books = Book.objects.filter(id__in=book_ids)
                shelf.books.set(books)
            return CreateShelf(shelf=shelf)
        except warehouse.DoesNotExist:
            return None                                                                             
    

class UpdateShelf(graphene.Mutation):
    warehouse = graphene.Field(WarehouseType)
    class Arguments:
        shelf_id = graphene.Int(required=True)
        capacity = graphene.Int(required=False)
        name = graphene.String(required=False)
        book_ids = graphene.List(graphene.Int, required=False)
    
    shelf = graphene.Field(ShelfType)

    def mutate(root, info, shelf_id, warehouse, capacity, name, book_ids=None):
        shelf = Shelf.objects.get(id=shelf_id)

        if warehouse:
            shelf.warehouse = warehouse

        if capacity:
            shelf.capacity = capacity

        if name:
            shelf.name = name
        
        if book_ids:
            books = Book.objects.filter(id__in=book_ids)
            shelf.books.set(books)
        shelf.save()
        return CreateShelf(shelf=shelf)
    

class DeleteShelf(graphene.Mutation):
    class Arguments:
        shelf_id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(root, info, shelf_id):
        Shelf.objects.get(id=shelf_id).delete()
        return DeleteShelf(success=True)
    
class Mutation2(graphene.ObjectType):
    create_warehouse = CreateWarehouse.Field()
    update_warehouse = UpdateWarehouse.Field()
    delete_warehouse = DeleteWarehouse.Field()
    create_shelf = CreateShelf.Field()
    update_shelf = UpdateShelf.Field()
    delete_shelf = DeleteShelf.Field()
