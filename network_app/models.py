from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    """Модель юзера"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    image = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, verbose_name='Изображение')
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=20, blank=True, verbose_name='Город')
    bio = models.TextField(max_length=150, blank=True, verbose_name='О себе')
    friends = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return f'{self.user.username}'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'id': self.pk})

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']


class Post(models.Model):
    title = models.CharField(max_length=25, verbose_name="Заголовок")
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poster')
    text = models.TextField(max_length=120, verbose_name='Текст')
    image = models.ImageField(upload_to='posts/%Y/%m/%d') #blank
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL") #uniqe

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        ordering = ['-date']


class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария', related_name='author')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=140, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return f'Комментарий от {self.author} к {self.post}'


class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
