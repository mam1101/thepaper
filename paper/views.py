import datetime
import json
import random

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect

from paper.forms import PaperItemForm
from paper.models import PaperItem


def index(request):
    context_dict = {}
    return render(request, 'index.html', context_dict)


@login_required()
def create_new_paper(request):
    data = request.GET
    default_text = data.get('respond')
    context_dict = {}
    if default_text is not None:
        context_dict = {'respond': '@' + default_text}
    return render(request, 'create_new_paper.html', context_dict)


def view_paper(request, slug):
    paper = PaperItem.objects.filter(slug=slug)
    context_dict = {}
    if paper.exists():
        if not paper.first().published and paper.first().owner == request.user:
            return redirect('/')
        context_dict = {'paper': paper.first()}
    return render(request, 'view_paper.html', context_dict)


@login_required()
def submit_paper(request):
    context_dict = {}
    if request.method == 'POST':
        form = PaperItemForm(request.POST)
        if form.is_valid():
            paper_item = form.save()
            return redirect('/paper/{}/'.format(paper_item.slug))
    return redirect('/')


def get_random_paper(request):
    random_paper = PaperItem.objects.random()
    return redirect('/paper/{}/'.format(random_paper.slug), permanent=False)


def get_front_page(request):
    data = request.GET
    date = data.get('date')

    current_paper = PaperItem.objects.all().first()
    serialized_obj = serializers.serialize('json', [current_paper, ])
    json_object = json.loads(serialized_obj)[0]

    return JsonResponse({'Success': json_object})


def get_page(request):
    data = request.GET
    page = int(data.get('page'))
    date = data.get('date')
    current_paper = None
    if page == 0:
        current_paper = PaperItem.objects.all().first()
    else:
        page = page - 1
        current_paper = PaperItem.objects.filter(created__lte=date).order_by('-created')[page]
    serialized_obj = serializers.serialize('json', [current_paper, ])
    json_object = json.loads(serialized_obj)[0]

    return JsonResponse({'Success': json_object})


@login_required()
def follow_publisher(request):

    return JsonResponse({'Success': 'Account Followed'})
