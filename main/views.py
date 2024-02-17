from django.shortcuts import render

from app.db_handler.db_update import database_filling


def home_page_view(request):
    return render(request, 'main/home_page.html')
