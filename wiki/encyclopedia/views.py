import random
import markdown2 as Markdown
from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util


def getEntry(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return errNotFound(request)
    return renderEntry(request, title, entry)


def addNewEntry(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            entry = form.cleaned_data['entry']
            if (title in util.list_entries()):
                return renderError(request,
                                   "Entry already exists in database.")
            util.save_entry(title, entry)
            return HttpResponseRedirect(reverse('enc:wiki', args=[title]))
        else:
            return renderNewEntry(request)
    else:
        return renderNewEntry(request)


def editEntry(request, title):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            entry = form.cleaned_data['entry']
            util.save_entry(title, entry)
            return HttpResponseRedirect(reverse('enc:wiki', args=[title]))
        else:
            return renderEditEntry(request, title)
    else:
        if title in util.list_entries():
            return renderEditEntry(request, title)
        else:
            return renderError(request,
                               "Cannot edit entry that does not exist.")


def doSearch(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data['q']
            entries = util.list_entries()
            if q in entries:
                return HttpResponseRedirect(reverse('enc:wiki', args=[q]))
            else:
                filteredEntries = [entry for entry in entries if q in entry]
                return renderSearchResults(request, filteredEntries)
        else:
            return HttpResponseRedirect(reverse('enc:index'))
    else:
        return HttpResponseRedirect(reverse('enc:index'))


def getRandom(request):
    entries = util.list_entries()
    randomTitle = random.choice(entries)
    return HttpResponseRedirect(reverse('enc:wiki', args=[randomTitle]))


# PAGE RENDER FUNCTIONS
def renderIndex(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searchForm": SearchForm()
    })


def renderSearchResults(request, results):
    return render(request, "encyclopedia/searchResults.html", {
        "results": results,
        "searchForm": SearchForm()
    })


def renderEntry(request, title, entry):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": Markdown.markdown(entry),
        "searchForm": SearchForm()
    })


def renderNewEntry(request):
    return render(request, "encyclopedia/newEntry.html", {
        "searchForm": SearchForm(),
        "entryForm": EntryForm()
    })


def renderEditEntry(request, title):
    initialData = {
        'title': title,
        'entry': util.get_entry(title)
    }
    return render(request, "encyclopedia/editEntry.html", {
        "title": title,
        "searchForm": SearchForm(),
        "entryForm": EntryForm(initial=initialData or None)
    })


def errNotFound(request):
    return render(request, "encyclopedia/errNotFound.html", {
        "searchForm": SearchForm()
    })


def renderError(request, errMsg):
    return render(request, "encyclopedia/error.html", {
        "errMsg": errMsg
    })


# FORM CLASSES
class SearchForm(forms.Form):
    q = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={
            'placeholder': 'search entries here',
            'class': 'form-control mt-2 mb-2'
        }
    ))


class EntryForm(forms.Form):
    title = forms.CharField(label='title', max_length=100,
                            widget=forms.TextInput(
                                attrs={
                                    'placeholder': 'new entry title',
                                    'class': 'form-control mb-3'
                                }
                            ))
    entry = forms.CharField(label='content',
                            widget=forms.Textarea(
                                attrs={
                                    'placeholder': 'new entry content',
                                    'rows': '15',
                                    'class': 'form-control mb-3'
                                }
                            ))
