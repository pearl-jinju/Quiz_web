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
    
    
class Rank(models.Model):
    id     = models.IntegerField(primary_key=True) # 퀴즈 id
    stage  = models.IntegerField() # 클리어 라운드
    point  = models.IntegerField() # 점수
