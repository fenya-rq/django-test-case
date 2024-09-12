from django.contrib import admin
from .models import Goods, Images, Parameters


class ImagesAdmin(admin.TabularInline):
    model = Images
    extra = 1


class ParametersAdmin(admin.TabularInline):
    model = Parameters
    extra = 1


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Parameters)
admin.site.register(Images)
