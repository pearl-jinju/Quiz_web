#REST 호출이 가능하도록 설정
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core import serializers
from .models import QuizSet

import random

# Create your views here.
class Main(APIView):
    def get(self, request): 
        request.session.flush()

            
        return render(request,'quiz/index.html',status=200) #context html로 넘길것 context=dict(mainfeeds=df)
    
class Quiz(APIView):
    def get(self, request): 
        now_score = request.session.get('now_score', 0) 
        
        #문제의 순번을 받음
        quiz_count = request.session.get('quiz_count', 0) 
        request.session['quiz_count'] = int(quiz_count)+1
        print("현재라운드",request.session['quiz_count'])

        # 랜덤하게 문제가 나오도록 설계
        # 문제의 순번들을 저장함
        quiz_num_list = request.session.get('quiz_num_list',[])
        
        quiz_all = list(QuizSet.objects.all().values_list('quiz_id', flat=True))
        
        # 리스트 섞기
        quiz_all = random.sample(quiz_all, len(quiz_all))
        
        # 퀴즈 id 번호
        for quiz in quiz_all:
            # 같은 퀴즈가 나왔는지 확인
            if quiz in quiz_num_list:
                continue
            # 다른 퀴즈를 뽑을 때까지
            else:
                quiz_num = quiz
                quiz_num_list.append(quiz_num)
                break
                
        request.session['quiz_num_list'] = quiz_num_list
        print("현재뽑힌상품",quiz_num_list)
        
        request.session['quiz_num'] = quiz_num
        
        # quiz_num_list.append(int(quiz_num))
        # request.session['quiz_num_list'] = quiz_num_list
        # print(quiz_num_list)
        

        quizset = QuizSet.objects.filter(quiz_id= quiz_num+1).first()
        
        # DB 내 queryset 호출
        return render(request,'quiz/quiz.html', context=dict(quizset = quizset,now_score=now_score),status=200) #context html로 넘길것 context=dict(mainfeeds=df)

class CheckAnswer(APIView):
    def get(self, request): 
        quiz_count = int(request.session.get('quiz_count'))
        quiz_num = int(request.session.get('quiz_num'))
        price = int(request.GET.get('price'))  #유저가 입력한 상품정보
        quizset = QuizSet.objects.filter(quiz_id= quiz_count).first()
        answer_price = quizset.price
        
        #점수계산 로직
        #점수 하락구간 30% 오차 최대     하락 점수 패널티 구간 90%
        error = abs(round((price-int(answer_price))/int(answer_price),2))
        if error>=0.9:
            score=-200
        elif error>=0.85:
            score=-150
        elif error>=0.80:
            score=-100
        elif error>=0.75:
            score=-90
        elif error>=0.70:
            score=-70
        elif error>=0.65:
            score=-50
        elif error>=0.50:
            score=-40
        elif error>=0.45:
            score=-30
        elif error>=0.40:
            score=-20
        elif error>=0.30:
            score= 30
        elif error>=0.25:
            score= 40
        elif error>=0.20:
            score= 50
        elif error>=0.15:
            score= 60
        elif error>=0.10:
            score= 70
        elif error>=0.05:
            score= 85
        elif error>=0.03:
            score= 95
        elif error>=0.01:
            score= 200
       
        
        result_dict = {
            "quiz_num" : quiz_num,
            "price" : price,
            "answer_price" : answer_price,
            "score" : score
        }

        
        return JsonResponse(data=result_dict, status=200)
    
    
class UserScore(APIView):
    def get(self, request): 
        score = int(request.GET.get('now_score'))  #유저가 얻은 점수
        
        
        # 저장할 값
        quiz_num = request.session.get('num', 0) 
        # 점수 저장
        request.session['now_score']  = score
        
    
        
        return Response(status=200)
