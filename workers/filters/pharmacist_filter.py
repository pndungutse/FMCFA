import django_filters
from django_filters import CharFilter
from django.db.models import Q
from workers.models.pharmacist import Pharmacist


# class for filter the knowledge base and render the list conditionally
class PharmacistFilter(django_filters.FilterSet):
    search = CharFilter(method='Pharmacist_custom_filter' ,field_name='search', label='')

    class Meta:
        model = Pharmacist
        fields = ['search']

    def Pharmacist_custom_filter(self, queryset, name, value):
        return Pharmacist.objects.filter(
            Q(name__icontains=value) | Q(address__icontains=value) | Q(phone__icontains=value) | Q(email__icontains=value)).order_by("id")
        
