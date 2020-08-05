from django.contrib import admin
from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'modify_dt', 'tag_list')
    # modify_dt 컬럼 사용하는 필터 사이드바 보여주도록 지정
    list_filter = ('modify_dt',)
    # 검색박스를 표시하고, 입력된 단어는 title과 content 컬럼에서 검색하도록 함
    search_fields = ('title', 'content')
    # slug 필드는 title 필드를 사용해 미리 채워지도록 함
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')
    
    def tag_list(self, obj):
        return ', '.join(o.name for o in obj.tags.all())