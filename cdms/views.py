from django.apps import apps
from django.db.models import Count

from django.views import generic

from django.db import connection
from django.shortcuts import render
from cdms.models import customer, company, manufacturer, branch, employee, model, transportation, sold, registration, ins_company, ins_policy, buys
from django.template.loader import get_template

# Create your views here.

def main_page(request):
	#tables = company.objects.all()
	tables = ['customer', 'company', 'manufacturer', 'branch', 'employee', 'model', 'transportation', 'sold', 'registration', 'ins_company', 'ins_policy', 'buys']
	#tables = Model.objects.model._meta.company
	#tables = apps.get_app_config("cdms").get_models()
	#print(tables)
	context = {'all_tables' : tables}
	return render(request, 'cdms/main_page.html', context)

def disp_table(request,table_name):
	all_instances = []
	formatt = dict()
	if table_name == 'customer':
		all_instances = customer.objects.all()
		formatt = {'cols' : ['customer names']}
	if table_name == 'company':
		all_instances = company.objects.all()
		formatt = {'cols' : ['comapny names']}
	if table_name == 'manufacturer':
		all_instances = manufacturer.objects.all()
		formatt = {'cols' : ['manufacturer names']}
	if table_name == 'branch':
		all_instances = branch.objects.all()
		formatt = {'cols' : ['branch area', 'branch phone_no']}
	if table_name == 'employee':
		all_instances = employee.objects.all()
		formatt = {'cols' : ['employee name']}
	if table_name == 'model':
		all_instances = model.objects.all()
		formatt = {'cols' : ['model name']}
	if table_name == 'transportation':
		all_instances = transportation.objects.all()
		formatt = {'cols' : ['manufacturer name', 'branch area-branch phone_no']}
	if table_name == 'sold':
		all_instances = sold.objects.all()
		formatt = {'cols' : ['saleID', 'model name', 'branch area-branch phone_no']}
	if table_name == 'registration':
		all_instances = registration.objects.all()
		formatt = {'cols' : ['registrationID', 'registration place', 'registration date']}
	if table_name == 'ins_company':
		all_instances = ins_company.objects.all()
		formatt = {'cols' : ['company name']}
	if table_name == 'ins_policy':
		all_instances = ins_policy.objects.all()
		formatt = {'cols' : ['policy_id', 'policy company name']}
	if table_name == 'buys':
		all_instances = buys.objects.all()
		formatt = {'cols' : ['customer name', 'saleID','model name', 'branch area - branch phone_no']}
	formatt['all_instances'] = all_instances
	formatt['table_name'] = table_name
	return render(request, 'cdms/disp_table.html', formatt)

'''def customer_query(request):
	context = {'customers':customer.objects.all(), 'all_mfg':model.objects.all(),}
	return render(request, 'cdms/customer_query.html', context)
'''

def cust_query_disp(request):
	context = {'cols':['customer_name', 'manufacturer name']}
	select_cust = customer.objects.get(name = request.POST['cust_name'])
	select_mfg = manufacturer.objects.get(name = request.POST['mfg_name'])
	select_sort = request.POST['sort']
	cust_results = buys.objects.filter(customer = select_cust.name).order_by('-customer').values('sale_id')
	sold_results = []
	for result in cust_results:
		now = result['sale_id']
		sold_results.append(sold.objects.filter(sale_id = now).values('model_id'))
	model_results = []
	for result in sold_results:
		now = str(result).split("'")[3]
		print(now)
		model_results.append(str(model.objects.filter(model_id = now).values('mfg_name')).split("'")[3])
	if select_sort == 'manufacturer name':
		model_results.sort()
	for result in model_results:
		model_results[model_results.index(result)] = str(select_cust)+'-------'+result
	context['results1'] = model_results

	return render(request, 'cdms/disp_queries.html', context)

def branch_query(request):
	context = {'branchs':branch.objects.all(),}
	return render(request, 'cdms/branch_query.html', context)

