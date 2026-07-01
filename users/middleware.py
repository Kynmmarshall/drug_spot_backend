from django.utils import timezone


class UpdateLastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            type(request.user).objects.filter(pk=request.user.pk).update(
                last_seen=timezone.now()
            )
        return response
