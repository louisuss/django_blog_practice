from django.contrib import admin
from photo.models import Album, Photo


# Album 객체 보여줄 때 객체에 연결된 사진 객체들 같이 보여줄 수 있음
# StackedInline - 세로 나열 방식
# TabularInline - 테이블 모양처럼 행으로 나열되는 형식
class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 2


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    inlines = (PhotoInline,)
    list_display = ('id', 'name', 'description')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'upload_dt')
