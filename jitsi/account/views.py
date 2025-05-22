from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, TeamForm
from .models import Account, Team


@login_required
def home(request):
    person = Account.objects.get(id=request.user.id)
    if person.team is not None:
        return render(request, 'home.html', context={'team': person.team.name})
    else:
        return render(request, 'home.html', context={'team': None})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            person = form.save()
            login(request, person)
            return redirect("team")
    else:
        form = SignUpForm()
    return render(request, "signup.html", context={"form": form})


def login_account(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get("username"),
                                password=form.cleaned_data.get("password"))
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                return redirect("login")
    else:
        form = LoginForm()
    return render(request, "login.html", context={"form": form})


def logout_account(request):
    logout(request)
    return redirect("login")


@login_required
def joinoradd_team(request):
    person = Account.objects.get(id=request.user.id)
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data.get("name")
            if Team.objects.filter(name=team_name).exists():
                team = Team.objects.get(name=team_name)
                person.team = team
            else:
                team = form.save(commit=False)
                team.jitsi_url_path = f'http://meet.jit.si/{team_name}'
                team.save()
                person.team = team
                person.save()
                return redirect("home")
        else:
            return redirect("home")

    else:
        if person.team:
            return redirect("home")
        else:
            form = TeamForm()
            return render(request, "team.html", context={"form": form})


def exit_team(request):
    person = Account.objects.get(id=request.user.id)
    if person.team is not None:
        person.team = None
        person.save()
        return redirect("home")
    else:
        return redirect("home")
