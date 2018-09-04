from django.shortcuts import render, redirect
from.models import User, Itemlist
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,"first_app/index.html")

def register(request):
    results = User.objects.register(request.POST)
    print(results)
    if not results[0]:
        for error in results[1]:
            messages.add_message(request,messages.ERROR,error)
        return redirect("/")
    else:
        user = results[1]
        request.session['user_id'] = user.id
        return redirect('/dashboard')

def login(request):
    requestData = User.objects.login(request.POST)
    if not (requestData[0]):
        for error in requestData[1]:
            messages.error(request, error)
        return redirect("/")
    else: # if succeeds in login
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id

        return redirect("/dashboard")

def dashboard(request):
    if not 'user_id' in request.session:
        return redirect('/')

    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'items': Itemlist.objects.all(),
        'favorite_items': User.objects.get(id=request.session['user_id']).user_favorite_items.all()
    }

    return render(request, 'first_app/dashboard.html', context)

def addItemPage(request):

    return render(request, 'first_app/addItem.html')

def logOut(request):
    if not 'user_id' in request.session:
        return redirect('/')
    request.session.flush()

    return redirect('/')

def addItem(request):
    if not 'user_id' in request.session:
        return redirect('/')
        
    #Adding movie then adding one to many relationship
    results = Itemlist.objects.add_item(request.POST)

    if not (results[0]):
        print(results[1])
        for error in results[1]:
            messages.error(request, error)
        return redirect("/addItemPage")
    else: # if succeeds in login
        #Adds created_by for Itemlist
        Itemlist.objects.create(title=request.POST['title'],item_added_by=User.objects.get(id=request.session['user_id']))
        return redirect('/dashboard')

def favoriteItem(request,  item_id):
    if not 'user_id' in request.session:
        return redirect('/')

    Itemlist.objects.get(id=item_id).item_favorited_by_users.add(User.objects.get(id=request.session['user_id']))

    return redirect('/dashboard')

def showItemPage(request, item_id):
    context = {
        'item': Itemlist.objects.get(id=item_id),
        'users_favorited': Itemlist.objects.get(id=item_id).item_favorited_by_users.all()
    }

    return render(request, 'first_app/show.html', context)

def cancelfavoriteItem(request,  item_id):
    if not 'user_id' in request.session:
        return redirect('/')

    Itemlist.objects.get(id=item_id).item_favorited_by_users.remove(User.objects.get(id=request.session['user_id']))

    return redirect('/dashboard')

def delete(request,  item_id):
    if not 'user_id' in request.session:
        return redirect('/')

    
    Itemlist.objects.get(id=item_id).delete()

    return redirect('/dashboard')    