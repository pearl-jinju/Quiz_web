#REST 호출이 가능하도록 설정
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core import serializers
from .models import LolQuizList,LolRank
from django.db.models import Avg


import random

#=================================================================
# tip 제공기능
tip_list =[
    "tip : 최고 점수는 1500점입니다.",
    "tip : 최저 점수는 -3000점입니다.",
    "tip : 정답 오차범위는 ±1% 입니다. 정답은 +100점을 얻습니다. ",
    "tip : 정답과 ±20% 미만으로 차이나는 경우에만 점수를 얻습니다.",
    "tip : 정답과 ±20% 이상으로 차이나는 경우에는 점수를 잃습니다.",
    "tip : 0원을 제출하면 -200점을 받습니다.(패널티)",
    "tip : 총 15 문제가 제시됩니다.",
    "tip : 버튼 클릭으로만 작성해야합니다.",
    "tip : 광고 클릭은 개발자 인생에 큰 도움이 됩니다.",
]
#=================================================================

# Create your views here.
class LolMain(APIView):
    """
    메인 홈페이지 출력
    """
    def get(self, request): 
        request.session.flush()
                
        # ls = ["핏빛 칼날","서리불꽃 건틀릿","빗발칼날","잉걸불 칼","대천사의 포옹","굳건한 의지의 완전한 비스킷"]
        # for i in ls :
        #     a = LolQuizList.objects.filter(name=i).first()
        #     a.delete()
            
        # ls = [["원기 회복의 구슬",300],["초시계",750],["심연의 가면",3000],["마나무네",2900],["수호 천사",3000],["필멸자의 운명",3000],['도미닉 경의 인사',3000],['무라마나',3000],['유령 무희',2600],['온기가 필요한 자의 도끼',1000],['태양불꽃 방패',2700],['칠흑의 양날 도끼',3100],['피바라기',3200],['굶주린 히드라',3400],['루난의 허리케인',2600],['라바돈의 죽음모자',3600],['밴시의 장막',2600],['군단의 방패',1200],['내셔의 이빨',3200],['라일라이의 수정홀',2600],['구인수의 격노검',2600],['공허의 지팡이',2800],['란두인의 예언',3000],['몰락한 왕의 검',3300],['맬모셔스의 아귀',2900],['존야의 모래시계',3000],['명석함의 아이오니아 장화',950],['모렐로노미콘',3000],['그림자 검',2300]]
        # for i in ls :
        #     a = LolQuizList.objects.filter(name=i[0]).first()
        #     print(a)
        #     a.price = i[1]
        #     a.save()

        # 유저 수 호출
        lol_user = LolRank.objects.filter(score__lt=1501,score__gte=-3000).count()
        
        # 퀴즈 개수 정의
        quizes = 15
        #DB에서 id로 문제 추출(15문제), 정렬
        random_id_list = list(LolQuizList.objects.all().values_list('id',flat=True))
        quiz_id_list = sorted(random.sample(random_id_list, k=quizes))
        quiz_id_list = random.sample(quiz_id_list, k=len(quiz_id_list))
        
        #퀴즈 데이터 저장
        request.session['quiz_data_list']  = quiz_id_list
        #유저의 정답 데이터 초기화
        request.session['user_answer_list']  = []
        #퀴즈 라운드 초기화
        request.session['quiz_round']  = 1
        #퀴즈 점수 초기화
        request.session['quiz_score'] = 0
        #DB 저장 확인 기능 초기화
        request.session['checked'] = 0     
           
        return render(request,'lol/index.html',context=dict(
                                                            lol_user=lol_user,
                                                            )
                                                            , status=200) #context html로 넘길것 context=dict(mainfeeds=df)
    
    
