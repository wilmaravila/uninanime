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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Character(models.Model):
    name = models.CharField(max_length=150)

    role = models.CharField(
        max_length=50,
        blank=True
    )

    description = models.TextField(blank=True)

    image_url = models.URLField(default="https://i.imgur.com/cZL0mCq.jpeg")

    age = models.IntegerField(
        null=True,
        blank=True
    )

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

    poster_url = models.URLField(default="https://i.imgur.com/QvUUowX.jpeg")

    genres = models.JSONField()

    reviews = models.ArrayField(
        model_container=Review,
        blank=True,
        default=list
    )

    characters = models.ArrayField(
        model_container=Character,
        blank=True,
        default=list
    )

    stats = models.JSONField(default=dict)


    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not isinstance(self.genres, list):
            raise ValidationError("Generos debe ser una lista")

        if len(self.genres) == 0:
            raise ValidationError("Debe tener al menos un género")

        character_names = set()

        for character in self.characters:

            if character.name in character_names:
                raise ValidationError(
                    f"El personaje '{character.name}' ya existe"
                )

            character_names.add(character.name)

        review_users = set()

        for review in self.reviews:

            if review.username in review_users:
                raise ValidationError(
                    f"{review.username} ya hizo una review"
                )

            review_users.add(review.username)

    def __str__(self):
        return self.title