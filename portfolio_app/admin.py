from django.contrib import admin
from .models import Education, Certification, Portfolio, Contact, About, Employment

admin.site.register(About)
admin.site.register(Employment)
admin.site.register(Education)
admin.site.register(Certification)
admin.site.register(Portfolio)
admin.site.register(Contact)
