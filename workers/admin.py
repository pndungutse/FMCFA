from django.contrib import admin
from workers.models.hosAgent import HospitalAgent
from workers.models.pharmacist import Pharmacist

# Register your models here.
admin.site.register(HospitalAgent)
admin.site.register(Pharmacist)
