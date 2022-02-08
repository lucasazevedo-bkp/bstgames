import threading

from django.http.response import HttpResponseRedirect
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.db.models import F
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required

from .models import Game, GamePlatform, GameGamePlatform, GameMarket
from .forms import (SignUpForm, LogInForm, SendVerifyEmailForm, 
    PasswordChangeForm, EditProfileForm, EditProfileAddressForm)
from .tokens import email_verification_token
from .viacep import get_address
from users.models import UserAddress

User = get_user_model()


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()
        

class HomeView(TemplateView):
    template_name = 'bstgames/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platforms'] = GamePlatform.objects.all()
        context['nbar'] = 'home'
        return context


class SignUpView(SuccessMessageMixin, CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'bstgames/signup.html'
    success_url = reverse_lazy('bstgames:login')
    success_message = "You have successfully signed up! Verify your email so you can log in."

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('bstgames:home'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nbar'] = 'signup'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        send_verification_email(self.object, self.request)
        return response


def send_verification_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Verify your email'
    email_body = render_to_string('bstgames/verify_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': email_verification_token.make_token(user)})
    email = EmailMessage(
        subject=email_subject, 
        body=email_body, 
        from_email=settings.EMAIL_FROM_USER, 
        to=[user.email])
    EmailThread(email).start()


class LogInView(SuccessMessageMixin, views.LoginView):
    template_name = 'bstgames/login.html'
    authentication_form = LogInForm
    success_message = "You have successfully logged in!"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('bstgames:home'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nbar'] = 'login'
        return context

    def form_valid(self, form):
        user = form.get_user()

        if not user.is_email_verified:
            messages.warning(self.request, 'Your email is not verified, verify your email so you can log in.')
            href = reverse_lazy('bstgames:send-verify-email')
            messages.info(self.request, f"If you have not received the email or the verification link is invalid, click <a href='{href}'>here</a> to get a new one.")
            return HttpResponseRedirect(reverse_lazy('bstgames:login'))
            
        return super().form_valid(form)


class LogOutView(LoginRequiredMixin, views.LogoutView):
    next_page = 'bstgames:home'


class VerifyEmailView(View):
    
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as e:
            user = None

        if user and email_verification_token.check_token(user, token):
            if not request.user.is_authenticated:
                user.is_email_verified = True
                user.save()
                messages.success(request, 'Your email have been verified, you can now login.')
                return HttpResponseRedirect(reverse_lazy('bstgames:login'))

        if user:
            if user.is_email_verified:
                if request.user.is_authenticated:
                    if user == request.user:
                        messages.success(request, 'Your email is already verified.')
                        return HttpResponseRedirect(reverse_lazy('bstgames:home'))
                    messages.warning(request, 'Invalid verification link.')
                    return HttpResponseRedirect(reverse_lazy('bstgames:home'))
                messages.success(request, 'Your email is already verified, you can now login.')
                return HttpResponseRedirect(reverse_lazy('bstgames:login'))
        messages.warning(request, 'Invalid verification link.')
        return HttpResponseRedirect(reverse_lazy('bstgames:home'))


class SendVerifyEmailView(FormView):
    template_name = 'bstgames/send_verify_email.html'
    form_class = SendVerifyEmailForm
    success_url = reverse_lazy('bstgames:login')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('bstgames:home'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()

        if user.is_email_verified:
            messages.success(self.request, 'Your email is already verified, you can now login.')
        else:
            send_verification_email(user, self.request)
            messages.success(self.request, 'Verify your email so you can log in.')

        return super().form_valid(form)


class PasswordChangeView(SuccessMessageMixin, views.PasswordChangeView):
    template_name = 'bstgames/change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('bstgames:change-password')
    success_message = 'You have successfully changed your password!'


class PasswordResetView(SuccessMessageMixin, views.PasswordResetView):
    template_name = 'bstgames/reset_password.html'
    email_template_name = 'bstgames/reset_password_email.html'
    subject_template_name = 'bstgames/reset_password_subject.txt'
    from_email = settings.EMAIL_FROM_USER
    success_url = reverse_lazy('bstgames:login')
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('bstgames:home'))
        return super().get(request, *args, **kwargs)


class PasswordResetConfirmView(SuccessMessageMixin, views.PasswordResetConfirmView):
    template_name = 'bstgames/reset_password_confirm.html'
    success_url = reverse_lazy('bstgames:login')
    success_message = 'You have successfully reset your password! You can now login.'


class PlatformGameListView(ListView):
    context_object_name = 'game_list'
    template_name = 'bstgames/list_games.html'
    paginate_by = 6

    def get_queryset(self):
        self.platform = get_object_or_404(GamePlatform, pk=self.kwargs['pk'])
        games = GameGamePlatform.objects.filter(
            gameplatform=self.platform
        ).order_by(F('release_date').desc(nulls_last=True), '-game_id')
        return games

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nbar'] = self.platform.platform
        context['platforms'] = GamePlatform.objects.all()
        context['title'] = self.platform.platform
        return context


class GameDetailView(DetailView):
    model = GameGamePlatform
    template_name = 'bstgames/detail_game.html'
    context_object_name = 'game_platform'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.game} - {self.object.gameplatform}'
        context['platforms'] = GamePlatform.objects.all()
        context['actions'] = {
            GameMarket.ActionChoices.BUY.name: {
                'label': GameMarket.ActionChoices.BUY.label, 'value': GameMarket.ActionChoices.BUY 
            },
            GameMarket.ActionChoices.SELL.name: {
                'label': GameMarket.ActionChoices.SELL.label, 'value': GameMarket.ActionChoices.SELL 
            },
            GameMarket.ActionChoices.TRADE.name: {
                'label': GameMarket.ActionChoices.TRADE.label, 'value': GameMarket.ActionChoices.TRADE 
            }
        }
        return context


class GameSearchListView(ListView):
    context_object_name = 'game_list'
    template_name = 'bstgames/list_games.html'
    paginate_by = 6

    def get_queryset(self):
        self.query = self.request.GET.get('q', '')
        games = GameGamePlatform.objects.filter(
            game__in=Game.objects.filter(game__icontains=self.query)
        ).order_by(F('release_date').desc(nulls_last=True), '-game_id')
        return games

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platforms'] = GamePlatform.objects.all()
        context['title'] = 'Search game'
        return context


class GameMarketView(LoginRequiredMixin, TemplateView):
    template_name = 'bstgames/game_market.html'

    def get_context_data(self, **kwargs):
        game_platform = get_object_or_404(GameGamePlatform, pk=kwargs.get('pk'))
        try:
            action = GameMarket.ActionChoices(kwargs.get('action'))
        except ValueError:
            raise Http404
        if action.value == GameMarket.ActionChoices.BUY:
            action_filter = GameMarket.ActionChoices.SELL
        elif action.value == GameMarket.ActionChoices.SELL:
            action_filter = GameMarket.ActionChoices.BUY
        else:
            action_filter = action.value
        markets = markets = GameMarket.objects.filter(
            gameplatform=game_platform, 
            status=GameMarket.StatusChoices.ACTIVE, 
            action=action_filter
        )
        context = super().get_context_data(**kwargs)
        context['game_platform'] = game_platform
        context['platforms'] = GamePlatform.objects.all()
        context['title'] = f'{action.label} - {game_platform.game} - {game_platform.gameplatform}'
        context['action'] = {'label': action.label, 'value': action.value}
        context['markets'] = markets
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            href_signup = reverse_lazy('bstgames:signup')
            msg = f"You have to be logged in to trade a game. <a href='{href_signup}'>Sign up</a> if you don't have an account."
            messages.warning(request, msg)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


def handler404(request, exception):
    platforms = GamePlatform.objects.all()
    context = {
        'title': 'Page not found',
        'platforms': platforms,
        'exception': exception
    }
    return render(request, 'bstgames/404.html', context, status=404)


class EditProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'bstgames/edit_profile.html'
    success_url = reverse_lazy('bstgames:edit-profile')
    success_message = "You have successfully edited your profile!"

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            address = UserAddress.objects.get(user=self.object)
        except:
            address = None

        address_formset = EditProfileAddressForm(instance=address)

        return self.render_to_response(self.get_context_data(
            form=EditProfileForm(instance=self.object), address_formset=address_formset))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = EditProfileForm(request.POST, instance=self.object)

        try:
            address = UserAddress.objects.get(user=self.object)
        except:
            address = None

        address_formset = EditProfileAddressForm(request.POST, instance=address)

        if form.is_valid() and address_formset.is_valid():
            return self.form_valid(form, address_formset)
        else:
            return self.form_invalid(form, address_formset)

    def form_valid(self, form, address_formset):
        response = super().form_valid(form)
        
        if ((not address_formset.instance.pk and address_formset.has_changed()) 
            or (address_formset.instance.pk 
            and (address_formset.instance.postal_code
            or address_formset.instance.state 
            or address_formset.instance.locality))):
            address = address_formset.save(commit=False)
            address.user = self.object
            address.save()
        elif address_formset.instance.pk:
            address_formset.instance.delete()

        return response

    def form_invalid(self, form, address_formset):
        return self.render_to_response(self.get_context_data(form=form, address_formset=address_formset))


@login_required
def viacep_ajax(request):
    if request.is_ajax and request.method == 'GET':
        postal_code = request.GET.get('postal_code', None)
        address = get_address(postal_code)
        if address:
            return JsonResponse(address)
    return JsonResponse({}, status=400)


@login_required
def market_table_ajax(request):
    if request.is_ajax and request.method == 'GET':
        platform = request.GET.get('platform', None)
        game = request.GET.get('game', None)
        action = request.GET.get('action', None)
        if platform and game and action:
            try:
                if int(action) == GameMarket.ActionChoices.BUY:
                    action = GameMarket.ActionChoices.SELL
                elif int(action) == GameMarket.ActionChoices.SELL:
                    action = GameMarket.ActionChoices.BUY
                markets = markets = GameMarket.objects.filter(
                    gameplatform__game=game,
                    gameplatform__gameplatform=platform, 
                    status=GameMarket.StatusChoices.ACTIVE, 
                    action=action
                )
            except:
                markets = None
            if markets:
                response = {}
                for market in markets:
                    try:
                        user_state = market.user.useraddress.state
                        user_locality = market.user.useraddress.locality
                    except:
                        user_state = user_locality = None
                    user_name = f'{market.user.first_name} ({market.user.email})' if market.user.first_name else market.user.email
                    trade = None
                    if market.trade.all():
                        trade = {}
                        for trade_query in market.trade.all():
                            trade[trade_query.pk] = trade_query.__str__()
                    response[market.pk] = {
                        'user': user_name,
                        'state': user_state,
                        'locality': user_locality,
                        'price': market.price,
                        'trade': trade
                    }
                return JsonResponse(response)
    return JsonResponse({}, status=400)