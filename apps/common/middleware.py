import requests
from apps.country.models import Country
from apps.branch.models import Branch


class GeoCityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        
        # Skip if already redirected
        if request.COOKIES.get('geo_redirected'):
            return self.get_response(request)
        
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
        
        try:
            res = requests.get(f'https://https://ip-api.com/json/', timeout=1).json()
            country_code = res.get('country')
            city_name = res.get('city', '').lower()
            
            country = Country.objects.filter(code=country_code).first()
            branch = Branch.objects.filter(country=country, city__iexact=city_name).first() if country else None
            
            request.country = country
            request.branch = branch
            
            response = self.get_response(request)
            response.set_cookie('geo_redirected', '1', max_age=30*24*3600)
            return response
        except Exception as e:
            request.country = None
            request.branch = None
            return self.get_response(request)
