#REST 호출이 가능하도록 설정
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core import serializers
from .models import QuizSet, Rank, RankSurvive
from django.db.models import Avg

import random

#=================================================================
# tip 제공기능
tip_list =[
    "tip : 최고 점수는 1000점입니다.",
    "tip : 최저 점수는 -2000점입니다.",
    "tip : 정답 오차범위는 ±1% 입니다. 정답은 +100점을 얻습니다. ",
    "tip : 상품의 최고가격은 100만원입니다.",
    "tip : 가격이 생각과 다를수 있습니다. 하지만 그것이 현실입니다.",
    "tip : 정답과 ±30% 미만으로 차이나는 경우에만 점수를 얻습니다.",
    "tip : 정답과 ±30% 이상으로 차이나는 경우에는 점수를 잃습니다.",
    "tip : 0원을 제출하면 -200점을 받습니다.(패널티)",
    "tip : 총 10 문제가 제시됩니다.",
    "tip : 쇼핑몰 가격기준입니다.",
    "tip : 그림과 문구를 보면 힌트가 보입니다.",
    "tip : 버튼 클릭으로만 작성해야합니다.",
    "tip : 서바이벌 모드는 추후 개발 예정입니다.",
    "tip : 광고 클릭은 개발자 인생에 큰 도움이 됩니다.",
    "tip : 할인율이 크게 적용된(특가)상품은 현재 가격에 반영됩니다. (할인중 표시)",
    "tip : 할인율이 적게 적용된 상품은 할인 전 가격이 반영됩니다.",
]
#=================================================================

# Create your views here.
class Main(APIView):
    """
    메인 홈페이지 출력
    """
    def get(self, request): 
        request.session.flush()
        
        normal_user = Rank.objects.filter(point__lt=1001,point__gte=-2000).count()
        survive_user = RankSurvive.objects.filter(stage__lt=101,stage__gte=1).count()
           
        return render(request,'quiz/index.html',context=dict(
                                                            normal_user=normal_user,
                                                            survive_user=survive_user)
                                                            , status=200) #context html로 넘길것 context=dict(mainfeeds=df)
    
    
