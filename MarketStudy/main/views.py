from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Головна сторінка'
        context['content'] = 'Пивоварня "HOLY"'
        return context

class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Про пивоварню'
        context['content'] = 'Ми Пивоварня "HOLY"'
        context['text_on_page'] = 'Ось чому ми такі класні і афігенні!'
        return context
