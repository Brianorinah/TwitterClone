from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Create your views here.


def login_view(request, *args, **kwags):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user_ = form.get_user()
        login(request, user_)
        return redirect("/")
    context = {
        "form": form,
        "btn_label": "Login",
        "title": "Login"

    }
    return render(request, "accounts/auth.html", context)


def logout_view(request, *args, **kwags):
    if request.method == "POST":
        logout(request)
        return redirect("/login")
    context = {
        "form": None,
        "btn_label": "Logout?",
        "title": "Logout"

    }
    return render(request, "accounts/auth.html", context)


def register_view(request, *args, **kwags):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=True)
        user.set_password(form.cleaned_data.get("password1"))
        #You can add functionality to send a confirmation email to verify
        login(request, user)
        return redirect("/")
        #Create a suer manually
        #username = form.cleaned_data.get("username")
        #User.objects.create(username=username)
    context = {
        "form": form,
        "descrption": "Are you sure you want to login",
        "btn_label" "Click to confirm"
        "btn_label": "Register",
        "title": "Register"
    }
    return render(request, "accounts/auth.html", context)
