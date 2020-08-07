from django.urls import path
# from bookmark.views import BookmarkDV, BookmarkLV
from bookmark import views

# 애플리케이션 네임스페이스 : URL 패턴의 이름을 정하는 데 사용
app_name = 'bookmark'


urlpatterns = [
    path('', views.BookmarkLV.as_view(), name='index'),
    path('<int:pk>/', views.BookmarkDV.as_view(), name='detail'),
    # /bookmark/add/
    path('add/', views.BookmarkCreateView.as_view(), name='add'),
    # /bookmark/change/
    path('change/', views.BookmarkChangeLV.as_view(), name='change'),
    # /bookmark/99/update/
    path('<int:pk>/update/', views.BookmarkUpdateView.as_view(), name='update'),
    # /bookmark/99/delete/
    path('<int:pk>/delete/', views.BookmarkDeleteView.as_view(), name='delete'),
]
