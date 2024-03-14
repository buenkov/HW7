from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
#Импортируем модуль авторизации
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import PostForm
from .models import Post, count_posts, Author
from .filters import PostFilter
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-create_date'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10# указываем количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в 7 юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

# отдельное вью для новостей
class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-create_date'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10# указываем количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в 7 юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs.filter(art_new='N')


    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        # Проверяем является ли пользоватесль подписчиком
        context['is_not_subscriber'] = not self.request.user.groups.filter(name='sub_N').exists()
        return context

# отдельное вью для статей
class ArticlesList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-create_date'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10# указываем количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в 7 юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs.filter(art_new='A')


    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        # Проверяем является ли пользоватесль подписчиком
        context['is_not_subscriber'] = not self.request.user.groups.filter(name='sub_A').exists()
        return context


# Create your views here.
class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'article.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect('/news/')
    return render(request, 'post_edit.html', {'form':form})

class PostCreate(PermissionRequiredMixin, CreateView):
    # Добавляю проверку прав создание поста
    permission_required = ('nportal.add_post',)
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

    def form_valid(self, form):
        # Добавляем, проверку, того, что пользователь не создал более 3 постов за сегодня
        today = timezone.now().date()
        author_instance = Author.objects.get(user=self.request.user)
        posts_count_today = Post.objects.filter(author=author_instance, create_date__date=today).count()
        if posts_count_today >= 100:
            # Если у пользователя 3 поста или более возвращаем ошибку, прерываем выполнение
            return render(self.request, 'post_edit.html',
                          {'form': form, 'error_message': 'Вы уже создали 3 публикации за день.'})
        # Иначе продолжаем выполнение
        post = form.save(commit=False)
        url_referer = self.request.META['HTTP_REFERER']
        if 'news' in url_referer:
            post.art_new = 'N'
        elif 'articles' in url_referer:
            post.art_new = 'A'
        else:
            # Если некорректно, пропускаем
            pass
        # если все ок, отправляем письмо
        # if post.art_new == 'N':
        #
        #     subscribe_group = Group.objects.get(name='sub_N')
        #     users = subscribe_group.user_set.all()
        #
        #     for user in users:
        #         email = tuple(user.email.split('  '))
        #         username = user.username
        #         msg = EmailMultiAlternatives(
        #                 subject=f'Здравствуй, {username}, Создана новая новость с темой: {post.title}',
        #                 body=f'Здравствуй, {username}, Новая статья в твоём любимом разделе!  {post.text}',  # это то же, что и message
        #                 from_email='buenkov-ta@yandex.ru',
        #                 to=email,  # это то же, что и recipients_list
        #             )
        #
        #         html_content = render_to_string(
        #             'post_created.html',
        #             {
        #                 'username': username,
        #                 'post': post,
        #             }
        #         )
        #         msg.attach_alternative(html_content, "text/html")  # добавляем html
        #         msg.send()  # отсылаем
        # if post.art_new == 'A':
        #
        #     subscribe_group = Group.objects.get(name='sub_A')
        #     users = subscribe_group.user_set.all()
        #
        #     for user in users:
        #         email = tuple(user.email.split('  '))
        #         username = user.username
        #         msg = EmailMultiAlternatives(
        #             subject=f'Создана новая статья с темой: {post.title}',
        #             body=f'Здравствуй, {username}, Новая статья в твоём любимом разделе!  {post.text}',
        #             # это то же, что и message
        #             from_email='buenkov-ta@yandex.ru',
        #             to=email,  # это то же, что и recipients_list
        #         )
        #
        #         html_content = render_to_string(
        #             'post_created.html',
        #             {
        #                 'username': username,
        #                 'post': post,
        #             }
        #         )
        #         msg.attach_alternative(html_content, "text/html")  # добавляем html
        #         msg.send()  # отсылаем

            # if post.art_new == 'N' or post.art_new == 'A':
        #     # получаем наш html
        #     html_content = render_to_string(
        #         'post_created.html',
        #         {
        #             'post': post,
        #         }
        #     )
        #     #отправляем
        #     msg = EmailMultiAlternatives(
        #         subject=f'Создана новая публикация с типом: {post.art_new} с темой: {post.title}',
        #         body=post.text,  # это то же, что и message
        #         from_email='buenkov-ta@yandex.ru',
        #         to=['buenkovt@gmail.com'],  # это то же, что и recipients_list
        #     )
        #     msg.attach_alternative(html_content, "text/html")  # добавляем html
        #     msg.send()  # отсылаем


# Это если бы мы отправляли по старому не html
            # send_mail(
            #     # тема письма:
            #     subject=f'Создана новая публикация с типом: {post.art_new} с темой: {post.title}',
            #     message=post.text,  # сообщение с кратким описанием проблемы
            #     from_email='buenkov-ta@yandex.ru',
            #     # здесь указываете почту, с которой будете отправлять
            #     recipient_list=['buenkovt@gmail.com']  # здесь список получателей. Например, секретарь, сам врач и т. д.
            # )

        return super().form_valid(form)




# Добавляем представление для изменения товара.
class PostUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('nportal.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    login_url = 'post_list'
    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save(commit=False)
        if type == 'news':
            post.art_new = 'N'
        elif type == 'articles':
            post.art_new = 'A'
        else:
            # Если некорректно, пропускаем
            pass
        return super().form_valid(form)


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

@login_required
def subscribe_news(request):
    user = request.user
    subscribe_group = Group.objects.get(name='sub_N')
    if not request.user.groups.filter(name='sub_N').exists():
        subscribe_group.user_set.add(user)
    return redirect('/')
def subscribe_arts(request):
    user = request.user
    subscribe_group = Group.objects.get(name='sub_A')
    if not request.user.groups.filter(name='sub_A').exists():
        subscribe_group.user_set.add(user)
    return redirect('/')