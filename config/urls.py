"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.views.generic import RedirectView
from users.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetEmailSentView,
    PasswordResetView,
    RegisterView,
)

users_paths = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password-reset/email-sent/",
        PasswordResetEmailSentView.as_view(),
        name="password_reset_email_sent",
    ),
    path(
        "password-reset/<uidb64>/<token>",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("rq/", include("django_rq.urls")),
    # add user routes
    path("users/", include((users_paths, "users"), namespace="users")),
    # other routes
    path("", RedirectView.as_view(pattern_name="users:login"), name="home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
