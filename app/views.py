from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import Question, Tag, Answer, Profile


def paginate(objects_list, request, per_page=20):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    return paginator.get_page(page)


def index(request):
    return render(request, 'index.html', {
        'questions': paginate(Question.objects.new_questions(), request, 20),
        'tags': Tag.objects.get_top_tags(),
        'members': Profile.objects.best_members(),
    })


def hot(request):
    return render(request, 'hot.html', {
        'questions': paginate(Question.objects.hot_questions(), request, 20),
        'tags': Tag.objects.get_top_tags(),
        'members': Profile.objects.best_members(),
    })


def questions_by_tag(request, tag):
    return render(request, 'tag.html', {
        'tag': tag,
        'questions': paginate(Question.objects.get_questions_by_tag(tag), request, 20),
        'tags': Tag.objects.get_top_tags(),
        'members': Profile.objects.best_members(),
    })


def question_by_id(request, question_id):
    return render(request, 'question.html', {
        'question': Question.objects.get(id=question_id),
        'answers': paginate(Answer.objects.get_answers_of_question(question_id), request, 30),
        'tags': Tag.objects.get_top_tags(),
        'members': Profile.objects.best_members(),
    })


def login(request):
    return render(request, 'login.html', {
        'tags': Tag.objects.get_top_tags(),
        'members': Profile.objects.best_members(),
    })


def signup(request):
    return render(request, 'signup.html', {
        'tags': Tag.objects.get_top_tags(),
        'members': Profile.objects.best_members(),
    })


def ask(request):
    return render(request, 'ask.html', {
        'tags': Tag.objects.get_top_tags(),
        'members': Profile.objects.best_members(),
    })


def settings(request):
    return render(request, 'settings.html', {
        'tags': Tag.objects.get_top_tags(),
        'members': Profile.objects.best_members(),
    })

