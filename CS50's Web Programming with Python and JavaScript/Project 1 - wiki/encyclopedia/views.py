from django.shortcuts import render
import markdown
import random

from . import util

def convert_md_to_html(title):
    markdowner = markdown.Markdown()
    content = util.get_entry(title)
    if content:
        return markdowner.convert(content)
    return None

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = convert_md_to_html(title)
    # Ensure title exists
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"Title name {title} couldnt found!"
        })
    
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })

    
def search(request):
    if request.method == "POST":
        # Get posted variables
        entry_search = request.POST["q"]

        # Check is there any content with given entry name
        content = convert_md_to_html(entry_search)
        if content:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": content
            })
        
        # Return all entries constains search as a substring
        matched_entries = \
            [x for x in util.list_entries() if entry_search in x.lower()]
        return render(request, "encyclopedia/index.html", {
            "entries": matched_entries
        })

def new_entry(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_entry.html")
    
    else:
        # Get posted variables
        entry_name = request.POST["new_entry"]
        content = request.POST["entry_content"]

        # Ensure entry name is given
        if not entry_name:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry name should be entered"
            })
        
        # Check entry name already exists
        if util.get_entry(entry_name):
            return render(request, "encyclopedia/error.html", {
                "message": "Given name is already exists"
            })

        # Save entry
        util.save_entry(entry_name, content)
        html_content = convert_md_to_html(entry_name)
        return render(request, "encyclopedia/entry.html", {
            "title": entry_name,
            "content": html_content
        })

def edit_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "old_content": content
        })

def update_entry(request):
    if request.method == "POST":
        title = request.POST["title"]
        new_content = request.POST["new_content"]

        util.save_entry(title, new_content)
        content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    
def random_entry(request):
    entry = random.choice(util.list_entries())
    content = convert_md_to_html(entry)
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "content": content
    })