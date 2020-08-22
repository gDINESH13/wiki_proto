from django.shortcuts import render

from . import util
import markdown2
import random as rd
from django.contrib import messages
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect



class newpage(forms.Form):
	title=forms.CharField(label="Title")
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
				l["body"]="No Search found."
				return render(request,"encyclopedia/error.html",l)
			return render(request,"encyclopedia/index.html",l)
			
		else:
			return HttpResponseRedirect(reverse("wiki",kwargs={"title":request.POST["search-text"]}))
	return render(request,"encyclopedia/index.html",l)


	
	#return render(request, "encyclopedia/index.html", context)
def wiki(request,title):
	"""try:
		html=markdown2.markdown(util.get_entry(title))
	except:
		
		return render(request, "encyclopedia/error.html", {"title": title})"""
	
	html=markdown2.markdown(util.get_entry(title))
	l={"entries":util.list_entries(),"title":title,"markdown":str(html)}
	return render(request,"encyclopedia/wiki.html",l)



def random(request):
	entries=util.list_entries()
	size=len(entries)
	#rand=rd.randint(size)
	entry=rd.choice(entries)
	return HttpResponseRedirect(reverse("wiki",kwargs={"title":entry}))
def new(request):
	if request.method=="POST":
		form=newpage(request.POST)
		if form.is_valid():
			title=form.cleaned_data["title"]
			content=form.cleaned_data["content"]
			if not util.get_entry(title):
				util.save_entry(title,content)
				return HttpResponseRedirect(reverse("wiki",kwargs={"title":title}))
			else:
				messages.error(request,"entry already exist")
				return render(request,"encyclopedia/newpage.html",{"form":form})
		else:
			return render(request,"encyclopedia/newpage.html",{"form":form})
	return render(request,"encyclopedia/newpage.html",{"form":newpage()})




