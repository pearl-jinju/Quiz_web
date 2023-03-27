#REST 호출이 가능하도록 설정
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core import serializers
from .models import SintoburiQuizList, SintoburiRank, Rank, RankSurvive, LolRank
from django.db.models import Avg
import random


class Home(APIView):
    def get(self, request):
        normal_user = Rank.objects.filter(point__lt=1001,point__gte=-2000).count()
        survive_user = RankSurvive.objects.filter(stage__lt=101,stage__gte=1).count()
        howmuch_all = normal_user+survive_user
        
        sintoburi_all = SintoburiRank.objects.all().count
        
        lolquiz_all = LolRank.objects.all().count

        return render(request,'home/home.html', context=dict(
                                                    howmuch_all=howmuch_all,
                                                    sintoburi_all=sintoburi_all,
                                                    lolquiz_all=lolquiz_all
            
                                                              ),status=200)