class LolQuiz(APIView):
    """
    퀴즈 일반모드 실행

    Args:
        APIView (_type_): _description_
    """
    def get(self, request): 

        # 유저의 정답 데이터 로드
        user_answer_list = request.session.get('user_answer_list', [])
        # 현재 점수를 불러오기, 없다면(시작시) 0점으로 시작
        now_score = request.session.get('quiz_score', 0) 
        # 문제의 현재 순번을 받음, 없다면(시작시) 1번째로 시작 
        quiz_count = request.session.get('quiz_count', 1) 

        # tip 메세지
        tip = random.sample(tip_list, k=1)[0]
        
        # 10문제가 모두 제시된 경우 종료 조건
        if len(user_answer_list)>=15:
            quiz_score = request.session['quiz_score']          
            # DB저장
            if request.session['checked'] ==0:
                # 점수 저장
                LolRank.objects.create(
                    score=quiz_score
                )
                
                # 저장 확인
                request.session['checked'] = 1 
                
            

            # 플레이 인원(아웃라이어 삭제 기능 추가)
            users = LolRank.objects.filter(score__lt=1501,score__gte=-3000).count()
            
            #점수분포표 데이터 생성
            all = LolRank.objects.all().count()
            challenger = LolRank.objects.filter(score__gte=1400).count() #챌린저
            grandmaster = LolRank.objects.filter(score__lt=1400, score__gte=1100).count() #그마
            master = LolRank.objects.filter(score__lt=1100, score__gte=900).count() #마스터
            diamond = LolRank.objects.filter(score__lt=900, score__gte=700).count() #다이아
            platinum = LolRank.objects.filter(score__lt=700, score__gte=500).count() #플레
            gold = LolRank.objects.filter(score__lt=500, score__gte=300).count() #골드
            silver = LolRank.objects.filter(score__lt=300, score__gte=100).count() #실버
            bronze = LolRank.objects.filter(score__lt=100, score__gte=0).count() # 브론즈
            iron = LolRank.objects.filter(score__lt=0, score__gte=-300).count() #아이언
            deepsea = LolRank.objects.filter(score__lt=-300).count()  #심해
            
            # 점수 딕셔너리 저장
            score_dict={
                "all":all,
                "challenger":challenger,
                "grandmaster":grandmaster,
                "master":master,
                "diamond":diamond,
                "platinum":platinum,
                "gold":gold,
                "silver":silver,
                "bronze":bronze,
                "iron":iron,
                "deepsea":deepsea,
            }
            
            
            # nickname 결정
            if quiz_score>=1400:
                nickname = "챌린저"
                img_name = "result_챌린저.png"
                share_img = "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FBIf8Z%2Fbtr5Q4XNIYZ%2Foet7WENAkbkSoNAFzkFZo0%2Fimg.png"
            elif quiz_score>=1100:
                nickname = "그랜드마스터"
                img_name = "result_그랜드마스터.png"
                share_img = "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FWFZ6z%2Fbtr5TnbwIAH%2FKR62JjIPKa0BXttlVFw2H1%2Fimg.png"
            elif quiz_score>=900:
                nickname = "마스터"
                img_name = "result_마스터.png"
                share_img ="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbXXHYZ%2Fbtr6haBUMV7%2FcUkLAqR25NKFBuGXuyfJQK%2Fimg.png"
            elif quiz_score>=700:
                nickname = "다이아"
                img_name = "result_다이아.png"
                share_img ="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FSL8h9%2Fbtr5QySsWxn%2Fud95UGlyXskoxe0vQVusKK%2Fimg.png"
            elif quiz_score>=500:
                nickname = "플레티넘"
                img_name = "result_플레티넘.png"
                share_img ="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FpBkyZ%2Fbtr5PSjj8cd%2FUJhOvgDow2bKgsFdyqz2Yk%2Fimg.png"
            elif quiz_score>=300:
                nickname = "골드"
                img_name = "result_골드.png"
                share_img ="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcfrwIO%2Fbtr5Pcbhil2%2FTYr289NwOOclqYWZxBbSu1%2Fimg.png"
            elif quiz_score>=100:
                nickname = "실버"
                img_name = "result_실버.png"
                share_img ="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F9CP1k%2Fbtr5QoPL5Po%2FRDo0PCW7lt7oX2mM1wnpM0%2Fimg.png"
            elif quiz_score>=0:
                nickname = "브론즈"
                img_name = "result_브론즈.png"
                share_img ="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FGBQDw%2Fbtr59ZVambs%2FT0BNiWmBzmA6EkKBB8dcuK%2Fimg.png"
            elif quiz_score>=-300:
                nickname = "아이언"
                img_name = "result_아이언.png"
                share_img ="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FpjdOB%2Fbtr5QnwuBhy%2FKBtbuvqcDWcPKfcOhCkEK0%2Fimg.png"
            else:
                nickname = "심해"
                img_name = "result_심해.png"
                share_img ="https://img1.daumcdn.net/thumb/R1280x0.fjpg/?fname=http://t1.daumcdn.net/brunch/service/user/aYgW/image/VaPosNBYpNJYOaEgzAMgoncIosA"



            # 평균 점수
            mean_score = round(LolRank.objects.filter(score__lt=1501,score__gte=-3000).aggregate(score = Avg('score'))['score'],1)

            # 결과 페이지 출력
            return render(request,'lol/end.html', context=dict(
                                                                quiz_count=quiz_count,
                                                                users=users,
                                                                now_score=now_score,
                                                                mean_score=mean_score,
                                                                score_dict=score_dict,
                                                                nickname=nickname,
                                                                img_name=img_name,
                                                                share_img=share_img
                                                                
                                                                ),status=200) #context html로 넘길것 context=dict(mainfeeds=df)


        # 퀴즈 리스트 가져오기
        quiz_data_list = request.session.get('quiz_data_list', []) 
        

        now_quiz_id = quiz_data_list[quiz_count-1]
        
        # 번호에 해당하는 문제 가져오기 
        quizset = LolQuizList.objects.filter(id= now_quiz_id).first()
        
        # DB 내 queryset 호출
        return render(request,'lol/quiz.html', context=dict(
                                                             quizset=quizset,
                                                             now_score=now_score,
                                                             tip=tip, # tip 메세지
                                                             round=quiz_count # 현재 라운드
                                                             ),status=200) #context html로 넘길것 context=dict(mainfeeds=df)

