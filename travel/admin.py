# your_app/admin.py
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.urls import reverse
from django import forms

from .form import AttractionForm
from .models import (
    Attraction, TourPackage, Order,
    TourPackageFavorite, AttractionFavorite, AttractionVisited,
)


# -------------------------------------------------
# 1. Attraction
# -------------------------------------------------
class AttractionAdmin(admin.ModelAdmin):
    form = AttractionForm
    list_display = (
        'name', 'province', 'city', 'type', 'ticket_price',
        'display_cover', 'created_at',
    )
    list_filter = ('type', 'province', 'city', 'created_at')
    search_fields = ('name', 'description', 'specific_location')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('基础信息', {
            'fields': ('name', 'description', 'cover')
        }),
        ('位置信息', {
            'fields': ('province', 'city', 'specific_location')
        }),
        ('基本信息', {
            'fields': (
                'type', 'telephone', 'time_reference',
                'opening_hours', 'ticket_price'
            )
        }),
    )

    def display_cover(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" style="height:50px; width:auto; border-radius:4px;" />',
                obj.cover.url
            )
        return "-"

    display_cover.short_description = "封面预览"


admin.site.register(Attraction, AttractionAdmin)


# -------------------------------------------------
# 2. TourPackage
# -------------------------------------------------
class TourPackageForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = '__all__'

    # 校验：结束日期不能早于开始日期
    def clean(self):
        cleaned_data = super().clean()
        current_participants = cleaned_data.get('current_participants')
        max_participants = cleaned_data.get('max_participants')
        if current_participants > max_participants:
            raise ValidationError(
                f"当前报名人数（{current_participants}）不能超过最大容量（{max_participants}）。请重新输入。"
            )

        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if start and end and end < start:
            raise ValidationError("结束日期不能早于开始日期，请重新选择。")
        return cleaned_data


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    form = TourPackageForm
    list_display = (
        'name', 'display_cover', 'start_date', 'end_date', 'base_price', 'discount_percentage', 'current_participants',
        'max_participants', 'status',
    )
    list_filter = (
        'status', 'difficulty_level', 'guide_included',
        'insurance_included', 'start_date', 'transportations',
    )
    search_fields = ('name', 'short_description', 'tags')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('attractions',)
    fieldsets = (
        ('基础信息', {
            'fields': ('name', 'cover', 'short_description', 'description')
        }),
        ('时间', {
            'fields': ('start_date', 'end_date')
        }),
        ('价格 & 折扣', {
            'fields': ('base_price', 'discount_percentage')
        }),
        ('容量 & 状态', {
            'fields': ('min_participants', 'max_participants', 'current_participants', 'status')
        }),
        ('其他信息', {
            'fields': (
                'tags', 'difficulty_level', 'suitable_for', 'guide_included',
                'insurance_included', 'transportations', 'attractions'
            )
        }),
    )

    # 列表页显示缩略图
    def display_cover(self, obj):
        return format_html(
            '<img src="{}" style="width:60px; height:40px; object-fit:cover; border-radius:4px;">',
            obj.cover.url
        )

    display_cover.short_description = "封面"

    # 详情页显示大图预览
    def display_cover_preview(self, obj):
        return format_html(
            '<img src="{}" style="max-width:100%; max-height:400px; border-radius:8px; box-shadow:0 2px 10px rgba(0,0,0,0.1);">',
            obj.cover.url
        )

    display_cover_preview.short_description = "封面预览"

    def discounted_price(self, obj):
        return f"{obj.get_discounted_price:.2f} 元"

    discounted_price.short_description = "折扣后价格"

    # 自定义动作：一键把状态改成“售罄”
    actions = ['make_sold_out']

    def make_sold_out(self, request, queryset):
        queryset.update(status='sold_out')

    make_sold_out.short_description = "将选中行程标记为「售罄」"


# -------------------------------------------------
# 3. Order
# -------------------------------------------------
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'user', 'tour_package_link',
        'contact_name', 'contact_phone', 'created_at',
    )
    list_filter = ('created_at', 'tour_package__status')
    search_fields = (
        'order_number', 'user__username', 'contact_name',
        'contact_phone', 'tour_package__name'
    )
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    def tour_package_link(self, obj):
        url = reverse("admin:your_app_tourpackage_change", args=[obj.tour_package_id])
        return format_html('<a href="{}">{}</a>', url, obj.tour_package.name)

    tour_package_link.short_description = "行程包"


admin.site.register(Order, OrderAdmin)


# -------------------------------------------------
# 4. TourPackageFavorite（行程收藏）
# -------------------------------------------------
class TourPackageFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour_package', 'created_at', 'note_preview')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'tour_package__name', 'note')
    readonly_fields = ('created_at',)

    def note_preview(self, obj):
        if obj.note:
            return obj.note[:30] + ('...' if len(obj.note) > 30 else '')
        return '-'

    note_preview.short_description = "备注预览"


admin.site.register(TourPackageFavorite, TourPackageFavoriteAdmin)


# -------------------------------------------------
# 5. AttractionFavorite（景点收藏）
# -------------------------------------------------
class AttractionFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'attraction', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'attraction__name')
    readonly_fields = ('created_at',)


admin.site.register(AttractionFavorite, AttractionFavoriteAdmin)


# -------------------------------------------------
# 6. AttractionVisited（去过记录）
# -------------------------------------------------
# attractions/admin.py

class AttractionVisitedAdmin(admin.ModelAdmin):
    """
    景点“去过”记录后台管理（精简版）
    """
    list_display = ('user', 'attraction', 'created_at')
    list_filter = ('created_at', 'attraction__province', 'attraction__city')
    search_fields = (
        'user__username',
        'user__email',
        'attraction__name',
    )
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 30

    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'attraction')
        }),
        ('系统记录', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    # 优化查询：避免 N+1
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'attraction', 'attraction__province', 'attraction__city'
        )


admin.site.register(AttractionVisited, AttractionVisitedAdmin)
