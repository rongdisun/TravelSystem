from django.contrib import admin
from .models import AreaCode
# Register your models here.


@admin.register(AreaCode)
class AreaCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'level', 'pcode', 'pname', 'fullname', 'longitude', 'latitude']
    # 搜索字段
    search_fields = [
        'name',
        'fullname',
    ]
