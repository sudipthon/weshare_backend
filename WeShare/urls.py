"""
URL configuration for WeShare project.

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
from rest_framework.routers import DefaultRouter


from django.conf import settings
from django.conf.urls.static import static


from Posts.views import *
from Account.views import UserViewSet
from Message.views import *

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"users", UserViewSet)

# router.register(r"conversation", ConversationViewSet, basename="conversation")
# router.register(r'message', MessageViewSet,basename='message')

# from rest_framework_nested import routers

# conversations_router = routers.NestedSimpleRouter(
#     router, r"conversation", lookup="conversation"
# )
# conversations_router.register(
#     r"message", MessageViewSet, basename="conversation-messages"
# )

urlpatterns = [
    # ... other url patterns ...
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    # path("api/", include(conversations_router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