def branch_query_disp(request):
	context = {'cols':['branch area - phone_no', 'models sold']}
	branch_models = branch.objects.get(area = request.POST['branch'])
	branch_maxmin = request.POST['maxmin']
	branch_results = model.objects.filter(branch = branch_models).values('model_id')
	results1 = list()
	for result in branch_results:
		results1.append(str(branch_models)+'-----'+str(result).split("'")[3])

	all_branch = branch.objects.all()
	branchs = [[branch,0] for branch in all_branch]
	maxx = branchs[0]
	if branch_maxmin == "max":
		for b in branchs:
			b[1] = len(sold.objects.filter(branch = b[0]).values('model_id'))
			if b[1] > maxx[1]:
				maxx = b
		context['results2'] = [maxx[0], maxx[1]]
	if branch_maxmin == "min":
		for b in branchs:
			b[1] = len(sold.objects.filter(branch = b[0]).values('model_id'))
			if b[1] < maxx[1]:
				maxx = b
		context['results2'] = [maxx[0], maxx[1]]

	context['results1'] = results1 

	return render(request, 'cdms/disp_queries.html', context)


class customerCreate(generic.CreateView):
	model = customer
	fields = ['name', 'mob_no', 'address']
	success_url = '/main/customer/'
	template_name = 'cdms/create.html'

class companyCreate(generic.CreateView):
	model = company
	fields = ['name', 'phone_no', 'address']
	success_url = '/main/company/'
	template_name = 'cdms/create.html'

class manufacturerCreate(generic.CreateView):
	model = manufacturer
	fields = ['name', 'email', 'address']
	success_url = '/main/manufacturer/'
	template_name = 'cdms/create.html'

class branchCreate(generic.CreateView):
	model = branch
	fields = ['area', 'address', 'phone_no', 'email', 'company']
	success_url = '/main/branch/'
	template_name = 'cdms/create.html'

class employeeCreate(generic.CreateView):
	model = employee
	fields = ['id', 'name', 'mob_no', 'branch']
	success_url = '/main/employee/'
	template_name = 'cdms/create.html'

class modelCreate(generic.CreateView):
	model = model
	fields = ['model_id', 'name', 'weight', 'release_date', 'top_speed', 'mfg_name', 'branch']
	success_url = '/main/model/'
	template_name = 'cdms/create.html'

class transportationCreate(generic.CreateView):
	model = transportation
	fields = ['t_id', 'mfg_name', 't_date', 'branch']
	success_url = '/main/transportation/'
	template_name = 'cdms/create.html'

class soldCreate(generic.CreateView):
	model = sold
	fields = ['sale_id', 'price', 'sale_date', 'model_id', 'branch']
	success_url = '/main/sold/'
	template_name = 'cdms/create.html'

class registrationCreate(generic.CreateView):
	model = registration
	fields = ['id', 'sale_id', 'reg_date', 'reg_place']
	success_url = '/main/registration/'
	template_name = 'cdms/create.html'

class ins_companyCreate(generic.CreateView):
	model = ins_company
	fields = ['name', 'address', 'phone_no']
	success_url = '/main/ins_company/'
	template_name = 'cdms/create.html'

class ins_policyCreate(generic.CreateView):
	model = ins_policy
	fields = ['id', 'start_date', 'end_date', 'emi', 'ins_company', 'sale_id']
	success_url = '/main/ins_policy/'
	template_name = 'cdms/create.html'

class buysCreate(generic.CreateView):
	model = buys
	fields = ['buy_id', 'invoice', 'sale_id', 'branch']
	success_url = '/main/buys/'
	template_name = 'cdms/create.html'


class customerUpdate(generic.UpdateView):
	model = customer
	fields = ['name', 'mob_no', 'address']
	template_name = 'cdms/Update.html'
	success_url = '/main/customer/'

class companyUpdate(generic.UpdateView):
	model = company
	fields = ['name', 'phone_no', 'address']
	success_url = '/main/company/'
	template_name = 'cdms/Update.html'

class manufacturerUpdate(generic.UpdateView):
	model = manufacturer
	fields = ['name', 'email', 'address']
	success_url = '/main/manufacturer/'
	template_name = 'cdms/Update.html'

class branchUpdate(generic.UpdateView):
	model = branch
	fields = ['area', 'address', 'phone_no', 'email', 'company']
	success_url = '/main/branch/'
	template_name = 'cdms/Update.html'

class employeeUpdate(generic.UpdateView):
	model = employee
	fields = ['id', 'name', 'mob_no', 'branch']
	success_url = '/main/employee/'
	template_name = 'cdms/Update.html'

