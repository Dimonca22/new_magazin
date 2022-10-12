from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категории"""
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, verbose_name='Url', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})


class Product(models.Model):
    """Белье"""
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, verbose_name='Url', db_index=True)
    image = models.ImageField(upload_to='images/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='цена')
    content = models.TextField(blank=True)
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    available = models.BooleanField(default=True, verbose_name='В наличии')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Белье'
        verbose_name_plural = 'Белье'
        index_together = (('id', 'slug'),)

    def get_absolute_url(self):
        return reverse('post', kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class ShopShots(models.Model):
    """Дополнительные фото"""
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="images_shots/")
    product = models.ForeignKey(Product, verbose_name="Комплект", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фото комплекта"
        verbose_name_plural = "Фото комплектов"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    kit = models.ForeignKey(Product, verbose_name="Комплект", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.kit}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
