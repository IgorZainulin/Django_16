from django import forms
from django.core.exceptions import ValidationError

from .models import Post

from datetime import date

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'header',
            'author',
            'text',
            'category',
        ]


    def clean_text(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "Описание не может быть менее 20 символов."
            })

        return text



    def clean(self):
        cleaned_data = super().clean()
        author = cleaned_data['author']
        today = date.today()
        post_limit = Post.objects.filter(author=author, create_time__date=today).count()
        if post_limit >= 3:
            raise ValidationError('Нельзя публиковать больше трех постов в сутки!!!')
        return cleaned_data







