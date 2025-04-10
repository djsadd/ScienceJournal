from django.shortcuts import render
from django.views import View
# Create your views here.


class JournalView(View):
    template_name = 'journal/main.html'

    def get(self, request):
        return render(request, self.template_name, {
            'user': request.user
        })

