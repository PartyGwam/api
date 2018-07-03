from django.urls import path
from api.parties.comments.views import CommentAPIView, CommentDetailAPIView

app_name = 'comments'

urlpatterns = [
    path('', CommentAPIView.as_view()),
    path('<str:slug>/', CommentDetailAPIView.as_view()),
]
