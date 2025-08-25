# filters.py
import django_filters as df

from .models import Artwork


class ArtworkFilter(df.FilterSet):
    sale_status = df.CharFilter(field_name="sale_status", lookup_expr="exact")
    sale_status__in = df.BaseInFilter(
        field_name="sale_status", lookup_expr="in"
    )  # CSV: available,reserved
    only_public = df.BooleanFilter(method="filter_only_public")
    exclude_sold = df.BooleanFilter(method="filter_exclude_sold")

    def filter_only_public(self, qs, name, value):
        if value:
            return qs.filter(display_status=Artwork.DisplayStatus.PUBLIC)
        return qs

    def filter_exclude_sold(self, qs, name, value):
        if value:
            return qs.exclude(sale_status=Artwork.SaleStatus.SOLD)
        return qs

    # TODO: 기간별 조회수 필터, 좋아요 수 필터 추가 필요, 가격 범위 필터 추가 필요
    class Meta:
        model = Artwork
        fields = ["sale_status", "sale_status__in", "only_public", "exclude_sold"]
