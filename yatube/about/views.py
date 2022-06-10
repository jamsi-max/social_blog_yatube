import datetime
from django.views.generic.base import TemplateView
from core.views import get_client_ip
from posts.models import Ip


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        ip = get_client_ip(self.request)
        if not Ip.objects.filter(ip=ip).exists():
            Ip.objects.create(ip=ip)

        context["visiterAll"] = Ip.objects.count()
        context["visiterDay"] = Ip.objects.filter(
            created__icontains=datetime.date.today()).count()
        return context


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        ip = get_client_ip(self.request)
        if not Ip.objects.filter(ip=ip).exists():
            Ip.objects.create(ip=ip)

        context["visiterAll"] = Ip.objects.count()
        context["visiterDay"] = Ip.objects.filter(
            created__icontains=datetime.date.today()).count()
        return context
