from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection

def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
        return JsonResponse({"stautus":"OK","db":"up"})
    except Exception as e:
        return JsonResponse(
            {"status":"error","db":"down","details":str(e)},
            status=500
        )
