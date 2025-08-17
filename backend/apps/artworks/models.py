from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from parler.models import TranslatableModel, TranslatedFields

from apps.artists.models import Artist


def get_current_year():
    return timezone.now().year


class Artwork(TranslatableModel):
    translation = TranslatedFields(
        title=models.CharField(max_length=150, db_index=True, help_text="작품명"),
        description=models.TextField(
            blank=True, verbose_name="작품 설명", help_text="작품에 대한 상세 설명"
        ),
    )

    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="artworks", verbose_name="작가"
    )

    # tags = models.ManyToManyField(Tag, blank=True, related_name='artworks', verbose_name="해시태그")

    year_created = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(
                limit_value=get_current_year, message="제작 연도는 현재 연도보다 클 수 없습니다."
            ),
        ],
        verbose_name="제작년도",
        help_text="작품이 제작된 년도",
    )

    price_krw = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        null=True,
        blank=True,
        verbose_name="가격(원화)",
        help_text="한국 원화 기준 가격",
    )

    price_usd = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="가격(달러)",
        help_text="미국 달러 기준 가격",
    )

    materials = models.TextField(verbose_name="재료", help_text="예: 캔버스에 아크릴, 브론즈 등")

    width = models.FloatField(verbose_name="가로(cm)", validators=[MinValueValidator(0.1)])

    height = models.FloatField(verbose_name="세로(cm)", validators=[MinValueValidator(0.1)])

    depth = models.FloatField(
        null=True,
        blank=True,
        verbose_name="깊이(cm)",
        help_text="조각품 등에 적용",
        validators=[MinValueValidator(0.1)],
    )

    dimension_unit = models.CharField(
        max_length=10,
        default="cm",
        choices=[("cm", "Centimeter"), ("inch", "Inch")],
        verbose_name="크기 단위",
    )

    CATEGORY_CHOICES = [
        ("painting", "회화"),
        ("oriental_painting", "동양화"),
        ("sculpture", "조소"),
        ("printmaking", "판화"),
        ("wood_craft", "목조"),
        ("ceramics", "도예"),
        ("metal_craft", "금속조형"),
        ("photography", "사진"),
        ("digital", "디지털아트"),
        ("mixed_media", "혼합매체"),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="카테고리")

    # class Visibility(models.TextChoices):
    #     PUBLIC = 'PUBLIC', '공개'
    #     HIDDEN = 'HIDDEN', '비공개'

    # visibility = models.CharField(
    #     max_length=20,
    #     choices=Visibility.choices,
    #     default='PUBLIC',
    #     verbose_name="공개 여부"
    # )

    class SaleStatus(models.TextChoices):
        AVAILABLE = "available", "판매중"
        SOLD = "sold", "판매완료"
        RESERVED = "reserved", "예약중"
        NOT_FOR_SALE = "not_for_sale", "판매안함"

    class DisplayStatus(models.TextChoices):
        PUBLIC = "public", "공개"
        HIDDEN = "hidden", "비공개"

    sale_status = models.CharField(
        max_length=20,
        choices=SaleStatus.choices,
        default="not_for_sale",
        db_index=True,
        verbose_name="판매 상태",
    )

    display_status = models.CharField(
        max_length=20,
        choices=DisplayStatus.choices,
        default="public",
        db_index=True,
        verbose_name="공개 여부",
    )

    copyright_agreed = models.BooleanField(
        default=False, verbose_name="저작권 동의", help_text="작품 업로드 시 저작권 관련 동의 여부"
    )

    license_agreed = models.BooleanField(
        default=False, verbose_name="라이선스 동의", help_text="플랫폼 이용 라이선스 동의 여부"
    )

    view_count = models.PositiveIntegerField(default=0, verbose_name="조회수")

    like_count = models.PositiveIntegerField(default=0, verbose_name="좋아요 수")

    is_featured = models.BooleanField(
        default=False, verbose_name="큐레이터 추천", help_text="메인 페이지에 노출될 추천 작품 여부"
    )

    featured_at = models.DateTimeField(null=True, blank=True, verbose_name="추천 등록일")

    is_deleted = models.BooleanField(default=False, verbose_name="삭제됨")

    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="삭제일시")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.safe_translation_getter('title', any_language=True)} by {self.artist.name}"

    @property
    def primary_image(self):
        """대표 이미지 반환"""
        return self.images.filter(is_primary=True).first()

    @property
    def dimensions_display(self):
        """크기 표시용 프로퍼티"""
        if self.depth:
            return f"{self.width} × {self.height} × {self.depth} {self.dimension_unit}"
        return f"{self.width} × {self.height} {self.dimension_unit}"

    def increment_view_count(self):
        """조회수 증가"""
        self.view_count += 1
        self.save(update_fields=["view_count"])

    def get_price_display(self, currency="KRW"):
        """통화별 가격 표시"""
        if currency == "USD" and self.price_usd:
            return f"${self.price_usd:,.2f}"
        elif currency == "KRW" and self.price_krw:
            return f"₩{self.price_krw:,}"
        return "가격 문의"


class ArtworkImage(models.Model):
    """작품 이미지 모델"""

    artwork = models.ForeignKey(
        Artwork, on_delete=models.CASCADE, related_name="images", verbose_name="작품"
    )

    image = models.ImageField(upload_to="artworks/%Y/%m/", verbose_name="이미지")

    is_primary = models.BooleanField(default=False, verbose_name="대표 이미지")

    order = models.PositiveIntegerField(default=0, verbose_name="정렬 순서")

    alt_text = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="대체 텍스트",
        help_text="접근성을 위한 이미지 설명",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="업로드일시")

    class Meta:
        verbose_name = "작품 이미지"
        verbose_name_plural = "작품 이미지들"
        ordering = ["order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["artwork"],
                condition=models.Q(is_primary=True),
                name="unique_primary_image_per_artwork",
            )
        ]

    def __str__(self):
        return f"{self.artwork.safe_translation_getter('title', any_language=True)} - Image {self.order}"

    def get_inquiries(self):
        return self.purchase_inquiries.select_related("inquirer")

    def has_pending_inquiries(self):
        return self.purchase_inquiries.filter(status="pending").exists()
