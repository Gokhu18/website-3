from django.db import models
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
# Create your models here.
class product(models.Model):
	title=models.CharField(max_length=200)
	price=models.CharField(max_length=10)
	description=models.TextField()
	rating=models.FloatField()
	published_date=models.DateTimeField(auto_now=True)
	image=models.ImageField(upload_to='product_image',blank=True)
	s_id=models.ForeignKey('seller',on_delete=models.CASCADE)
	stock=models.IntegerField()
	category=models.IntegerField()
	class Meta:
		db_table="product"
	def publish(self):
		self.published_date=timezone.now()
		self.save()
	def __str__(self):
		return self.title
	def getabsoluteurl(self):
		return "/product/%i/" % self.id
	def rate(self):
		if(int(self.rating)==5):
			return "★ ★ ★ ★ ★"
		elif(int(self.rating)==4):
			return "★ ★ ★ ★ ☆"
		elif(int(self.rating)==3):
			return "★ ★ ★ ☆ ☆"
		elif(int(self.rating)==2):
			return "★ ★ ☆ ☆ ☆"
		elif(int(self.rating)==1):
			return "★ ☆ ☆ ☆ ☆"
		else:
			return "☆ ☆ ☆ ☆ ☆"
class buyer(models.Model):
	b_email=models.CharField(max_length=100,primary_key=True)
	name=models.CharField(max_length=100)
	phno=models.CharField(max_length=20,null=True)
	class Meta:
		db_table="buyer"
class seller(models.Model):
	s_email=models.CharField(max_length=100)
	name=models.CharField(max_length=100)
	address=models.CharField(max_length=200)
	phno=models.CharField(max_length=20)
	class Meta:
		db_table="seller"
class cart(models.Model):
	bid=models.ForeignKey('buyer', on_delete=models.CASCADE,name='bid',null=False)
	pid=models.ForeignKey('product',	on_delete=models.CASCADE,name='pid')
	sid=models.ForeignKey('seller',on_delete=models.CASCADE,name='sid')
	quantity=models.IntegerField()
	price=models.IntegerField()
	class Meta:
		unique_together=(("pid","bid"),)
		db_table="cart"
class order(models.Model):
	bid=models.ForeignKey('buyer',on_delete=models.CASCADE,name='bid',null=False)
	pid=models.ForeignKey('product',on_delete=models.CASCADE,name='pid')
	sid=models.ForeignKey('seller',on_delete=models.CASCADE,name='sid')
	created_at = models.DateTimeField(auto_now_add=True)
	price=models.IntegerField()
	quantity=models.IntegerField()
	address=models.ForeignKey('address',on_delete=models.CASCADE)
	class Meta:
		unique_together=('bid','pid','sid','created_at')
		db_table="order1"
class address(models.Model):
	bid=models.ForeignKey('buyer',on_delete=models.CASCADE,name='bid',null=False)
	name=models.CharField(max_length=20)
	address=models.TextField()
	state=models.CharField(max_length=10)
	pincode=models.IntegerField()
	ccnum=models.CharField(max_length=20)
	exp_month=models.CharField(max_length=10)
	exp_year=models.IntegerField()
	class Meta:
		db_table="address"
class review(models.Model):
	bid=models.ForeignKey('buyer',on_delete=models.CASCADE,name='bid',null=False)
	review=models.TextField()
	rating=models.IntegerField()
	pid=models.ForeignKey('product',on_delete=models.CASCADE,name='pid')
	class Meta:
		unique_together=('bid','pid')
		db_table="review"