class Quiz(APIView):
    """
    퀴즈 일반모드 실행

    Args:
        APIView (_type_): _description_
    """
    def get(self, request): 
        # 현재 점수를 불러오기, 없다면(시작시) 0점으로 시작
        now_score = request.session.get('now_score', 0) 
        #문제의 현재 순번을 받음, 없다면(시작시) 1번째로 시작 
        quiz_count = request.session.get('quiz_count', 1) 

        # a = QuizSet.objects.filter(quiz_id = 29).first()
        # a.delete()
        # a.price= 799000
        # a.category = "공식판매가격 (3월 특가 종료)"
        # a.save()

        # tip 메세지
        tip = random.sample(tip_list, k=1)[0]
        
        # 10문제가 모두 제시된 경우 종료 조건
        if quiz_count>=11:
            # 평균 점수
            mean_score = round(Rank.objects.filter(point__lt=1001,point__gte=-2000).aggregate(point = Avg('point'))['point'],1)
            # 플레이 인원(아웃라이어 삭제 기능 추가)
            users = Rank.objects.filter(point__lt=1001,point__gte=-2000).count()
            
            #점수분포표 데이터 생성
            all = Rank.objects.all().count()
            over500 = Rank.objects.filter(point__gte=500).count()
            over300 = Rank.objects.filter(point__lt=500, point__gte=300).count()
            over150 = Rank.objects.filter(point__lt=300, point__gte=150).count()
            over50 = Rank.objects.filter(point__lt=150, point__gte=50).count()
            over0 = Rank.objects.filter(point__lt=50, point__gte=0).count()
            over_100 = Rank.objects.filter(point__lt=0, point__gte=-100).count()
            over_300 = Rank.objects.filter(point__lt=-100, point__gte=-300).count()
            over_500 = Rank.objects.filter(point__lt=-300, point__gte=-500).count()
            over_700 = Rank.objects.filter(point__lt=-500, point__gte=-700).count()
            over_2000 = Rank.objects.filter(point__lt=-700, point__gte=-2000).count()
            
            # 점수 딕셔너리 저장
            score_dict={
                "all":all,
                "over500":over500,
                "over300":over300,
                "over150":over150,
                "over50":over50,
                "over0":over0,
                "over_100":over_100,
                "over_300":over_300,
                "over_500":over_500,
                "over_700":over_700,
                "over_2000":over_2000,
            }
            # 결과 페이지 출력
            return render(request,'quiz/end.html', context=dict(
                                                                quiz_count=quiz_count,
                                                                users=users,
                                                                now_score=now_score,
                                                                mean_score=mean_score,
                                                                score_dict=score_dict,
                                                                tip=tip,
                                                                ),status=200) #context html로 넘길것 context=dict(mainfeeds=df)

        # 랜덤하게 문제가 나오도록 설계
        # 문제의 순번들을 저장함
        quiz_id_list = request.session.get('quiz_id_list',[])
        # DB 내 문제 id를 받아옴
        quiz_all = list(QuizSet.objects.all().values_list('quiz_id', flat=True))
        
        # 리스트 섞기
        quiz_all = random.sample(quiz_all, len(quiz_all))
        
        # 문제 중복 출제 방지 리스트
        # 퀴즈 id 번호
        for quiz in quiz_all:
            # 같은 퀴즈가 나왔는지 확인
            if quiz in quiz_id_list:
                continue
            # 다른 퀴즈를 뽑을 때까지
            else:
                quiz_id = quiz
                quiz_id_list.append(quiz_id)
                break
        
        # 문제 리스트 저장
        request.session['quiz_id_list'] = quiz_id_list
        # 현재 문제 번호 저장
        request.session['quiz_id'] = quiz_id
        # 번호에 해당하는 문제 가져오기 
        quizset = QuizSet.objects.filter(quiz_id= quiz_id).first()
        
        # DB 내 queryset 호출
        return render(request,'quiz/quiz.html', context=dict(
                                                             quizset=quizset,
                                                             now_score=now_score,
                                                             tip=tip, # tip 메세지
                                                             round_rate=quiz_count*10 , #현재 라운드 진행률
                                                             round=quiz_count # 현재 라운드
                                                             ),status=200) #context html로 넘길것 context=dict(mainfeeds=df)

class CheckAnswer(APIView):
    def get(self, request): 
        # 현재 라운드를 받음
        quiz_count = int(request.session.get('quiz_count',1))
        # quiz id를 받음
        quiz_id = int(request.session.get('quiz_id'))
        # 유저가 입력한 상품정보
        price = int(request.GET.get('price'))  
        print(price)
        # quizset을 가져옴(quizset의 정답(가격)을 가져옴)
        quizset = QuizSet.objects.filter(quiz_id= quiz_id).first()
        answer_price = quizset.price
        #다음문제 session으로 
        request.session['quiz_count'] = int(quiz_count)+1
        

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
                score=-200
        # 클라이언트 조작 방지
        if abs(score)%5!=0:
            return Response(status=400)
        

        result_dict = {
            "quiz_id" : quiz_id,
            "price" : price,
            "answer_price" : answer_price,
            "score" : score,
           
        }
        #json 형태로 html로 전송
        return JsonResponse(data=result_dict, status=200)
    
