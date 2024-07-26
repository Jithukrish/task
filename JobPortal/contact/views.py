from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from .forms import ContactForm
from django.contrib import messages

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('login_user')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your message has been sent successfully!')
        return super().form_valid(form)
   
# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save() 
#             return redirect('contact') 
#     else:
#         form = ContactForm()
#     return render(request, 'contact.html', {'form': form})
