from djongo import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Anime(models.Model):
    id = models.ObjectIdField(primary_key=True)
    title = models.CharField(max_length=255)
    synopsis = models.TextField()

    episodes = models.IntegerField(
        validators=[MinValueValidator(1)]
    )

    release_year = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100)
        ]
    )

    poster_url = models.URLField(
        default="https://i.imgur.com/QvUUowX.jpeg"
    )

    genres = models.JSONField(default=list)

    reviews = models.JSONField(default=list)

    characters = models.JSONField(default=list)

    stats = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not isinstance(self.genres, list):
            raise ValidationError("genres debe ser una lista")

        if len(self.genres) == 0:
            raise ValidationError("Debe tener al menos un género")
        

        users = set()

        for r in self.reviews:

            if "username" not in r:
                raise ValidationError("review sin username")

            if "rating" not in r:
                raise ValidationError("review sin rating")

            if "comment" not in r:
                raise ValidationError("review sin comment")

            if "description" not in r:
                r["description"] = "Sin descripción"

            if not isinstance(r["rating"], int):
                raise ValidationError("rating debe ser un número")

            if not (1 <= r["rating"] <= 5):
                raise ValidationError("rating debe ser entre 1 y 5")

            if r["username"] in users:
                raise ValidationError(
                    f"{r['username']} ya hizo una review"
                )

            users.add(r["username"])

        names = set()

        for c in self.characters:

            if "name" not in c:
                raise ValidationError("character sin name")

            if "image_url" not in c:
                c["image_url"] = "https://i.imgur.com/cZL0mCq.jpeg"

            if "age" in c:
                if not isinstance(c["age"], int) or c["age"] < 0:
                    raise ValidationError("age debe ser un número válido")

            if "gender" in c:
                if c["gender"] not in ["hombre", "mujer", "otro"]:
                    raise ValidationError("gender inválido")

            if c["name"] in names:
                raise ValidationError(f"personaje duplicado: {c['name']}")

            names.add(c["name"])

    def save(self, *args, **kwargs):

        self.clean()

        if self.reviews:
            total = sum(r.get("rating", 0) for r in self.reviews)
            count = len(self.reviews)

            self.stats = {
                "avg_rating": round(total / count, 2),
                "total_reviews": count,
                "views": self.stats.get("views", 0)
            }
        else:
            self.stats = {
                "avg_rating": 0,
                "total_reviews": 0,
                "views": 0
            }

        super().save(*args, **kwargs)

    