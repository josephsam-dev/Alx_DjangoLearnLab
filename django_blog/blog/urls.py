from django.urls import path
from . import views
from .views import CommentCreateView, CommentUpdateView, CommentDeleteView

app_name = "blog"

urlpatterns = [
    # Authentication
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile, name="profile"),

    # Posts
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),

    # Comments (CBVs)
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
]
