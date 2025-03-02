from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from . import util
import markdown2
from django.urls import reverse
from django.http import HttpResponseRedirect

class Create_entry(forms.Form):
    title = forms.CharField(max_length=20)
    content = forms.CharField(widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display(request, page):
    x = util.get_entry(page)
    if x == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entries.html", {
            "page": page,
            "content": markdown2.markdown(x),
            "entries": util.list_entries()
        })

def search(request):
    if request.method == "GET":
        query = request.GET.get('q')
        x = util.get_entry(query)
        if x == None:
            return render(request, "encyclopedia/search.html", {
                "entries": util.list_entries(),
                "query":query
            })
        else:
            return render(request, "encyclopedia/entries.html", {
                "page": query, 
                "content": markdown2.markdown(x),
                "entries": util.list_entries()
            })

def add(request):
    if request.method == "POST":
        form = Create_entry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(f'/wiki/{title}')
        else:
            return render(request, "encyclopedia/add.html", {
                "entries": util.list_entries(),
                "form": form
            })
    return render(request, "encyclopedia/add.html", {
        "entries": util.list_entries(),
        "form": Create_entry()
    })
    
def edit(request, page):
    initial_cont = util.get_entry(page)
    initial_values = {
        'title': page,
        'content':initial_cont
    }
    if request.method == "POST":
        form = Create_entry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(f'/wiki/{title}')
        else:
            return render(request, "encyclopedia/add.html", {
                "entries": util.list_entries(),
                "form": form,
                "page": page
            })
    return render(request, "encyclopedia/edit.html", {
        "entries": util.list_entries(),
        "form": Create_entry(initial=initial_values),
        "page": page
    })