from django_filters import rest_framework as filters

from reviews.models import Title


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class TitleFilterSet(filters.FilterSet):
    category = CharFilterInFilter(
        field_name='category__slug', lookup_expr='in'
    )
    genre = CharFilterInFilter(field_name='genre__slug', lookup_expr='in')
    name = CharFilterInFilter(field_name='name', lookup_expr='in')
    year = CharFilterInFilter(
        field_name='year',
    )

    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year')
