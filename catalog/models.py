from django.db import models


class SortOrder(models.TextChoices):

    ASC = 'ASC'
    DESC = 'DESC'


class Goods(models.Model):

    name = models.CharField(max_length=80, verbose_name='Товар')
    info = models.TextField(verbose_name='Описание')
    base_cost = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Базовая цена')
    sort_order = models.CharField(max_length=4, choices=SortOrder.choices, default=SortOrder.ASC)

    class Meta:
        app_label = 'catalog'
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'

    def __str__(self):
        return f'Название товара: {self.name}'


class Images(models.Model):

    good = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='images')
    file = models.FileField()
    sign = models.CharField(max_length=55, verbose_name='Подпись')
    sort_order = models.CharField(max_length=4, choices=SortOrder.choices, default=SortOrder.ASC)

    class Meta:
        app_label = 'catalog'
        verbose_name_plural = 'Изображения'
        verbose_name = 'Изображение'

    def __str__(self):
        return f'Изображение товара {self.good.name}'


class Parameters(models.Model):

    good = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='parameters')
    name = models.CharField(max_length=80, verbose_name='Имя параметра', blank=True)
    value = models.CharField(max_length=80, verbose_name='Значение параметра', blank=True)
    cost = models.DecimalField(max_digits=14, decimal_places=2,
                               verbose_name='Цена', blank=True, null=True)
    sort_order = models.CharField(max_length=4, choices=SortOrder.choices, default=SortOrder.ASC)

    class Meta:
        app_label = 'catalog'
        verbose_name_plural = 'Параметры'
        verbose_name = 'Параметр'

    def __str__(self):
        return f'Параметр товара {self.good.name}'