class CheckAnswerSurvive(APIView):
    def get(self, request): 
        # 현재 라운드를 받음
        quiz_count = int(request.session.get('quiz_count',1))
        # 유저가 입력한 상품정보
        price = int(request.GET.get('price'))  
        # quiz id를 받음
        quiz_id = int(request.session.get('quiz_id'))
        # quizset을 가져옴(quizset의 정답(가격)을 가져옴)
        quizset = QuizSet.objects.filter(quiz_id= quiz_id).first()
        answer_price = quizset.price
        #다음문제 session으로 
        request.session['quiz_count'] = int(quiz_count)+1
        

        #점수계산 로직
        #점수 하락구간 30% 오차 최대     하락 점수 패널티 구간 90%
        # zero division error방지
        if int(price)==int(answer_price):
            score=15
        else:            
            error = abs(round((price-int(answer_price))/int(answer_price),2))
            if error>=0.9:
                score=-15
            elif error>=0.85:
                score=-12
            elif error>=0.80:
                score=-10
            elif error>=0.75:
                score=-8
            elif error>=0.70:
                score=-6
            elif error>=0.65:
                score=-4
            elif error>=0.50:
                score=-3
            elif error>=0.45:
                score=-2
            elif error>=0.40:
                score=-1
            elif error>=0.30:
                score= 3
            elif error>=0.25:
                score= 4
            elif error>=0.20:
                score= 5
            elif error>=0.15:
                score= 7
            elif error>=0.10:
                score= 9
            elif error>=0.05:
                score= 11
            elif error>=0.03:
                score= 13
            elif error>=0.01:
                score=16
            else:
                score=15
            # 대충 하는 유저에 대한 패널티
            if price==0:
                score=-30

        

        result_dict = {
            "quiz_id" : quiz_id,
            "price" : price,
            "answer_price" : answer_price,
            "score" : score,
           
        }
        #json 형태로 html로 전송
        return JsonResponse(data=result_dict, status=200)

    
class UserScore(APIView):
    """_
    유저가 얻은 점수를 받아 session값에 저장하는 함수
    """
    def get(self, request): 
        score = int(request.GET.get('now_score'))  #유저가 얻은 점수 html에서 받아 서버 session값에 저장 
        # 점수 저장
        request.session['now_score']  = score

        return Response(status=200)
    
    
class UploadScore(APIView):
    """
    유저의 점수를 업로드 하는 함수
    """
    def post(self, request): 
        score = request.data.get('score', None) #유저가 얻은 점수
        quiz_count = int(request.session.get('quiz_count'))
    
        if quiz_count==11:
            stage = quiz_count-1
            Rank.objects.create(
                stage=stage,
                point=score)
            
        # 연속 저장 방지
        request.session['quiz_count'] = quiz_count +1
         
        return Response(status=200)
    
class UploadSuriveScore(APIView):
    """
    서바이벌 모드 게임 유저의 점수를 업로드 하는 함수
    """
    def post(self, request):
        quiz_count = int(request.session.get('quiz_count'))    
          
        # 최초업로드인지 확인  
        checker = request.session.get('checker', 0)
        
        if checker==0:
            RankSurvive.objects.create(
                stage=quiz_count,
                )
            # 최초업로드 확인완료  
            request.session['checker'] = checker +1
            return Response(status=200)
        else:
            return Response(status=200)

        
        # # 연속 저장 방지 기술 필요
        # request.session['quiz_count'] = quiz_count +1
        
        return Response(status=200)

    
