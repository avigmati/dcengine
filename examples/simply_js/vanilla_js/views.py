from django.views.generic.base import TemplateView
# from django.conf import settings
from dcengine import settings


class IndexView(TemplateView):

    template_name = 'vanilla_js/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['socket_url_path'] = settings.DCENGINE_SOCKET_URL_PATH
        return context