class LolCheckAnswer(APIView):
    def get(self, request): 
        # 현재 라운드를 받음
        quiz_count = int(request.session.get('quiz_count',1))
        
        # 퀴즈 리스트 가져오기
        quiz_data_list = request.session.get('quiz_data_list', []) 
        
        # quiz id를 받음
        quiz_id =  quiz_data_list[quiz_count-1]
        # 유저가 입력한 상품정보
        price = int(request.GET.get('price'))  
        # quizset을 가져옴(quizset의 정답(가격)을 가져옴)
        quizset = LolQuizList.objects.filter(id= quiz_id).first()
        answer_price = quizset.price
        #다음문제 session으로 
        request.session['quiz_count'] = int(quiz_count)+1

        
        user_answer_list = request.session['user_answer_list'] 
        user_answer_list.append(quiz_id) 
        request.session['user_answer_list']  = user_answer_list
        

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
                score=-60
            elif error>=0.75:
                score=-50
            elif error>=0.70:
                score=-40
            elif error>=0.65:
                score=-35
            elif error>=0.50:
                score=-30
            elif error>=0.45:
                score=-25
            elif error>=0.40:
                score=-20
            elif error>=0.30:
                score= -15
            elif error>=0.25:
                score= -10
            elif error>=0.20:
                score= -5
            elif error>=0.15:
                score= 10
            elif error>=0.10:
                score= 15
            elif error>=0.05:
                score= 25
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
        
        now_score = request.session.get('quiz_score', 0) 
        request.session['quiz_score'] = now_score+score
        

        result_dict = {
            "quiz_id" : quiz_id,
            "price" : price,
            "answer_price" : answer_price,
            "score" : score,
           
        }
        #json 형태로 html로 전송
        return JsonResponse(data=result_dict, status=200)
    
    
class LolUserScore(APIView):
    """_
    유저가 얻은 점수를 받아 session값에 저장하는 함수
    """
    def get(self, request): 
        score = int(request.GET.get('now_score'))  #유저가 얻은 점수 html에서 받아 서버 session값에 저장 
        # 점수 저장
        request.session['now_score']  = score

        return Response(status=200)
    
    
# class LolUploadScore(APIView):
#     """
#     유저의 점수를 업로드 하는 함수
#     """
#     def post(self, request): 
#         score = request.data.get('score', None) #유저가 얻은 점수
#         quiz_count = int(request.session.get('quiz_count'))
    
#         if quiz_count==11:
#             stage = quiz_count-1
#             LolRank.objects.create(
#                 stage=stage,
#                 score=score)
            
#         # 연속 저장 방지
#         request.session['quiz_count'] = quiz_count +1
         
#         return Response(status=200)
    
    
class LolUserScore(APIView):
    """_
    유저가 얻은 점수를 받아 session값에 저장하는 함수
    """
    def get(self, request): 
        score = int(request.GET.get('now_score'))  #유저가 얻은 점수 html에서 받아 서버 session값에 저장 
        # 점수 저장
        request.session['now_score']  = score

        return Response(status=200)