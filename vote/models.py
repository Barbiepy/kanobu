from django.contrib.auth.models import User
from django.db import models


class Material(models.Model):

    NEWS = "news"
    ARTICLE = "article"

    TYPE_CHOICES = (
        (NEWS, "Новость"),
        (ARTICLE, "Статья")
    )

    type = models.CharField("Тип материала", choices=TYPE_CHOICES, max_length=7)
    title = models.CharField("Заголовок", max_length=100)
    text = models.TextField("Текст")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    published_at = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(User, verbose_name="Автор", related_name="materials", on_delete=models.CASCADE)
    votes = models.ManyToManyField("Vote", verbose_name="Оценки", related_name="materials", blank=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.title}"


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=Material.ARTICLE)


class Article(Material):
    objects = ArticleManager()

    class Meta:
        proxy = True
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


class NewsManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(type=Material.NEWS)


class News(Material):
    objects = NewsManager()

    class Meta:
        proxy = True
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class Comment(models.Model):
    text = models.TextField("Текст")
    material = models.ForeignKey(Material, verbose_name="Материал", related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='Автор', related_name='comments', on_delete=models.CASCADE)
    votes = models.ManyToManyField("Vote", verbose_name="Оценки", related_name="comments", blank=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"{self.material} - {self.text}"


class Vote(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"

    STATUS_CHOICES = (
        (LIKE, "Понравилось"),
        (DISLIKE, "Не понравилось")
    )
    status = models.CharField("Статус", choices=STATUS_CHOICES, max_length=7)
    author = models.ForeignKey(User, verbose_name="Автор", related_name="votes", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"

    def __str__(self):
        return f"{self.author} - {self.get_status_display()}"
