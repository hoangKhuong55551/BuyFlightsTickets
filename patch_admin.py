import re
with open('flights/admin.py', 'r', encoding='utf-8') as f:
    content = f.read()

override_code = '''
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'profile') and request.user.profile.managed_airline:
            return qs.filter(airline=request.user.profile.managed_airline)
        return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'profile') and request.user.profile.managed_airline:
            if db_field.name == "airline":
                kwargs["queryset"] = Airline.objects.filter(id=request.user.profile.managed_airline.id)
                kwargs["initial"] = request.user.profile.managed_airline.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and hasattr(request.user, 'profile') and request.user.profile.managed_airline:
            obj.airline = request.user.profile.managed_airline
        super().save_model(request, obj, form, change)
'''

content = content.replace('    list_filter = ["airline", "status", "departure_time"]', '    list_filter = ["airline", "status", "departure_time"]' + override_code)
with open('flights/admin.py', 'w', encoding='utf-8') as f:
    f.write(content)
