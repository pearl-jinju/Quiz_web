#REST 호출이 가능하도록 설정
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core import serializers
from .models import QuizSet, Rank
from django.db.models import Avg

import random

# Create your views here.
class Main(APIView):
    def get(self, request): 
        request.session.flush()

            
        return render(request,'quiz/index.html',status=200) #context html로 넘길것 context=dict(mainfeeds=df)
    
class Quiz(APIView):
    def get(self, request): 
        # 문제종료 조건 체크
        
        

        now_score = request.session.get('now_score', 0) 
        mean_score = round(Rank.objects.aggregate(point = Avg('point'))['point'],1)
        
        #문제의 순번을 받음
        quiz_count = request.session.get('quiz_count', 0) 
        request.session['quiz_count'] = int(quiz_count)+1
        
        # tip 제공기능
        tip_list =[
            "tip : 최고 점수는 1000점입니다.",
            "tip : 최저 점수는 -2000점입니다.",
            "tip : 정답 오차범위는 ±1% 입니다. 정답은 +100점을 얻습니다. ",
            "tip : 상품의 최고가격은 100만원입니다.",
            "tip : 가격이 생각과 다를수 있습니다. 하지만 그것이 현실입니다.",
            "tip : 정답과 ±30% 미만으로 차이나는 경우에만 점수를 얻습니다.",
            "tip : 정답과 ±30% 이상으로 차이나는 경우에는 점수를 잃습니다.",
            "tip : 0원을 제출하면 -200점을 받습니다.",
            "tip : 총 10 문제가 제시됩니다.",
            "tip : 쇼핑몰 가격기준입니다.",
            "tip : 그림과 문구를 보면 힌트가 보입니다.",
            "tip : 버튼클릭으로만 작성해야합니다.",
        ]
        
        tip = random.sample(tip_list, k=1)[0]
        
        if request.session['quiz_count']>=11:
            

            return render(request,'quiz/end.html', context=dict(quiz_count = quiz_count,now_score=now_score, mean_score=mean_score, tip=tip),status=200) #context html로 넘길것 context=dict(mainfeeds=df)
            

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
        
        request.session['quiz_num'] = quiz_num
        
        # quiz_num_list.append(int(quiz_num))
        # request.session['quiz_num_list'] = quiz_num_list
        # print(quiz_num_list)
        

        quizset = QuizSet.objects.filter(quiz_id= quiz_num).first()
        
        # DB 내 queryset 호출
        return render(request,'quiz/quiz.html', context=dict(quizset = quizset,now_score=now_score, tip=tip, round_rate=request.session['quiz_count']*10 ,round=request.session['quiz_count']),status=200) #context html로 넘길것 context=dict(mainfeeds=df)

class CheckAnswer(APIView):
    def get(self, request): 
        quiz_count = int(request.session.get('quiz_count'))
        quiz_num = int(request.session.get('quiz_num'))
        price = int(request.GET.get('price'))  #유저가 입력한 상품정보
        quizset = QuizSet.objects.filter(quiz_id= quiz_num).first()
        answer_price = quizset.price
        

        #점수계산 로직
        #점수 하락구간 30% 오차 최대     하락 점수 패널티 구간 90%
        # zero division error방지
        if int(price)==int(answer_price):
            score=100
        else:            
            error = abs(round((price-int(answer_price))/int(answer_price),2))
            if error>=0.9:
                score=-100
            elif error>=0.85:
                score=-75
            elif error>=0.80:
                score=-50
            elif error>=0.75:
                score=-45
            elif error>=0.70:
                score=-35
            elif error>=0.65:
                score=-25
            elif error>=0.50:
                score=-20
            elif error>=0.45:
                score=-15
            elif error>=0.40:
                score=-10
            elif error>=0.30:
                score= 15
            elif error>=0.25:
                score= 20
            elif error>=0.20:
                score= 25
            elif error>=0.15:
                score= 30
            elif error>=0.10:
                score= 35
            elif error>=0.05:
                score= 40
            elif error>=0.03:
                score= 50
            elif error>=0.01:
                score=100
            else:
                score=100
            # 대충 하는 유저에 대한 패널티
            if price==0:
                score=-250
            
       
        
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
    
    
class UploadScore(APIView):
    def post(self, request): 
        score = request.data.get('score', None) #유저가 얻은 점수
    
        
        quiz_count = int(request.session.get('quiz_count'))
        if quiz_count==11:
            stage = quiz_count-1
            Rank.objects.create(
                stage=stage,
                point=score)
         
        return Response(status=200)