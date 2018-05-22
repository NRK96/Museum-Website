from django.contrib import admin
from scheduling.models import CustomerProfile, Reservation
import datetime
import calendar
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
from django.urls import reverse
from scheduling.utils import ReservationCalendar
from scheduling.models import CustomerProfile, Reservation, Request, Docent

#rename header for the admin page
admin.site.site_header = 'Museum of South Texas History Administration'


class ReservationInline(admin.TabularInline):
	model = Reservation
	extra = 0


class CustomerProfileAdmin(admin.ModelAdmin):
        #fieldsets seperate fields into subcategories
	fieldsets = [
		('Customer Profile', {'fields': ['name']}),
		('Email',            {'fields': ['email']})
	]
	inlines = [ReservationInline]
	#list displays choose which fields of the model to show on the list view
	list_display = ('name', 'email')
	#search fields determine what fields we can search by in the list view
	search_fields = ['name']


class DocentAdmin(admin.ModelAdmin):
	fieldsets = [
		('Docent', {'fields': ['name']}),
		('Email',  {'fields': ['email']})
	]
	inlines = [ReservationInline]
	list_display = ('name', 'email')
	search_fields = ['name']
    
    
class RequestAdmin(admin.ModelAdmin):
    fieldsets = [
            ('Customer Info', {'fields': ['name', 'email']}),
            ('Reservation Info', {'fields': ['group_size', 'reserved_date', 'start_time', 'end_time']}),
            ('Other', {'fields': ['info_text']})
    ]
    list_display = ('name', 'reserved_date', 'group_size')
    #list filters determine which fields we can filter the list view by
    list_filter = ['name', 'start_time', 'reserved_date']
    search_fields = ['name', 'reserved_date', 'start_time', 'group_size']

class ReservationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Customer Info', {'fields': ['customer']}),

        ('Reservation Info', {'fields': ['group_size', 'actual_group_size', 'date', 'start_time', 'end_time', 'docent']}),

        ('Other', {'fields': ['info_text']})
    ]
    list_display = ['date', 'customer', 'start_time', 'end_time', 'info_text', 'docent']
    list_filter = ['customer', 'start_time', 'date']
    search_fields = ['customer__name', 'date', 'start_time', 'group_size']


admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Docent, DocentAdmin)

