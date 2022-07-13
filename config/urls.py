from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('apps.authentication.urls')),
    path('technics/', include('apps.technics.urls')),
    path('file/', include('apps.files_app.urls')),
    path('tool/', include('apps.tools.urls')),
    path('orders/', include('apps.orders.urls')),
    path('leasing/', include('apps.leasing_agreem.urls')),
    path('g/', include('apps.guarantee_agreem.urls')),
    path('payment-graph/', include('apps.payment_graph.urls')),
    path('act/', include('apps.acts.urls')),
    path('expert/', include('apps.expert_assessment.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
