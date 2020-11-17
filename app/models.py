from django.conf import settings
from django.contrib.auth.models import User
from .managers import *


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=50, verbose_name='Nick name')
    avatar = models.ImageField(upload_to=settings.LOCAL_FILE_DIR,
                               default=f'{settings.LOCAL_FILE_DIR} user_avatar.png',
                               verbose_name='Avatar')
    objects = ProfileManager()

    def __str__(self):
        return self.nick_name

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Rating(models.Model):
    count_likes = models.PositiveIntegerField(default=0, verbose_name='Count likes')
    count_dislikes = models.PositiveIntegerField(default=0, verbose_name='Count dislikes')
    rating = models.IntegerField(default=0, editable=False)
    authors = models.ManyToManyField('Profile', through='RatingAuthors', through_fields=('rating', 'profile'),
                                     blank=False, editable=False, verbose_name='Author')

    def save(self, **kwargs):
        self.rating = self.count_likes - self.count_dislikes
        super(Rating, self).save(**kwargs)

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'


class RatingAuthors(models.Model):
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type_opinion = models.BooleanField(verbose_name='User like it')


class Question(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    text = models.TextField(verbose_name='Text')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Author')
    date_of_create = models.DateField(auto_now_add=True, verbose_name='Date of creating')
    rating = models.ForeignKey('Rating', on_delete=models.PROTECT, editable=False)
    tags = models.ManyToManyField('Tag', blank=False, verbose_name='Tag')

    objects = QuestionManager()

    def delete(self, *args, **kwargs):
        self.rating.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

    def save(self, **kwargs):
        rating = Rating()
        rating.save()
        self.rating = rating
        super(Question, self).save(**kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='Question')
    text = models.TextField(verbose_name='Text')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Author')
    date_of_create = models.DateField(auto_now_add=True, verbose_name='Date of creating')
    flag_correct_answer = models.BooleanField(verbose_name='Is correct')
    rating = models.ForeignKey('Rating', on_delete=models.PROTECT, editable=False)
    objects = AnswerManager()

    def delete(self, *args, **kwargs):
        self.rating.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

    def save(self, **kwargs):
        rating = Rating()
        rating.save()
        self.rating = rating
        super(Answer, self).save(**kwargs)

    def __str__(self):
        return str(self.author)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='Name')
    objects = TagManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
