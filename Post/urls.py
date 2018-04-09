from django.urls import path
from . import views

urlpatterns = [
  path('',views.index,name="index"),
  path('signup/',views.signup,name="signup"),
  path('login/',views.login,name="login"),
  path('logout/',views.log_out,name="logout"),
  path('create/article/',views.createArticle,name="createArticle"),
  path('articles/',views.getArticles,name="articles"),
  path('article/<int:blog_id>/',views.getArticle,name="article"),
  path('post/comment/<int:blog_id>',views.postComment,name="postcomment"),
  path('like/<int:blog_id>',views.increaseLike,name="likepost"),
  path('profile/',views.getProfile,name='userprofile'),
  path('edit/profile/<int:user_id>/',views.editProfile,name='editprofile')
]