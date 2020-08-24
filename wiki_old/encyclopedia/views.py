from django.shortcuts import render

from . import util
import markdown2
import random as rd
from django.contrib import messages
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect



class newpage(forms.Form):
	title=forms.CharField(label="Title",widget=forms.TextInput)
	content=forms.CharField(label="Add Content",widget=forms.Textarea)


def index(request):
	l={"entries":util.list_entries(),"title":"All pages"}
	if(request.method=="POST"):
		search=util.get_entry(request.POST["search-text"])
		if search is None:
			l["title"]="Search Results"
			possibility=[]
			#to check the possbile searches of the user bu the characters entered.
			for i in l["entries"]:
				if request.POST["search-text"].lower() in i.lower():
					possibility.append(i)
			l["entries"]=possibility

			if (len(possibility)==0):
				l["body"]="No such page exist."
				return render(request,"encyclopedia/error.html",l)
			return render(request,"encyclopedia/index.html",l)
			
		else:
			return HttpResponseRedirect(reverse("wiki",kwargs={"title":request.POST["search-text"]}))
	return render(request,"encyclopedia/index.html",l)


	
	
def wiki(request,title):
	try:
		html=markdown2.markdown(util.get_entry(title))
	except:
		return render(request,"encyclopedia/error.html",{"body":"No such page exist","title":"Search Results"})
	l={"entries":util.list_entries(),"title":title,"markdown":str(html)}
	return render(request,"encyclopedia/wiki.html",l)
   
def random(request):
	entries=util.list_entries()
	entry=rd.choice(entries)
	return HttpResponseRedirect(reverse("wiki",kwargs={"title":entry}))
def new(request):
	if request.method=="POST" :
		form=newpage(request.POST)
		if form.is_valid():
			title=form.cleaned_data["title"]
			content=form.cleaned_data["content"]
			if not util.get_entry(title):
				util.save_entry(title,content)
				return HttpResponseRedirect(reverse("wiki",kwargs={"title":title}))
			else:
				messages.error(request,"Title already exist (close this alert message and try again)")
				return render(request,"encyclopedia/newpage.html",{"form":form})
		else:
			return render(request,"encyclopedia/newpage.html",{"form":form})
	return render(request,"encyclopedia/newpage.html",{"form":newpage()})


def edit(request,title1):
	try:
		html=markdown2.markdown(util.get_entry(title1))
	except:
		return render(request,"encyclopedia/error.html",{"body":"No such page exist","title":"Search Results"})
	if request.method=="GET":
		current_title=title1
		md_content=util.get_entry(current_title)
		return render(request,"encyclopedia/edit.html",{"form":newpage(initial={"title":current_title,"content":md_content}),"tat":current_title})
	
	if request.method=="POST":
		form=newpage(request.POST)
		if form.is_valid():
			title=form.cleaned_data["title"]
			edited_content=form.cleaned_data["content"]
			util.save_entry(title,edited_content)
			return HttpResponseRedirect(reverse("wiki",kwargs={"title":title}))

