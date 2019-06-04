from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from django.core.exceptions import ValidationError
from lists.forms import ItemForm
# Create your views here.


def home_page(request):

    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    # list_ = List.objects.get(id=list_id)
    # error = None

    # if request.method == 'POST':
    #     try:
    #         # 此处不能使用 Item.objects.create(...) ，否则item直接在数据库中保存，不需要经过.save()函数
    #         # item = Item.objects.create(text=request.POST['item_text'], list=list_)
    #         item = Item(text=request.POST['text'], list=list_)
    #         item.full_clean()
    #         item.save()
    #         return redirect(list_)
    #     except ValidationError:
    #         error = "You can't have an empty list item"

    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)
    return render(request, 'list.html', {
        'list': list_,
        'form': form,
        # 'error': error,
    })


def new_list(request):
    # list_ = List.objects.create()
    # item = Item.objects.create(text=request.POST['text'], list=list_)
    # try:
    #     item.full_clean()
    #     item.save()
    # except ValidationError:
    #     list_.delete()
    #     error = "You can't have an empty list item"
    #     return render(request, 'home.html', {'error': error})
    # return redirect(list_)
    # return redirect('view_list', list_.id)

    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})


