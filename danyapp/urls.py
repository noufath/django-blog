"""danyapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from danynotes import views
from danynotes.views import account_signup_view
from danynotes.views import account_login_view
from danynotes.views import account_logout_view

urlpatterns = [
    # path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('create/', views.blog_create, name='blog_create'),
    path('blog/<int:blog_id>/', views.blog, name='blog'),
    path('blog/<int:blog_id>/update', views.blog_update, name='blog_update'),
    path('blog/<int:blog_id>/delete', views.blog_delete, name='blog_delete'),
    path('add-category/',
         views.AddCategoryView.as_view(), name='add_category'),
    path('category/<str:cats>/', views.CategoryView, name='category'),
    path('tinymce/', include('tinymce.urls')),
    path('search/', views.search, name='search'),
    # override the SignupView of django-allauth
    path('accounts/signup/', view=account_signup_view),
    # override the LoginView of django-allauth
    path('accounts/login/', view=account_login_view, name='account_login'),
    # override the LoginView of django-allauth
    path('accounts/logout/', view=account_logout_view),
    # this is the default config for django-allauth
    path('accounts/', include('allauth.urls')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
