from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage

from .models import *

# Create your views here.
def index(request):
	return render(request, 'twitter/index.html')

def login(request):
	id = request.POST['input_id']
	pw = request.POST['input_pw']
	for user in User.objects.all():
		if id == user.get_id():
			if pw == user.get_pw():
				return HttpResponseRedirect(reverse('timeline', args=[user.uId]))
	msg = "Login failed!"
	return render(request, 'twitter/index.html', {'message' : msg})

def signin(request):
	if request.method == "GET":
		users = User.objects.all();
		return render(request, 'twitter/signin.html', {'users' : users})
	if request.method == "POST":
		id = request.POST['input_id']
		pw = request.POST['input_pw']
		nickname = request.POST['input_nickname']
		gender = request.POST['input_gender']
		email = request.POST['input_email']
		profile = request.FILES['input_profile']
		input_user = User(userName=id, password=pw, email=email, nickname=nickname, gender=gender, profile=profile)
		input_user.save()
		return HttpResponseRedirect(reverse('index'))

def timeline(request, user_id):
	information = User.objects.get(pk=user_id)
	allarticles = Article.objects.all().order_by('-mtime')
	allphotos = [];
	for article in allarticles:
		photos = Photo.objects.filter(aId=article)
		for photo in photos:
			allphotos.append({
				'articleId' : article.aId,
				'photosLocation': photo.photo_location,  
			})
	return render(request, 'twitter/timeline.html', {'information' : information, 'articles' : allarticles, 'allphotos' : allphotos})
	
def mytimeline(request, user_id):
	try:
		user_information = User.objects.get(pk=user_id).get_information
	except User.DoesNotExist:
		raise Http404("User does not exist")
	else:
		try:
			thisauthor = User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return render(request, 'twitter/mytimeline.html', {'information' : user_information})
		else:
			try:
				allmyarticles = Article.objects.filter(author=thisauthor).order_by('-mtime')
				allphotos = [];
				for article in allmyarticles:
					photos = Photo.objects.filter(aId=article)
					for photo in photos:
						allphotos.append({
							'articleId' : article.aId,
							'photosLocation': photo.photo_location,  
						})
			except Article.DoesNotExist:
				return render(request, 'twitter/mytimeline.html', {'information' : user_information})
			else:
				return render(request, 'twitter/mytimeline.html', {'information' : user_information, 'articles': allmyarticles, 'allphotos' : allphotos})

def helpauth(request):
	return render(request, 'twitter/helplogin.html')

def helpfindid(request):
	input_email = request.POST['input_email']
	try:
		user = User.objects.get(email=input_email)
	except User.DoesNotExist:
		raise Http404("User does not exist")
	else:
		msg = "Your ID is " + user.userName + "."
		return render(request, 'twitter/index.html', {'message' : msg})

def helpfindpw(request):
	input_email = request.POST['input_email']
	input_id = request.POST['input_id']
	try:
		user = User.objects.get(email=input_email)
	except User.DoesNotExist:
			raise Http404("User does not exist")
	else:
		if user.userName != input_id:
			raise Http404("User does not exist")
		else:
			user_pw = user.password
			msg = "Your PW is " + user_pw + "."
		return render(request, 'twitter/index.html', {'message' : msg})

def writearticle(request, user_id):
	if request.method == "GET":
		return render(request, 'twitter/article.html', {'user_id': user_id})
	if request.method == "POST":
		context = request.POST['ta_context']
		try:
			user = User.objects.get(pk=request.POST['hidden_user_id'])
			input_article = Article(author=user, context=context)
			input_article.save()
			photo = request.FILES['input_photos']
		except:
			return HttpResponseRedirect(reverse('timeline', args=[user.uId]))
		else:
			input_photo = Photo(aId=input_article, photo_location=photo)
			input_photo.save()
			return HttpResponseRedirect(reverse('timeline', args=[user.uId]))

def modifyarticle(request, article_id):
	article = Article.objects.get(pk=article_id)
	if request.method == "GET":
		photos = Photo.objects.filter(aId=article)
		return render(request,'twitter/article.html', {'article': article, 'photos': photos})
	if request.method == "POST":
		modify_context = request.POST['ta_context']
		article.context = modify_context
		article.save()
		try:
			photo = request.FILES['input_photos']
		except:
			return HttpResponseRedirect(reverse('timeline', args=[article.author.uId]))
		else:
			modify_photo = Photo(aId=article, photo_location=photo)
			modify_photo.save()
			return HttpResponseRedirect(reverse('timeline', args=[article.author.uId]))

def userInfo(request, user_id):	
	if request.method == "GET":
		user = User.objects.get(pk=user_id).get_information
		users = User.objects.all();
		return render(request, 'twitter/modifyinformation.html', {'information' : user, 'users': users})
	if request.method == "POST":
		user = User.objects.get(pk=user_id)
		input_nickname = request.POST['input_nickname']
		input_gender = request.POST['input_gender']
		input_profile = request.FILES['input_profile']
		user.nickname = input_nickname
		user.gender = input_gender
		user.profile = input_profile
		user.save()
		return HttpResponseRedirect(reverse('timeline', args=[user_id]))

def logout(request):
	return HttpResponseRedirect(reverse('index'))	

def uploads(request, file):
	if file[0:8] == 'profile/':
		user = User.objects.get(profile=file)
		return HttpResponse(user.profile)
	if file[0:6] == 'media/':
		photos = Photo.objects.get(photo_location=file)
		return HttpResponse(photos.photo_location)
