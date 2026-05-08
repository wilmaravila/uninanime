from djongo import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Review(models.Model):
    user_id = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        abstract = True

class Anime(models.Model):
    title = models.CharField(max_length=255)
    synopsis = models.TextField()

    episodes = models.IntegerField(
        validators=[MinValueValidator(1)]
    )

    release_year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )

    genres = models.JSONField()

    reviews = models.ArrayField(
        model_container=Review,
        blank=True,
        default=list
    )

    stats = models.JSONField(default=dict)


    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not isinstance(self.genres, list):
            raise ValidationError("Genres debe ser una lista")

        if len(self.genres) == 0:
            raise ValidationError("Debe tener al menos un género")

    def __str__(self):
        return self.title