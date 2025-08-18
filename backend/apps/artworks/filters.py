# filters.py
import django_filters as df

from .models import Artwork


class ArtworkFilter(df.FilterSet):
    status = df.CharFilter(field_name="status", lookup_expr="exact")
    status__in = df.BaseInFilter(field_name="status", lookup_expr="in")  # CSV: available,reserved
    only_public = df.BooleanFilter(method="filter_only_public")
    exclude_sold = df.BooleanFilter(method="filter_exclude_sold")

    def filter_only_public(self, qs, name, value):
        if value:
            return qs.filter(status=Artwork.DisplayStatus.PUBLIC)
        return qs

    def filter_exclude_sold(self, qs, name, value):
        if value:
            return qs.exclude(status=Artwork.SaleStatus.SOLD)
        return qs

    # TODO: 기간별 조회수 필터, 좋아요 수 필터 추가 필요
    class Meta:
        model = Artwork
        fields = ["status", "status__in", "only_public", "exclude_sold"]
