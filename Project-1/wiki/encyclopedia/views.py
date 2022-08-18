from django.shortcuts import render, redirect

from . import util

import random

import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display(request, title):
    html = util.get_entry(title)
    if html != None:
        html = markdown2.markdown(html)
        
    return render(request, "encyclopedia/display.html", {
        "title": title, "content": html
    })

def search(request):
    q = request.GET['q']
    
    entries =  util.list_entries()
    substringentry = []
    
    for i in entries:
        if q.lower() == i.lower():
            return redirect(f'wiki/{i}')
        
        elif q.lower() in i.lower():
            substringentry.append(i)
                
    if substringentry == []:
        substringentry = None
    
    return render(request, "encyclopedia/searchresult.html", {
        "entries": substringentry
    })
    
def randomentry(request):
    entries = util.list_entries()
    randchoice = random.choice(entries)
    return redirect(f'wiki/{randchoice}')

def create(request):
    if request.method=="POST":
        title = request.POST["title"]
        content = request.POST["content"]
        entries = util.list_entries()
        
        for i in entries:
            if title.lower() == i.lower():
                return render(request, "encyclopedia/createerror.html")
        
        util.save_entry(title, content)
        return redirect(f'wiki/{title}')
        
    else:
        return render(request, "encyclopedia/createnew.html")
    
def edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["updatecontent"]
        util.save_entry(title, content)
        return redirect(f'wiki/{title}')
    
    else:
        title = request.GET["title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title, "content": content
        })