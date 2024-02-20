from django.shortcuts import render
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET'])
def main_page_view(request):
	return render(request, 'dashboard/index.html', {})

@require_http_methods(['GET'])
def home_page_view(request):
	return render(request, 'dashboard/dashboard.html', {})	