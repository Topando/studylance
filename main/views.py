from django.shortcuts import render



def home_page_view(request):
    return render(request, 'main/home_page.html')