class modelUpdate(generic.UpdateView):
	model = model
	fields = ['model_id', 'name', 'weight', 'release_date', 'top_speed', 'mfg_name', 'branch']
	success_url = '/main/model/'
	template_name = 'cdms/Update.html'

class transportationUpdate(generic.UpdateView):
	model = transportation
	fields = ['t_id', 'mfg_name', 't_date', 'branch']
	success_url = '/main/transportation/'
	template_name = 'cdms/Update.html'

class soldUpdate(generic.UpdateView):
	model = sold
	fields = ['sale_id', 'price', 'sale_date', 'model_id', 'branch']
	success_url = '/main/sold/'
	template_name = 'cdms/Update.html'

class registrationUpdate(generic.UpdateView):
	model = registration
	fields = ['id', 'sale_id', 'reg_date', 'reg_place']
	success_url = '/main/registration/'
	template_name = 'cdms/Update.html'

class ins_companyUpdate(generic.UpdateView):
	model = ins_company
	fields = ['name', 'address', 'phone_no']
	success_url = '/main/ins_company/'
	template_name = 'cdms/Update.html'

class ins_policyUpdate(generic.UpdateView):
	model = ins_policy
	fields = ['id', 'start_date', 'end_date', 'emi', 'ins_company', 'sale_id']
	success_url = '/main/ins_policy/'
	template_name = 'cdms/Update.html'

class buysUpdate(generic.UpdateView):
	model = buys
	fields = ['buy_id', 'invoice', 'sale_id', 'branch']
	success_url = '/main/buys/'
	template_name = 'cdms/Update.html'

def delete(request, table_name, pk):
	customer.objects.get(pk = pk).delete()
	tables = ['customer', 'company', 'manufacturer', 'branch', 'employee', 'model', 'transportation', 'sold', 'registration', 'ins_company', 'ins_policy', 'buys']
	#tables = Model.objects.model._meta.company
	#tables = apps.get_app_config("cdms").get_models()
	#print(tables)
	context = {'all_tables' : tables}
	return render(request, 'cdms/main_page.html', context)


#queries
#customer
def customer_queries(request):
	context = {"querylist" : ["cust_model","cust_count_cars"], }
	return render(request, 'cdms/querylist.html', context)

def cust_model(request):
	context = {'customers':customer.objects.all()}
	return render(request, 'cdms/cust_model.html', context)

def cust_model_disp(request):
	with connection.cursor() as cursor:
		customer = request.POST['cust_name']
		cursor.execute("SELECT b.customer_id, m.model_id, m.name FROM cdms_buys as b, cdms_sold as s, cdms_model as m WHERE b.customer_id =%s AND s.sale_id = b.sale_id_id AND s.model_id_id = m.model_id ORDER BY m.name",[customer])
		context = {"result": [c for c in cursor.fetchall()], "cols":["customers", "model_ids", "model_names"]}
		return render(request, 'cdms/disp_queries.html', context)

