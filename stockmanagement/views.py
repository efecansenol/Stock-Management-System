from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from .forms import IssueForm, ReceiveForm
from django.contrib.auth.decorators import login_required
def home(request):
    title = 'Welcome to this page !'

    context = {
        "title": title,

    }
    return render(request, "home.html", context)
def list_items(request):
    header = 'List of items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        "header": header,
        "queryset": queryset,
        "form": form,
    }
    if request.method == 'POST':
        queryset = Stock.objects.filter( item_name__icontains=form['item_name'].value()) 
        context = { 
            "form": form,
            "header": header,
            "queryset": queryset,
        }
    return render(request, "list_items.html",context)
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():       
        form.save()
        messages.success(request, 'Succesfully Saved!')
        return redirect('/list_items')
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "add_items.html", context)

def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():            
            form.save()
            messages.success(request, 'Succesfully Updated!')
            return redirect('/list_items')
        
    context = {
        'form': form
    }
    return render(request, 'add_items.html', context)

def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Succesfully Deleted!')
        return redirect('/list_items')
    return render(request, 'delete_items.html')
def stock_detail(request, pk):
    query_set = Stock.objects.get(id=pk)
    context = {
        "queryset": query_set,
    }
    return render(request, "stock_detail.html", context)

def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None,instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity -= instance.issue_quantity
        messages.success(request, "Issued Succesfully!" + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
        instance.save()

        return redirect('/stock_detail/'+str(instance.id))
    
    context ={
        "title": 'Issue' + str(queryset.item_name),
        "query_set": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)
def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None,instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity += instance.receive_quantity
        instance.issue_by = str(request.user)
        instance.save()
        messages.success(request, "Received Succesfully!" + str(instance.quantity) + " " + str(instance.item_name) + "s now  in Store")
        return redirect('/stock_detail/'+str(instance.id))
    
    context ={
        "title": 'Receive' + str(queryset.item_name),
        "instance": queryset,
        "form": form,
        "username": 'Received By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)
def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder Level for" + str(instance.item_name) + " is updated to" + str(instance.reorder_level))
        return redirect("/list_items")
    context = {
        "instance": queryset,
        "form": form,
    }
    return render (request, "add_items.html", context)
    
# Create your views here.   
