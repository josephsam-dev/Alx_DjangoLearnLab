from django.urls import path
from . import views
from .views import CommentCreateView, CommentUpdateView, CommentDeleteView

app_name = "blog"

urlpatterns = [
    # Authentication
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.register_view, name="register"),  # match function name in views.py
    path("profile/", views.profile, name="profile"),  # required by checker

    # Posts
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),

    # Comments (CBVs)
    path('posts/<int:post_id>/comments/new/', CommentCreateView.as_view(), name='add_comment'),
    path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='edit_comment'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
]
