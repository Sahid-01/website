from django.contrib import admin
from .models import Branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'country', 'address', 'created_at']
    list_filter = ['country', 'created_at']
    search_fields = ['name', 'code', 'address']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'country', 'address')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        
        if user.is_superadmin():
            # Superadmin sees all branches
            return qs
        elif user.is_main_admin():
            # Main admin sees branches in their country
            return qs.filter(country=user.country)
        elif user.is_branch_admin():
            # Branch admin sees only their branch
            return qs.filter(id=user.branch_id)
        
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user
        
        if db_field.name == "country":
            if user.is_main_admin():
                # Main admin can only assign their country
                kwargs["queryset"] = db_field.related_model.objects.filter(id=user.country_id)
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_add_permission(self, request):
        user = request.user
        # Only superadmin and main admin can add branches
        return user.is_superadmin() or user.is_main_admin()
    
    def has_change_permission(self, request, obj=None):
        user = request.user
        
        if obj is None:
            return True
        
        # Superadmin can edit all branches
        if user.is_superadmin():
            return True
        
        # Main admin can edit branches in their country
        if user.is_main_admin():
            return obj.country == user.country
        
        # Branch admin can view but not edit
        return False
    
    def has_delete_permission(self, request, obj=None):
        user = request.user
        
        if obj is None:
            return True
        
        # Only superadmin can delete branches
        if user.is_superadmin():
            return True
        
        return False
