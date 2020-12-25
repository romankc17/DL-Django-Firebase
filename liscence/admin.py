from django.contrib import admin
from .models import Client, Cookies
from django.contrib.auth.models import User,Group
# admin.site.unregister([User,Group])

class ClientAdmin(admin.ModelAdmin):

    #fields = ('user', 'staff','firstname','middlename','lastname', 'submitted', 'payload',)
    list_display = ('firstname','lastname','is_submitted','user','staff','id',)
    list_filter = ('client_added_at','user','staff', 'submitted',)

admin.site.register(Client, ClientAdmin )
admin.site.register(Cookies )

class ClientInline(admin.TabularInline):
    model = Client
    fk_name = 'staff'
    fields = ('submitted','user', 'staff', 'firstname', 'middlename', 'lastname',  'payload',)

    extra = 0

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username']}),
        ('Password', {'fields':['password',], 'classes': ['collapse']})
    ]
    list_display=('username','id','is_staff','date_joined',)
    list_filter=('is_staff',)
    ordering = ('date_joined',)
    inlines = [ClientInline]


# admin.site.register(User, UserAdmin)
