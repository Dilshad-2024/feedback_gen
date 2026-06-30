from django.db import models
from django.contrib.auth.models import User


class Form(models.Model):

    title = models.CharField(max_length=200)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='forms'
    )

    def __str__(self):
        return self.title


class AdditionalField(models.Model):

    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name='additional_fields'
    )

    field_name = models.CharField(max_length=100)

    def __str__(self):
        return self.field_name


class Question(models.Model):

    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question_text = models.TextField()

    def __str__(self):
        return self.question_text[:50]


class Response(models.Model):

    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name='responses'
    )

    email = models.EmailField()

    overall_rating = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )

    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ['form', 'email']

    def __str__(self):
        return self.email


class AdditionalFieldValue(models.Model):

    response = models.ForeignKey(
        Response,
        on_delete=models.CASCADE,
        related_name='field_values'
    )

    field = models.ForeignKey(
        AdditionalField,
        on_delete=models.CASCADE,
        related_name='values'
    )

    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.field.field_name} : {self.value}"


class Answer(models.Model):

    response = models.ForeignKey(
        Response,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    rating = models.IntegerField()

    def __str__(self):
        return f"{self.question.question_text[:20]} - {self.rating}"