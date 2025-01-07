from django.shortcuts import render
from django.http import HttpResponse
from . import util
import markdown2


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
            "page": page, "content": markdown2.markdown(x)
        })

