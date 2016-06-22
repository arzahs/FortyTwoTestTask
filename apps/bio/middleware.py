from django.core.urlresolvers import reverse
from apps.bio.models import Request


class SaveRequestMiddleware():

    def process_response(self, request, response):
        if request.path != reverse('requests_list') and not request.is_ajax():
            Request.objects.create(
                path=request.path,
                method=request.method,
                server_protocol=request.META['SERVER_PROTOCOL'],
                status_code=response.status_code,
                content_len=len(response.content)
            )

        return response