def cust_count_cars_disp(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT b.customer_id, count(*) FROM cdms_buys as b group by(b.customer_id) order by (count(*)) desc")
		context = {"result": [c for c in cursor.fetchall()], "cols":["customer", "count"]}
		return render(request, 'cdms/disp_queries.html', context)

#company
def company_queries(request):
	context = {"querylist" : ["company_branch", "company_count_branchs"], }
	return render(request, 'cdms/querylist.html', context)

def company_branch(request):
	context = {'companys':company.objects.all()}
	return render(request, 'cdms/company_branch.html', context)

def company_branch_disp(request):
	with connection.cursor() as cursor:
		company = request.POST['company_name']
		cursor.execute("SELECT  c.name, b.area, b.phone_no FROM cdms_company as c, cdms_branch as b WHERE b.company_id = c.name AND c.name = %s",[company])
		context = {"result": [c for c in cursor.fetchall()], "cols":["company_name", "branch_area", "branch_phone"]}
		return render(request, 'cdms/disp_queries.html', context)

def company_count_branchs_disp(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT b.company_id, count(*) FROM cdms_branch as b group by(b.company_id) having count(*)>3 order by (count(*)) desc")
		context = {"result": [c for c in cursor.fetchall()], "cols":["company", "count"]}
		return render(request, 'cdms/disp_queries.html', context)

#manufacuter
def mfg_queries(request):
	context = {"querylist" : ["mfg_model",], }
	return render(request, 'cdms/querylist.html', context)

def mfg_model(request):
	context = {'mfgs':manufacturer.objects.all()}
	return render(request, 'cdms/mfg_model.html', context)

def mfg_model_disp(request):
	with connection.cursor() as cursor:
		mfg_name = request.POST['mfg_name']
		cursor.execute("SELECT m.name, mm.name, mm.model_id FROM cdms_manufacturer as m, cdms_model as mm WHERE m.name =%s AND mm.mfg_name_id = m.name",[mfg_name])
		context = {"result": [c for c in cursor.fetchall()], "cols":["mfg_name", "model_name", "model_id"]}
		return render(request, 'cdms/disp_queries.html', context)

#branch
def branch_queries(request):
	context = {"querylist" : ["branch_sold", "branch_count_sales"], }
	return render(request, 'cdms/querylist.html', context)

def branch_sold(request):
	context = {'branchs':branch.objects.all()}
	return render(request, 'cdms/branch_sold.html', context)

def branch_sold_disp(request):
	with connection.cursor() as cursor:
		branch_area = request.POST['branch_area']
		cursor.execute("SELECT b.area,s.sale_id from cdms_branch as b,cdms_sold as s where s.branch_id=b.area and b.area=%s",[branch_area])
		context = {"result": [c for c in cursor.fetchall()], "cols":["branch_area", "sale_id"]}
		return render(request, 'cdms/disp_queries.html', context)

def branch_count_sales_disp(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT s.branch_id, count(*) FROM cdms_sold as s group by(s.branch_id) order by (count(*)) desc")
		context = {"result": [c for c in cursor.fetchall()], "cols":["branch", "count"]}
		return render(request, 'cdms/disp_queries.html', context)

#employee
def employee_queries(request):
	context = {"querylist" : ["employee_sold",], }
	return render(request, 'cdms/querylist.html', context)

def employee_sold(request):
	context = {'employees':employee.objects.all()}
	return render(request, 'cdms/employee_sold.html', context)

def employee_sold_disp(request):
	with connection.cursor() as cursor:
		employee_name = request.POST['employee_name']
		cursor.execute("SELECT e.name, b.area, s.sale_id FROM cdms_employee as e, cdms_sold as s, cdms_branch as b where e.branch_id=b.area and b.area=s.branch_id and e.name=%s ",[employee_name])
		context = {"result": [c for c in cursor.fetchall()], "cols":["employee_name","branch_area", "sale_id"]}
		return render(request, 'cdms/disp_queries.html', context)

#model
def model_queries(request):
	context = {"querylist" : ["model_cust",], }
	return render(request, 'cdms/querylist.html', context)

def model_cust(request):
	context = {'models':model.objects.all()}
	return render(request, 'cdms/model_cust.html', context)

def model_cust_disp(request):
	with connection.cursor() as cursor:
		model_name = request.POST['model_name']
		cursor.execute("SELECT m.model_id, m.name, b.customer_id FROM cdms_buys as b, cdms_sold as s, cdms_model as m WHERE m.name =%s AND m.model_id = s.model_id_id AND s.sale_id = b.sale_id_id ORDER BY m.name",[model_name])
		context = {"result": [c for c in cursor.fetchall()], "cols":["model_id", "model_name", "customer"]}
		return render(request, 'cdms/disp_queries.html', context)

#transportation
def trans_queries(request):
	context = {"querylist" : ["trans_branch",], }
	return render(request, 'cdms/querylist.html', context)

def trans_branch(request):
	context = {'transs':transportation.objects.all()}
	return render(request, 'cdms/trans_branch.html', context)

def trans_branch_disp(request):
	with connection.cursor() as cursor:
		customer = request.POST['cust_name']
		cursor.execute("SELECT b.customer_id, m.model_id, m.name FROM cdms_buys as b, cdms_sold as s, cdms_model as m WHERE b.customer_id =%s AND s.sale_id = b.sale_id_id AND s.model_id_id = m.model_id ORDER BY m.name",[customer])
		context = {"result": [c for c in cursor.fetchall()], "cols":["customers", "model_ids", "model_names"]}
		return render(request, 'cdms/disp_queries.html', context)

#sold
def sold_queries(request):
	context = {"querylist" : ["sold_branch",], }
	return render(request, 'cdms/querylist.html', context)

def sold_branch(request):
	context = {'solds':sold.objects.all()}
	return render(request, 'cdms/sold_branch.html', context)

def sold_branch_disp(request):
	with connection.cursor() as cursor:
		customer = request.POST['cust_name']
		cursor.execute("SELECT b.customer_id, m.model_id, m.name FROM cdms_buys as b, cdms_sold as s, cdms_model as m WHERE b.customer_id =%s AND s.sale_id = b.sale_id_id AND s.model_id_id = m.model_id ORDER BY m.name",[customer])
		context = {"result": [c for c in cursor.fetchall()], "cols":["customers", "model_ids", "model_names"]}
		return render(request, 'cdms/disp_queries.html', context)

#registration
def reg_queries(request):
	context = {"querylist" : ["reg_branch",], }
	return render(request, 'cdms/querylist.html', context)

def reg_branch(request):
	context = {'regs':registration.objects.all()}
	return render(request, 'cdms/reg_branch.html', context)

def reg_branch_disp(request):
	with connection.cursor() as cursor:
		customer = request.POST['cust_name']
		cursor.execute("SELECT b.customer_id, m.model_id, m.name FROM cdms_buys as b, cdms_sold as s, cdms_model as m WHERE b.customer_id =%s AND s.sale_id = b.sale_id_id AND s.model_id_id = m.model_id ORDER BY m.name",[customer])
		context = {"result": [c for c in cursor.fetchall()], "cols":["customers", "model_ids", "model_names"]}
		return render(request, 'cdms/disp_queries.html', context)

#ins_company
def insc_queries(request):
	context = {"querylist" : ["insc_insp", "insc_count_insps"], }
	return render(request, 'cdms/querylist.html', context)

def insc_insp(request):
	context = {'inscs':ins_company.objects.all()}
	return render(request, 'cdms/insc_insp.html', context)

def insc_insp_disp(request):
	with connection.cursor() as cursor:
		insc = request.POST['insc_name']
		cursor.execute("SELECT c.name, p.id, p.sale_id_id FROM cdms_ins_company as c, cdms_ins_policy as p WHERE c.name =%s AND p.ins_company_id = c.name ",[insc])
		context = {"result": [c for c in cursor.fetchall()], "cols":["company", "policy_id", "sale_id"]}
		return render(request, 'cdms/disp_queries.html', context)

def insc_count_insps_disp(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT p.ins_company_id, count(*) FROM cdms_ins_policy as p group by(p.ins_company_id) order by (count(*)) desc")
		context = {"result": [c for c in cursor.fetchall()], "cols":["ins_company", "count"]}
		return render(request, 'cdms/disp_queries.html', context)

#ins_policy
def insp_queries(request):
	context = {"querylist" : ["insp_branch",], }
	return render(request, 'cdms/querylist.html', context)

def insp_branch(request):
	context = {'insps':ins_policy.objects.all()}
	return render(request, 'cdms/insp_branch.html', context)

def insp_branch_disp(request):
	with connection.cursor() as cursor:
		customer = request.POST['cust_name']
		cursor.execute("SELECT b.customer_id, m.model_id, m.name FROM cdms_buys as b, cdms_sold as s, cdms_model as m WHERE b.customer_id =%s AND s.sale_id = b.sale_id_id AND s.model_id_id = m.model_id ORDER BY m.name",[customer])
		context = {"result": [c for c in cursor.fetchall()], "cols":["customers", "model_ids", "model_names"]}
		return render(request, 'cdms/disp_queries.html', context)

#buys
def buys_queries(request):
	context = {"querylist" : ["buys_branch",], }
	return render(request, 'cdms/querylist.html', context)

def buys_branch(request):
	context = {'buyss':buys.objects.all()}
	return render(request, 'cdms/buys_branch.html', context)

def buys_branch_disp(request):
	with connection.cursor() as cursor:
		customer = request.POST['cust_name']
		cursor.execute("SELECT b.customer_id, m.model_id, m.name FROM cdms_buys as b, cdms_sold as s, cdms_model as m WHERE b.customer_id =%s AND s.sale_id = b.sale_id_id AND s.model_id_id = m.model_id ORDER BY m.name",[customer])
		context = {"result": [c for c in cursor.fetchall()], "cols":["customers", "model_ids", "model_names"]}
		return render(request, 'cdms/disp_queries.html', context)