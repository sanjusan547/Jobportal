import django_filters
from .models import Job

class Jobfilter(django_filters.FilterSet):
    title=django_filters.CharFilter(field_name='title',lookup_expr='icontains')
    min_salary=django_filters.NumberFilter(field_name="salary", lookup_expr='gte')
    max_salary=django_filters.NumberFilter(field_name="salary",lookup_expr='lte')
    min_experience=django_filters.NumberFilter(field_name="experience",lookup_expr='gte')
    max_experience=django_filters.NumberFilter(field_name="experience",lookup_expr='lte')
    jobtype = django_filters.CharFilter(field_name='jobtype', lookup_expr='iexact')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')

class Meta:
    model=Job
    fields=['location','jobtype','min_salary','max_salary','title','min_experience','max_experience']