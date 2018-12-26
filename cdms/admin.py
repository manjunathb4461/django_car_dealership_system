from django.contrib import admin

# Register your models here.

from cdms.models import customer, company, manufacturer, branch, employee, model, transportation, sold, registration, ins_company, ins_policy, buys

admin.site.register(customer)
admin.site.register(manufacturer)
admin.site.register(company)
admin.site.register(branch)
admin.site.register(employee)
admin.site.register(model)
admin.site.register(transportation)
admin.site.register(sold)
admin.site.register(registration)
admin.site.register(ins_company)
admin.site.register(ins_policy)
admin.site.register(buys)