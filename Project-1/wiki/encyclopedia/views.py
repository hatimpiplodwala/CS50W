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
            
    return render(request, "encyclopedia/result.html", {
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
                return render(request, "encyclopedia/error.html",{
                    "message":"Created page already exists", "code":"404"
                })
        
        util.save_entry(title, content)
        return redirect(f'wiki/{title}')
        
    else:
        return render(request, "encyclopedia/create.html")
    
def edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["updatecontent"]
        entries = util.list_entries()
        for i in entries:
            if title.lower() == i.lower():
                util.save_entry(title, content)
                return redirect(f'wiki/{title}')
            
        return render(request, "encyclopedia/error.html",{
            "message":"Cannot modify title while editing", "code":"400"
        })
                
    else:
        title = request.GET["title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title, "content": content
        })