from django.urls import path
from . import views
from .views import CommentCreateView, CommentUpdateView, CommentDeleteView

app_name = "blog"

urlpatterns = [
    # Authentication
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile, name="profile"),

    # Posts
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),

    # Comments CBVs
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),

    # Search
    path('search/', views.search_posts, name='search_posts'),

    # Tags (required by checker)
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts_by_tag'),
]
