from django.urls import path
from bookmark.views import BookmarkDV, BookmarkLV

# 애플리케이션 네임스페이스 : URL 패턴의 이름을 정하는 데 사용
app_name = 'bookmark'


urlpatterns = [
    path('', BookmarkLV.as_view(), name='index'),
    path('<int:pk>/', BookmarkDV.as_view(), name='detail'),
]
