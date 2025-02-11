"""
URL configuration for starletterProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from index.views import IndexView

urlpatterns = [
    path('gysuths4/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('mybooks/', include('books.urls')),
    path('funeralhalls/', include('funeralhalls.urls')),
    path('bookshelf/', include('bookshelf.urls')),
    path('market/', include('market.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)