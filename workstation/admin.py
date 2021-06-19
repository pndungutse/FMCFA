from django.contrib import admin
from workstation.models.hospital import Hospital, Pass, Ordonance, Exam, Medical_Exam, Drug, DrugsIssuing
from workstation.models.pharmacy import Pharmacy

# Register your models here.
admin.site.register(Hospital)
admin.site.register(Pharmacy)
admin.site.register(Pass)
admin.site.register(Ordonance)
admin.site.register(Exam)
admin.site.register(Medical_Exam)
admin.site.register(Drug)
admin.site.register(DrugsIssuing)


