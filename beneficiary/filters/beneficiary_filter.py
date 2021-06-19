import django_filters
from django_filters import CharFilter
from django.db.models import Q
from beneficiary.models import Beneficiary


# class for filter the knowledge base and render the list conditionally
class BeneficiaryFilter(django_filters.FilterSet):
    search = CharFilter(method='Beneficiary_custom_filter' ,field_name='search', label='')

    class Meta:
        model = Beneficiary
        fields = ['search']

    def Beneficiary_custom_filter(self, queryset, name, value):
        return Beneficiary.objects.filter(
            Q(ben_code__icontains=value) | Q(name__icontains=value) | Q(address__icontains=value) |Q(district__icontains=value) | Q(sector__icontains=value) | Q(province__icontains=value)).order_by("id")
        
