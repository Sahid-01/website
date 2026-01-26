from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Users


@admin.register(Users)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'country', 'branch', 'is_active']
    list_filter = ['role', 'country', 'branch', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'country', 'branch', 'phone')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'country', 'branch', 'phone')}),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        
        if user.is_superadmin():
            # Superadmin sees all users
            return qs
        elif user.is_main_admin():
            # Main admin sees users in their country (excluding superadmins)
            return qs.filter(country=user.country).exclude(role='superadmin')
        elif user.is_branch_admin():
            # Branch admin sees only users in their branch
            return qs.filter(branch=user.branch)
        
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user
        
        if db_field.name == "country":
            if user.is_main_admin():
                # Main admin can only assign their country
                kwargs["queryset"] = db_field.related_model.objects.filter(id=user.country_id)
            elif user.is_branch_admin():
                # Branch admin can only see their country
                kwargs["queryset"] = db_field.related_model.objects.filter(id=user.country_id)
        
        if db_field.name == "branch":
            if user.is_main_admin():
                # Main admin can assign branches in their country
                kwargs["queryset"] = db_field.related_model.objects.filter(country=user.country)
            elif user.is_branch_admin():
                # Branch admin can only assign their branch
                kwargs["queryset"] = db_field.related_model.objects.filter(id=user.branch_id)
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        user = request.user
        
        if db_field.name == "role":
            if user.is_main_admin():
                # Main admin can create main_admin, branch_admin, and staff
                kwargs['choices'] = [
                    ('main_admin', 'Main Admin'),
                    ('branch_admin', 'Branch Admin'),
                    ('staff', 'Staff'),
                ]
            elif user.is_branch_admin():
                # Branch admin can only create staff
                kwargs['choices'] = [
                    ('staff', 'Staff'),
                ]
        
        return super().formfield_for_choice_field(db_field, request, **kwargs)
    
    def has_delete_permission(self, request, obj=None):
        user = request.user
        
        if obj is None:
            return True
        
        # Superadmin can delete anyone except themselves
        if user.is_superadmin():
            return obj != user
        
        # Main admin can delete users in their country (except superadmins)
        if user.is_main_admin():
            return obj.country == user.country and not obj.is_superadmin()
        
        # Branch admin can delete users in their branch
        if user.is_branch_admin():
            return obj.branch == user.branch and obj.is_staff_user()
        
        return False
