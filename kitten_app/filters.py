import django_filters
from .models import Kitten

class KittenFilter(django_filters.FilterSet):
    min_age = django_filters.NumberFilter(field_name='age_months', lookup_expr='gte', label='Minimum Age')
    max_age = django_filters.NumberFilter(field_name='age_months', lookup_expr='lte', label='Maximum Age')
    breed = django_filters.CharFilter(field_name='breed', lookup_expr='exact')  # Exact match for breed
    color = django_filters.CharFilter(field_name='color', lookup_expr='exact')  # Exact match for color

    class Meta:
        model = Kitten
        fields = ['breed', 'color', 'min_age', 'max_age']

    def filter_queryset(self, queryset):
        # Filter by exact age if min_age and max_age are the same
        min_age = self.data.get('min_age')
        max_age = self.data.get('max_age')

        if min_age and max_age and min_age == max_age:
            queryset = queryset.filter(age_months=min_age)
        else:
            queryset = super().filter_queryset(queryset)

        return queryset
