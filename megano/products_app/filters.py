from django_filters import rest_framework as filters


class CatalogFilter(filters.FilterSet):
    """Фильтр товаров для каталога"""

    name = filters.CharFilter(field_name="title", lookup_expr="icontains")
    minPrice = filters.NumberFilter(field_name="price", lookup_expr="gte")
    maxPrice = filters.NumberFilter(field_name="price", lookup_expr="lte")
    available = filters.BooleanFilter(method="get_availability")
    freeDelivery = filters.BooleanFilter()

    def get_availability(self, queryset, name, value):
        """Отфильтровывает товары количество которых равно нулю"""
        if value:
            return queryset.exclude(count=0)
        return queryset
