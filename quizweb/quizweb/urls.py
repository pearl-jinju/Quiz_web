"""quizweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.views.generic import TemplateView
from quiz.views import Main, Quiz, CheckAnswer, UserScore, UploadScore, SurviveQuiz, SurviveUserScore, UploadSuriveScore, CheckAnswerSurvive
from .settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main.as_view()),
    path('quiz/', Quiz.as_view()),
    path('quiz/check', CheckAnswer.as_view()),
    path('quiz/checksurvive', CheckAnswerSurvive.as_view()),
    path('quiz/score', UserScore.as_view()),
    path('quiz/uploadscore', UploadScore.as_view()),
    path('quiz/survive', SurviveQuiz.as_view()),
    path('quiz/survivescore', SurviveUserScore.as_view()),
    path('quiz/uploadsurvivescore', UploadSuriveScore.as_view()),
    # robot.txt. 설정
    path('robots.txt',  TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)