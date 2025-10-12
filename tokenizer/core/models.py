import os
from django.db import models


class Token(models.Model):
    header = models.CharField(max_length=200, db_index=True, verbose_name="Header", null=True, blank=True)
    number = models.CharField(max_length=20, db_index=True, verbose_name="Token number")
    title = models.CharField(max_length=100, db_index=True, verbose_name="Title", null=True, blank=True)
    description = models.CharField(max_length=200, blank=True, null=True, verbose_name="Description")
    date = models.DateField(verbose_name="Token date")
    preview_image = models.ImageField(upload_to='tokens/previews/', blank=True, null=True, verbose_name="Preview image")
    small_preview = models.BooleanField(default=False, verbose_name="Small preview")

    def __str__(self):
        return f"Token {self.number} ({self.title})"

    def delete(self, *args, **kwargs):
        # Delete the preview image file when the Token is deleted
        if self.preview_image and os.path.isfile(self.preview_image.path):
            os.remove(self.preview_image.path)
        super(Token, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"
