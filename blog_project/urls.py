"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blog_project.views import HomeView
from django.conf.urls.static import static  # 정적 파일 처리 위해 그에 맞는 URL 패턴 반환
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('blog/', include('blog.urls')),
    path('bookmark/', include('bookmark.urls')),
    path('photo/', include('photo.urls')),
    # MEDIA_URL 요청 오면 django.views.static.serve() 뷰 함수가 처리, 뷰 함수에 document_root 키워드 인자 전달
    # static.serve() 함수는 개발용 / httpd, nginx가 상용
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # static 함수가 반환하는 URL 패턴 추가
