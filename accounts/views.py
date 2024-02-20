from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from accounts.forms import AccountAuthenticationForm, CreateUserForm
from django.core.exceptions import ValidationError
from accounts.models import Account

def login_view(request, *args, **kwargs):
	context = {}

	user = request.user

	if user.is_authenticated:
		return redirect('home')
	
	form = AccountAuthenticationForm()
	destination = get_redirect_if_exists(request)

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				request.session['user_id'] = user.id
				request.session['username'] = user.username
				
				login(request, user)
				if destination:
					return redirect(destination)
				else:
					return redirect('home')

	context['login_form'] = form
	return render(request, 'accounts/login.html', context)	

def logout_view(request):
	logout(request)
	return redirect('accounts:login')

def signup_view(request, *args, **kwargs):
	user = request.user

	if user.is_authenticated:
		return redirect('home')	

	context = {}

	if request.POST:
		form = CreateUserForm(request.POST)

		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)

			return redirect('home')
		else:
			context['signup_form'] = form

	else:			
		form = CreateUserForm()
		context['signup_form'] = form

	return render(request, 'accounts/signup.html', context)	

def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect