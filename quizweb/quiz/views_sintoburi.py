#REST 호출이 가능하도록 설정
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core import serializers
from .models import SintoburiQuizList, SintoburiRank, SintoburiCorrectRate
from django.db.models import Avg
import random


class Sintoburi(APIView):
    def get(self, request): 
        # session 정리
        request.session.flush()
        # 유저 정의
        sintoburi_all = SintoburiRank.objects.all().count
        # 퀴즈 개수 정의
        quizes = 20
        #DB에서 id로 문제 추출(10문제), 정렬
        random_id_list = list(SintoburiQuizList.objects.all().values_list('id',flat=True))
        quiz_id_list = sorted(random.sample(random_id_list, k=quizes))
        #각 id별 최대 문제 번호
        random_img_count_list = SintoburiQuizList.objects.filter(id__in=quiz_id_list).all().values_list('img_count',flat=True)
        # 사용할 문제 번호 추출
        quiz_img_count_list = [random.randint(1,i) for i in random_img_count_list]
        # 문제위치를 섞는 더미변수 = 정답지
        answer_list = [random.randint(0,1) for _ in range(quizes)]
        # 문제의 id, 사용할 문제 번호, 정답지 결합리스트 생성
        quiz_data_list = [[quiz_id, img_num, answer] for quiz_id, img_num, answer in zip(quiz_id_list, quiz_img_count_list, answer_list)]
        #문제 순서 섞기
        quiz_data_list = random.sample(quiz_data_list, k=len(quiz_data_list))
        
        #퀴즈 데이터 저장
        request.session['quiz_data_list']  = quiz_data_list
        #유저의 정답 데이터 초기화
        request.session['user_answer_list']  = []
        #퀴즈 라운드 초기화
        request.session['quiz_round']  = 1
        #퀴즈 점수 초기화
        request.session['quiz_score'] = 0
        #DB 저장 확인 기능 초기화
        request.session['checked'] = 0
        
        
        return render(request,'sintoburi/index2.html', context=dict(
                                                                    sintoburi_all=sintoburi_all),status=200)
    
