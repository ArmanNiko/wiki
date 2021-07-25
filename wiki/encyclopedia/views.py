import re
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from . import util
from django.urls import reverse

import markdown2
from random import choice

def convert(file, name):
    text = file
    html = markdown2.markdown(text)
    new = 'encyclopedia\\templates\\encyclopedia'

    with open(f"{name.replace('md', 'html').replace('entries', new)}", 'w') as f:
        f.write(html)
    
    return f"{name.replace('md', 'html').replace('entries', new)}"


class CreatePage(forms.Form):
    title = forms.CharField(label="title", max_length=20, min_length=3)
    content = forms.CharField(label="content", min_length = 30)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "random": choice(util.list_entries())
    })

def show(request, title):
    if request.method == 'POST':
        title = request.POST.get("q")
    try:
        return render(request, convert(*util.get_entry(title)))
    except:
        if title == 'create.html':
            return render(request, 'encyclopedia\\create.html', {
                'form': CreatePage(),
            })
        if title == 'index.html':
            return HttpResponseRedirect(reverse('wiki:index'))
        return render(request, 'encyclopedia\\notfound.html', {
            'entries': util.list_entries(),
        })

def create(request):
    print('hi')
    form = CreatePage(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        with open(f"entries\\{title}.md", 'w') as f:
            f.write(f'#{title}\n{content}\n[Edit this Page](create.html)\n[Home Page](index.html)')
    else:
        return render(request, 'encyclopedia\\create.html', {
            'form': CreatePage(),
        })
    
    return HttpResponseRedirect(reverse('wiki:index'))
