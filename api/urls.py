from django.urls import path, include

urlpatterns = [
    path('blog/', include('blog.api.urls')),
    path('user/', include('user.api.urls')),
]
