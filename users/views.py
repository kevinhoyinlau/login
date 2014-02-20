from django.shortcuts import render
from django.http import HttpResponse, Http404
from users.models import UserModel, UserForm

errors = {
    UserModel.ERR_BAD_CREDENTIALS: "LOGIN ERROR: Username/password not found",
    UserModel.ERR_USER_EXISTS:  "ADD USER ERROR: Username already exists",
    UserModel.ERR_BAD_PASSWORD: "ADD USER ERROR: Password is too long",
    None: "Please enter your credentials below", # This one should never appear
}

# Create your views here.
def index(request):
    context = {'message' : "Please enter your credentials below"}
    if request.method == 'POST':
        form = UserForm(request.POST)
        username = form.data[u'username']
        password = form.data[u'passwd']
        if u'login' in form.data:
            result = UserModel.login(username, password)
        elif u'adduser' in form.data:
            result = UserModel.add(username, password)
        else:
            result = None # This should never be reached

        if result == UserModel.SUCCESS:
            u = UserModel.objects.get(username = username)
            context['message'] = "User {0} has logged on {1} times".format(u.username, u.count)
            return render(request, 'users/login.html', context )
        elif result == UserModel.ERR_BAD_USERNAME:
            context['message'] = "ADD USER ERROR: Username is " + ("empty" if len(username) == 0 else "too long")
        else:
            context['message'] = errors[result]
    else:
        form = UserForm()
    context['form'] = form
    return render(request, 'users/login.html', context )