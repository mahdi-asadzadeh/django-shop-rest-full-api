from django.contrib import admin
from .models import (
    GalleryProduct,
	Product,
    Color,
    Size
)


class ImageProductInline(admin.StackedInline):
	model = GalleryProduct
	

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('status', 'gold_or_jewelry')
    search_fields = ('title', 'slug', 'body')
    inlines = [ImageProductInline]
    prepopulated_fields = {'slug': ('title',)}

    list_display = (
        'rating',
        'title',
        'slug',
        'gold_or_jewelry',
        'status',
        'image_tag'
    )

    
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass
