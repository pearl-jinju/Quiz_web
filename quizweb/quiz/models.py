from django.db import models

# Create your models here.

class QuizSet(models.Model):
    quiz_id     = models.IntegerField(primary_key=True) # 퀴즈 id
    name        = models.TextField()   # 상품 이름 
    category    = models.TextField()   # 상품 품종
    price       = models.IntegerField()  # 상품 가격
    img_url     = models.TextField()   # 상품 이미지 url
    url         = models.TextField()   # 상품링크
    num         = models.IntegerField() #퀴즈 순번
    created_at  = models.DateTimeField(auto_now=True)
    
    
class Rank(models.Model):
    id     = models.IntegerField(primary_key=True) # 퀴즈 id
    stage  = models.IntegerField() # 클리어 라운드
    point  = models.IntegerField() # 점수
    created_at           = models.DateTimeField(auto_now=True)
    
class RankSurvive(models.Model):
    id     = models.IntegerField(primary_key=True) # 퀴즈 id
    stage  = models.IntegerField() # 클리어 라운드
    created_at           = models.DateTimeField(auto_now=True)


# 신토불이 퀴즈
class SintoburiQuizList(models.Model):
    id          = models.IntegerField(primary_key=True) # 퀴즈 id
    name        = models.TextField()   # 상품 이름 
    img_count   = models.IntegerField()  # 이미지 개수
    created_at  = models.DateTimeField(auto_now=True)
    
# 신토불이 점수데이터
class SintoburiRank(models.Model):
    id          = models.IntegerField(primary_key=True) # 퀴즈 id
    score        = models.IntegerField()   # 점수
    created_at  = models.DateTimeField(auto_now=True)
    
# 신토불이 정답률 데이터
class SintoburiCorrectRate(models.Model):
    id          = models.IntegerField(primary_key=True) # 퀴즈 id
    quiz_id     = models.IntegerField()   # 해당 퀴즈 ID
    right_or_wrong = models.IntegerField() # 틀렸는지 맞았는지 여부 틀리면 0 맞으면 1
    created_at  = models.DateTimeField(auto_now=True)
    
# LOL 퀴즈
class LolQuizList(models.Model):
    id          = models.IntegerField(primary_key=True) # 퀴즈 id
    name        = models.TextField()   # 아이템 이름 
    img_url     = models.TextField()   # 아이템 이미지 url
    price       = models.IntegerField()  # 아이템 가격
    created_at  = models.DateTimeField(auto_now=True)
    
# LOL 점수데이터
class LolRank(models.Model):
    id          = models.IntegerField(primary_key=True) # 퀴즈 id
    score        = models.IntegerField()   # 점수 
    created_at  = models.DateTimeField(auto_now=True)
    