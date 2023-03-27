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
from quiz.viewhome  import Home
from quiz.views import Main, Quiz, CheckAnswer, UserScore, UploadScore, SurviveQuiz, SurviveUserScore, UploadSuriveScore, CheckAnswerSurvive
from quiz.views_sintoburi import Sintoburi, SintoburiQuiz, SintoburiQuizCheck
from quiz.views_lolitem import LolMain, LolQuiz, LolUserScore, LolCheckAnswer
from .settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    
    # 메인 홈
    path('home/', Home.as_view()),
    
    # 가격 맞히기
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
    
    # 신토불이 게임
    path('home/sintoburi/', Sintoburi.as_view()),
    path('home/sintoburi/quiz', SintoburiQuiz.as_view()),
    path('home/sintoburi/check', SintoburiQuizCheck.as_view()),
    
    # 롤 아이템 맞추기
    path('home/lolquiz/', LolMain.as_view()),
    path('home/lolquiz/quiz', LolQuiz.as_view()),
    path('home/lolquiz/check', LolCheckAnswer.as_view()),
    path('home/lolquiz/score', LolUserScore.as_view()),


    

    # robot.txt. 설정
    path('robots.txt',  TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)