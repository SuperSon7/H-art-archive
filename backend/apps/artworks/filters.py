# filters.py
import django_filters as df

from .models import Artwork


class ArtworkFilter(df.FilterSet):
    status = df.CharFilter(field_name="status", lookup_expr="exact")
    status__in = df.BaseInFilter(field_name="status", lookup_expr="in")  # CSV: available,reserved
    only_available = df.BooleanFilter(method="filter_only_available")
    exclude_sold = df.BooleanFilter(method="filter_exclude_sold")

    def filter_only_available(self, qs, name, value):
        if value:
            return qs.filter(status=Artwork.Status.AVAILABLE)
        return qs

    def filter_exclude_sold(self, qs, name, value):
        if value:
            return qs.exclude(status=Artwork.Status.SOLD)
        return qs

    class Meta:
        model = Artwork
        fields = ["status", "status__in", "only_available", "exclude_sold"]
