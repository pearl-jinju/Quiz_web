#REST 호출이 가능하도록 설정
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core import serializers
from .models import QuizSet

# Create your views here.
class Main(APIView):
    def get(self, request): 
        # DB 내 queryset 호출
        
        # 세션 삭제
        request.session.flush()
        return render(request,'quiz/index.html',status=200) #context html로 넘길것 context=dict(mainfeeds=df)
    
class Quiz(APIView):
    def get(self, request): 
        

        # 랜덤하게 상품이 나오도록 설계
        quiz_num = request.session.get('num', 1) #문제의 순번을 받음
        request.session['num'] = int(quiz_num)+1
        print(request.session['num'])
        
        # # #문제의 순번들을 저장함
        # quiz_num_list = request.session.get('quiz_num_list',[])
        # quiz_num_list.append(int(quiz_num))
        # request.session['quiz_num_list'] = quiz_num_list
        # print(quiz_num_list)
        

        quizset = QuizSet.objects.filter(quiz_id= quiz_num).first()
        # DB 내 queryset 호출
        return render(request,'quiz/quiz.html', context=dict(quizset = quizset),status=200) #context html로 넘길것 context=dict(mainfeeds=df)

class CheckAnswer(APIView):
    def get(self, request): 
        quiz_num = request.session.get('num')
        price = request.GET.get('price')  #유저가 입력한 상품정보
        quizset = QuizSet.objects.filter(quiz_id= int(quiz_num)).first()
        answer_price = quizset.price
        
        result_dict = {
            "quiz_num" : quiz_num,
            "price" : price,
            "answer_price" : answer_price
        }

        
        return JsonResponse(data=result_dict, status=200)
