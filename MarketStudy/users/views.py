from django.contrib.auth.decorators import login_required 
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.db.models import Prefetch
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from carts.models import Cart



class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    
    def get_success_url(self):
        next_url = self.request.POST.get('next')
        if next_url and next_url != reverse('user:logout'):
            return HttpResponseRedirect(next_url)
        return reverse_lazy('main:home')
    
    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            if session_key:
                guest_cart = Cart.objects.filter(session_key=session_key)
                
                if guest_cart.exists():
                    Cart.objects.filter(user=user).delete()
                    guest_cart.update(user=user, session_key=None)
                
                messages.success(self.request, 'Ви увійшли в систему')
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        messages.error(self.request, 'Неправильний логін або пароль')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Логін'
        return context


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('user:profile')
    
    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance
        form.save()
        auth.login(self.request, user)
        if session_key:
            guest_cart = Cart.objects.filter(session_key=session_key)
            if guest_cart.exists():
                Cart.objects.filter(user=user).delete()
                guest_cart.update(user=user, session_key=None)
            
            messages.success(self.request, 'Ви зареєструвались')
        return HttpResponseRedirect(self.success_url)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Помилка в заповненні форми')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Реєстрація'
        return context
    

class UserProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('user:profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance
        if user:
            form.save()
            auth.login(self.request, user)
        if session_key:
            guest_cart = Cart.objects.filter(session_key=session_key)
            if guest_cart.exists():
                Cart.objects.filter(user=user).delete()
                guest_cart.update(user=user, session_key=None)
        
        messages.success(self.request, 'Профіль оновлено')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Помилка в заповненні форми')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профіль'
        context['orders'] = Order.objects.filter(
            user=self.request.user
        ).prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product"),
            )
        ).order_by('-created_timestamp')
        return context


class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'Ви вийшли з системи')
    return redirect(reverse('main:home'))
