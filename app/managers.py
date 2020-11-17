from django.db import models
from django.db.models import Count


class ProfileManager(models.Manager):
    def best_members(self, members_num=10):
        # TODO: Продумать логику
        return self.all()[:members_num]


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('date_of_create')

    def hot_questions(self):
        return self.order_by('-rating__rating')

    def get_questions_by_tag(self, tag):
        return self.filter(tags__name=tag)

    def get_questions_by_id(self, question_id):
        return self(id=question_id)


class AnswerManager(models.Manager):
    def get_answers_of_question(self, question):
        return self.filter(question__id=question)


class TagManager(models.Manager):
    def get_top_tags(self, count=10):
        return self.annotate(question_count=Count('question')).order_by('-question_count')[:count]


