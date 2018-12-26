from django.db import models
from dbms import settings

# Create your //models here.

class customer(models.Model):
    name = models.CharField(max_length=50, primary_key = True)
    mob_no = models.BigIntegerField()
    address = models.CharField(max_length=100)
    def __str__(self):
    	return self.name

class manufacturer(models.Model):
	name = models.CharField(max_length=50, primary_key = True)
	email = models.EmailField()
	address = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class company(models.Model):
	name = models.CharField(max_length=50, primary_key = True)
	phone_no = models.BigIntegerField()
	address = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class branch(models.Model):
	area = models.CharField(max_length=100, primary_key = True)
	address = models.CharField(max_length=100)
	phone_no = models.BigIntegerField()
	email = models.EmailField()
	company = models.ForeignKey(company, on_delete=models.CASCADE)
	class Meta:
		unique_together = (("area", "phone_no"),)
	def __str__(self):
		return str(self.area) +"-"+ str(self.phone_no)

class employee(models.Model):
	id = models.CharField(max_length=5, primary_key = True)
	name = models.CharField(max_length=50)
	mob_no = models.BigIntegerField()
	branch = models.ForeignKey(branch, on_delete=models.CASCADE)
	def __str__(self):
		return self.name
    #branch_phone = models.ForeignKey(branch,related_name = "phone_no", on_delete=models.CASCADE)

class model(models.Model):
	model_id = models.CharField(max_length=5, primary_key=True)
	name = models.CharField(max_length=50)
	weight = models.IntegerField()
	release_date = models.DateField()
	top_speed = models.IntegerField()
	mfg_name = models.ForeignKey(manufacturer, on_delete = models.CASCADE)
	branch = models.ForeignKey(branch, on_delete=models.CASCADE)
	def __str__(self):
		return self.name

class transportation(models.Model):
	t_id = models.CharField(max_length=5, primary_key=True)
	mfg_name = models.ForeignKey(manufacturer, on_delete = models.CASCADE)
	t_date = models.DateField()
	branch = models.ForeignKey(branch, on_delete=models.CASCADE)
	def __str__(self):
		return "From "+str(self.mfg_name)+" to "+str(self.branch)

class sold(models.Model):
	sale_id = models.CharField(max_length=5, primary_key=True)
	price = models.IntegerField()
	sale_date = models.DateField()
	model_id = models.ForeignKey(model, on_delete = models.CASCADE)
	branch = models.ForeignKey(branch, on_delete = models.CASCADE)
	def __str__(self):
		return str(self.sale_id)+" ("+str(self.model_id)+" at "+str(self.branch)+")"

class registration(models.Model):
	id = models.CharField(max_length=5, primary_key=True)
	sale_id = models.ForeignKey(sold, on_delete=models.CASCADE)
	reg_date = models.DateField()
	reg_place = models.CharField(max_length = 100)
	def __str__(self):
		return str(self.id)+' at '+str(self.reg_place)+' on '+str(self.reg_date)

class ins_company(models.Model):
	name = models.CharField(max_length = 100, primary_key=True)
	address = models.CharField(max_length=100)
	phone_no = models.IntegerField()	
	def __str__(self):
		return str(self.name)

class ins_policy(models.Model):
	id = models.CharField(max_length=5, primary_key=True)
	start_date = models.DateField()
	end_date = models.DateField()
	emi = models.IntegerField()
	ins_company = models.ForeignKey(ins_company, on_delete=models.CASCADE)
	sale_id = models.ForeignKey(sold, on_delete=models.CASCADE)
	class Meta:
		unique_together = (("id", "ins_company", "sale_id"),)
	def __str__(self):
		return str(self.id)+'	 '+str(self.ins_company)

class buys(models.Model):
	buy_id = models.CharField(max_length=5, primary_key=True)
	invoice = models.CharField(max_length=100)
	sale_id = models.ForeignKey(sold, on_delete=models.CASCADE)
	branch = models.ForeignKey(branch, on_delete=models.CASCADE)
	customer = models.ForeignKey(customer, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.customer)+'		'+str(self.sale_id)