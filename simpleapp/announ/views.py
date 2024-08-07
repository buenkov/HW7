from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import AnnouncmentForm, ResponseForm, NewsForm
from django import forms
from django.utils import timezone

class AnnouncementList(ListView):
    model = Announcement
    ordering = '-create_date'
    template_name = 'announs.html'
    context_object_name = 'announcements'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            player = Player.objects.get(user=self.request.user)
            responses = Response.objects.filter(player_id=player).values_list('announcement_id', flat=True)
            context['user_responses'] = set(responses)
        return context

# class AnnouncementList(ListView):
#     # Указываем модель, объекты которой мы будем выводить
#     model = Announcement
#     # Поле, которое будет использоваться для сортировки объектов
#     ordering = '-create_date'
#     # Указываем имя шаблона, в котором будут все инструкции о том,
#     # как именно пользователю должны быть показаны наши объекты
#     template_name = 'announs.html'
#     # Это имя списка, в котором будут лежать все объекты.
#     # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
#     context_object_name = 'announcements'
#     paginate_by = 10# указываем количество записей на странице

class AnnouncementDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Announcement
    # Используем другой шаблон — product.html
    template_name = 'article.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'announcements'


@login_required
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncmentForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = Player.objects.get(user=request.user)
            announcement.save()
            return redirect('announcement_list')
    else:
        form = AnnouncmentForm()
    return render(request, 'create_announcement.html', {'form': form})


@login_required
def add_response(request, announcement_id):
    # Получаем объявление, если его нет - возвращаем 404
    announcement = get_object_or_404(Announcement, id=announcement_id)

    # Получаем игрока, если его нет - возвращаем 404
    player, created = Player.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.player_id = player
            response.announcement_id = announcement
            response.save()
            return redirect('announcement_list')
    else:
        form = ResponseForm()

    return render(request, 'add_response.html', {'form': form, 'announcement': announcement})

class ResponseFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('all', 'Все'),
        ('pending', 'Ожидает'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, initial='all', label='Статус')
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}), label='Начальная дата')
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}), label='Конечная дата')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            announcements = Announcement.objects.filter(author__user=user)
            ANNOUNCEMENT_CHOICES = [('all', 'Все')] + [(announcement.id, announcement.title) for announcement in
                                                       announcements]
            self.fields['announcement'] = forms.ChoiceField(choices=ANNOUNCEMENT_CHOICES, required=False, initial='all',
                                                            label='Объявление')

@login_required
def view_responses(request):
    player = get_object_or_404(Player, user=request.user)
    announcements = Announcement.objects.filter(author=player)
    responses = Response.objects.filter(announcement_id__in=announcements)

    if request.method == 'POST':
        if 'response_id' in request.POST and 'action' in request.POST:
            response_id = request.POST.get('response_id')
            action = request.POST.get('action')
            response = get_object_or_404(Response, id=response_id)
            if action == 'accept':
                response.status = 'accepted'
            elif action == 'reject':
                response.status = 'rejected'
            response.save()
            return redirect('view_responses')
        else:
            filter_form = ResponseFilterForm(request.POST, user=request.user)
            if filter_form.is_valid():
                status = filter_form.cleaned_data.get('status')
                start_date = filter_form.cleaned_data.get('start_date')
                end_date = filter_form.cleaned_data.get('end_date')
                announcement_id = filter_form.cleaned_data.get('announcement')

                if status and status != 'all':
                    responses = responses.filter(status=status)
                if start_date:
                    responses = responses.filter(create_date__gte=start_date)
                if end_date:
                    responses = responses.filter(create_date__lte=end_date)
                if announcement_id and announcement_id != 'all':
                    responses = responses.filter(announcement_id=announcement_id)
    else:
        filter_form = ResponseFilterForm(user=request.user)

    return render(request, 'view_responses.html', {'responses': responses, 'filter_form': filter_form})

# @login_required
# def view_responses(request):
#     player = get_object_or_404(Player, user=request.user)
#     announcements = Announcement.objects.filter(author=player)
#     responses = Response.objects.filter(announcement_id__in=announcements)
#
#     if request.method == 'POST':
#         response_id = request.POST.get('response_id')
#         action = request.POST.get('action')
#         response = get_object_or_404(Response, id=response_id)
#
#         if action == 'accept':
#             response.status = 'accepted'
#         elif action == 'reject':
#             response.status = 'rejected'
#         response.save()
#
#         return redirect('view_responses')

 #   return render(request, 'view_responses.html', {'responses': responses})

@login_required
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save()
            players = Player.objects.all()
            recipient_list = [player.user.email for player in players if player.user.email]

            # Используем render_to_string для создания HTML-сообщения
            html_message = render_to_string('news_email.html', {'news': news})

            send_mail(
                subject=news.title,
                message='',
                from_email='buenkov-ta@yandex.ru',
                recipient_list=recipient_list,
                fail_silently=False,
                html_message=html_message
            )
            return redirect('announcement_list')
    else:
        form = NewsForm()
    return render(request, 'create_news.html', {'form': form})