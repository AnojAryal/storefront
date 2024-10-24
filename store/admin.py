from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [("<10", "Low")]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == "<10":
            return queryset.filter(inventory_lt=10)


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "products_count"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": str(collection.id)})
        )
        return format_html("<a href='{}'>{}</a", url, collection.products_count)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                products_count=Count("product"),
            )
        )


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ["clear_inventory"]
    list_display = ["title", "price", "inventory_status", "collection_title"]
    list_editable = ["price"]
    list_per_page = 10
    list_filter = ["collection", "last_update", InventoryFilter]
    list_select_related = ["collection"]

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "Ok"

    @admin.action(description="clear_inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory="0")
        self.message_user(
            request,
            f"{updated_count} products were successfully updated",
            messages.ERROR,
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "membership"]
    list_editable = ["membership"]
    list_per_page = 10
    ordering = ["first_name__istartswith", "last_name__istartswith"]
    search_fields = ["first_name", "last_name"]


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "placed_at", "customer"]
