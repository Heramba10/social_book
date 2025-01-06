class CustomAdminSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin'):
            request.session.cookie_name = 'admin_session'  # Set custom session for admin
        else:
            request.session.cookie_name = 'frontend_session'  # Set normal session for frontend

        response = self.get_response(request)
        return response  