class SintoburiQuiz(APIView):
    def get(self, request):
        # 라운드 정의 
        quiz_round = request.session.get('quiz_round', 1)
        quiz_data_list = request.session.get('quiz_data_list')
        # 유저 제출 정답리스트 불러오기
        user_answer_list = request.session.get('user_answer_list')
               
        # 종료 조건
        if len(user_answer_list)>=20:
            #최종 점수 가져오기
            quiz_score = request.session['quiz_score'] * 5
            
            # DB저장
            if request.session['checked'] ==0:
                # 점수 저장
                SintoburiRank.objects.create(
                    score=quiz_score
                )
                # 문제 정답-오답 기록
                # quiz_id, right_or_wrong
                # 문제지 가져오기
                quiz_data_list = request.session['quiz_data_list'] 
                # 유저 제출 답 가져오기
                user_answer_list = request.session['user_answer_list']
                
                for data, user_data in zip(quiz_data_list,user_answer_list):
                    quiz_id = data[0]
                    answer = data[2]
                    right_or_wrong = 0
                    # 정답 시
                    if answer==user_data:
                        right_or_wrong = 1
                    SintoburiCorrectRate.objects.create(
                                                        quiz_id=quiz_id,
                                                        right_or_wrong=right_or_wrong
                                                        )
                request.session['checked'] = 1 
            

            # nickname 결정
            if quiz_score>=90:
                nickname = "흥성대원군"
                img_name = "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FniLxM%2Fbtr3cCPhuqF%2FCmK919OWTYh3ah2QOgUpE1%2Fimg.png"
            

            elif quiz_score>=70:
                nickname = "위정척사파"
                img_name = "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fcdals8%2Fbtr20zTgeNK%2F5JkW240Xdc9KuQ9X3397k1%2Fimg.png"
                
            elif quiz_score>=40:
                nickname = "온건개화파"
                img_name = "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FVyVMk%2Fbtr24MqKuFt%2FW4RJKcRX201GuqFPbe41ok%2Fimg.png"
                
            elif quiz_score>=20:
                nickname = "급진개화파"
                img_name = "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FJTbiG%2Fbtr20x8WtV1%2FVySvlVk3z1CjXbe4HnNJ31%2Fimg.png"
                
            else:
                nickname = "매국노"
                img_name = "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FWUOjT%2Fbtr2Ri6pz2J%2F2q8b5YxQsgkqWWLBPS3rwK%2Fimg.png"
                
            # 점수분포표 생성
            all = SintoburiRank.objects.all().count()
            over90 = SintoburiRank.objects.filter(score__gte=90).count()
            over70 = SintoburiRank.objects.filter(score__lt=81, score__gte=70).count()
            over40 = SintoburiRank.objects.filter(score__lt=61, score__gte=40).count()
            over20 = SintoburiRank.objects.filter(score__lt=31, score__gte=20).count()
            over0 = SintoburiRank.objects.filter(score__lt=11, score__gte=0).count()
            
            score_dict={
                "all":all,
                "over90":over90,
                "over70":over70,
                "over40":over40,
                "over20":over20,
                "over0":over0,
                }
            user_all = SintoburiRank.objects.all()
            mean_score = round(user_all.aggregate(score = Avg('score'))['score'],1)
            users = user_all.count()
            
            # print(request.session['quiz_data_list'])
            
            return render(request,'sintoburi/quiz_end.html', context=dict(
                                                                        quiz_score=quiz_score,
                                                                        nickname=nickname,
                                                                        img_name=img_name,
                                                                        mean_score=mean_score,
                                                                        users=users,
                                                                        score_dict=score_dict,
                       
                                                                                ),status=200)
            
        # 문제 호출(id, img_num, answer)
        # 호출할 문제 id
        quiz_id = quiz_data_list[quiz_round-1][0]
        name = SintoburiQuizList.objects.filter(id=quiz_id).first().name
        img_num = quiz_data_list[quiz_round-1][1]

        # 이미지명 정의        
        correct_img = str(name)+"_T_"+str(img_num)+".png"
        wrong_img =  str(name)+"_F_"+str(img_num)+".png"
        
        # 정답방향  0 왼쪽, 1 오른쪽
        answer_direction = quiz_data_list[quiz_round-1][2]
        
        # 정답률 가져오기
        answers = SintoburiCorrectRate.objects.filter(quiz_id=quiz_id).count()
        correct_answer = SintoburiCorrectRate.objects.filter(quiz_id=quiz_id, right_or_wrong=1).count()
        correct_rate = str(round(correct_answer/answers,2)*100)[:5]
        
        # 정답 위치 체크
        if answer_direction == 0:
            left_img = correct_img
            right_img = wrong_img
            request.session['correct_answer'] = 0
        elif answer_direction == 1:
            left_img = wrong_img
            right_img = correct_img
            request.session['correct_answer'] = 1
 
        return render(request,'sintoburi/quiz_game.html', context=dict(
                                                                        name=name,
                                                                        left_img=left_img,
                                                                        right_img = right_img,
                                                                        quiz_round=quiz_round,
                                                                        correct_rate=correct_rate
                                                                        
                                                                                ),status=200)
class SintoburiQuizCheck(APIView):
    def get(self, request):
        # 유저의 정답 받기
        user_answer = int(request.GET.get('user_answer'))
        
        
        # 유저의 정답 리스트 보관
        user_answer_list = request.session['user_answer_list']
        user_answer_list.append(user_answer)
        request.session['user_answer_list'] = user_answer_list
        
        # 정답 확인
        if user_answer == request.session['correct_answer']:
            request.session['quiz_score'] = request.session['quiz_score'] +1
        elif  user_answer != request.session['correct_answer']:
            pass
        
        # 라운드 증가
        request.session['quiz_round'] = request.session['quiz_round'] +1
        
        return Response(status=200)
