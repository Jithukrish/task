from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import ThreadForm
from chat.models import Thread
from django.views.generic.edit import FormView

def  messages(request):
    threads = Thread.objects.by_user(user = request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    return render(request, 'message/message.html',context)


class CreateThreadView(FormView):
    template_name = 'message/message.html'
    form_class = ThreadForm
    success_url = reverse_lazy('messages')  

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