class SurviveQuiz(APIView):
    def get(self, request):
        # 문제종료 조건 체크    
        now_score = request.session.get('now_score', 60) 
        
        
        #문제의 순번을 받음
        quiz_count = request.session.get('quiz_count', 1) 
        request.session['quiz_count'] = int(quiz_count)
        

        # 게임 종료 조건(문제 100개 해결 또는 점수가 0점에 도달한 경우)
        if (now_score<=0) or (quiz_count>=100):
            # 플레이 유저 수
            users = RankSurvive.objects.filter(stage__lt=101,stage__gte=1).count()
            # 평균 스테이지 수  
            mean_stages = round(RankSurvive.objects.filter(stage__lt=101,stage__gte=1).aggregate(stage = Avg('stage'))['stage'],1)
            
            
            # 유저의 달성 스테이지 = quiz_count
            # 구간별 유저의 비율
            #점수분포표 데이터 생성
            all = RankSurvive.objects.all().count()
            level10 = RankSurvive.objects.filter(stage__gte=75).count()
            level9 = RankSurvive.objects.filter(stage__lt=75,stage__gte=60).count()
            level8 = RankSurvive.objects.filter(stage__lt=60,stage__gte=50).count()
            level7 = RankSurvive.objects.filter(stage__lt=50,stage__gte=40).count()
            level6 = RankSurvive.objects.filter(stage__lt=40,stage__gte=30).count()
            level5 = RankSurvive.objects.filter(stage__lt=30,stage__gte=20).count()
            level4 = RankSurvive.objects.filter(stage__lt=20,stage__gte=15).count()
            level3 = RankSurvive.objects.filter(stage__lt=15,stage__gte=10).count()
            level2 = RankSurvive.objects.filter(stage__lt=10,stage__gte=5).count()
            level1 = RankSurvive.objects.filter(stage__lt=5,stage__gte=0).count()
            
            # 점수 딕셔너리 저장
            level_dict={
                "all": all,
                "level10": level10,
                "level9": level9,
                "level8": level8,
                "level7": level7,
                "level6": level6,
                "level5": level5,
                "level4": level4,
                "level3": level3,
                "level2": level2,
                "level1": level1,
            }
            
            # 1단계 높게 나오는 오류
            quiz_count =quiz_count -1
            return render(request,'quiz/survive_end.html', context=dict(
                                                            mean_stages=mean_stages,
                                                            users=users,
                                                            quiz_count=quiz_count,
                                                            level_dict=level_dict,
                                                            #  round_rate=request.session['quiz_count']*10 ,
                                                            #  round=request.session['quiz_count']
                                                             ),status=200) 
        
        

        # 랜덤하게 문제가 나오도록 설계
        # 문제의 순번들을 저장함
        quiz_id_list = request.session.get('quiz_id_list',[])
        quiz_all = list(QuizSet.objects.all().values_list('quiz_id', flat=True))
        
        # 리스트 섞기
        quiz_all = random.sample(quiz_all, len(quiz_all))
        
        # 퀴즈 id 번호
        for quiz in quiz_all:
            # 같은 퀴즈가 나왔는지 확인
            if quiz in quiz_id_list:
                continue
            # 다른 퀴즈를 뽑을 때까지
            else:
                quiz_id = quiz
                quiz_id_list.append(quiz_id)
                break
                
        request.session['quiz_id_list'] = quiz_id_list
        request.session['quiz_id'] = quiz_id
        
        # quiz_id_list.append(int(quiz_id))
        # request.session['quiz_id_list'] = quiz_id_list
        # print(quiz_id_list)
        

        
        
        quizset = QuizSet.objects.filter(quiz_id= quiz_id).first()
        
        # DB 내 queryset 호출
        return render(request,'quiz/survive.html', context=dict(
                                                             quizset=quizset,
                                                             now_score=now_score,
                                                             quiz_count=quiz_count,
                                                            #  tip=tip,
                                                            #  round_rate=request.session['quiz_count']*10 ,
                                                             round=request.session['quiz_count']),status=200) 
        

    
class SurviveUserScore(APIView):
    """_summary_
    유저의 점수를 session에 저장

    Args:
        APIView (_type_): _description_
    """
    def get(self, request): 
        score = int(request.GET.get('now_score'))  #유저가 얻은 점수
        # 점수 저장
        request.session['now_score']  = score
        
        if score<=0:
            return render(request,'quiz/survive_end.html', context=dict(
                                                            # quizset=quizset,
                                                            score=score,
                                                            # now_score=now_score,
                                                            # quiz_count=quiz_count,
                                                            #  tip=tip,
                                                            #  round_rate=request.session['quiz_count']*10 ,
                                                            #  round=request.session['quiz_count']
                                                             ),status=200) 
        return Response(status=200)
            
