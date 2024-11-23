from django_filters import FilterSet, DateFilter
from django.forms import DateInput
from .models import Post



class PostFilter(FilterSet):
    create_time = DateFilter(
        field_name='create_time',
        widget=DateInput(attrs={'type': 'date'}),
        label='Дата',
        lookup_expr='date__gte',
    )

    class Meta:
        model = Post
        fields = {
            'header': ['icontains'],
            'author': ['exact'],
            # 'create_time': ['gt'],
            'category': ['icontains']
        }








