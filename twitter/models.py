from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
	GENDERCHOICE = (
		('F', 'Female'),
		('M', 'Male'),
	)
	uId = models.AutoField(primary_key=True)
	userName = models.CharField(max_length =40)
	password = models.CharField(max_length=20)
	email = models.CharField(max_length=20)
	nickname = models.CharField(max_length=20)
	gender = models.CharField(max_length=1, choices=GENDERCHOICE)
	birthday = models.DateField(auto_now=False, auto_now_add=False)
	profile = models.ImageField(upload_to='profile/')
	withdrawFlag = models.BooleanField(default=False)
	ctime = models.DateTimeField(auto_now=False, auto_now_add=True)
	mtime = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "id: " + self.userName + ", nickname: " + self.nickname + ", email: " + self.email

	def find_userName(self, input_email):
		if self.email == input_email:
			return True
		else:
			return False

	def find_password(self, input_email, input_userName):
		if self.email == input_email:
			if self.userName == input_userName:
				return True
			else:
				return False
		else:
			return False

	def get_information(self):
		information = {
			"id" : self.uId,
			"nickname" : self.nickname,
			"gender" : self.gender,
			"birthday" : self.birthday,
			"profile" : self.profile,
		}
		return information

	def get_id(self):
		return self.userName

	def get_pw(self):
		return self.password

class Article(models.Model):
	aId = models.AutoField(primary_key=True)
	author = models.ForeignKey(User)
	context = models.CharField(max_length=1000)
	ctime = models.DateTimeField(auto_now=False, auto_now_add=True)
	mtime = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "author: " + self.author.nickname + ", context: " + self.context

class Photo(models.Model):
	pId = models.AutoField(primary_key=True)
	aId = models.ForeignKey(Article)
	photo_location = models.ImageField(upload_to='media/')
	ctime = models.DateTimeField(auto_now=False, auto_now_add=True)
	mtime = models.DateTimeField(auto_now=True)