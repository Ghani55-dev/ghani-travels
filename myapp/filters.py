import django_filters
from .models import TourPackage

class PackageFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    duration = django_filters.NumberFilter(field_name='duration', lookup_expr='exact')

    class Meta:
        model = TourPackage
        fields = ['destination', 'price', 'duration']