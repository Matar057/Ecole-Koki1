from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from .forms import UserRegistrationForm, CustomAuthenticationForm, UserProfileForm, UserAdminForm
from .decorators import role_required
from django.contrib.auth import get_user_model

User = get_user_model()


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                messages.success(request, f'Bon retour, {user.get_full_name()} !')
                return redirect('dashboard:home')
            else:
                messages.error(request, 'Votre compte est désactivé.')
        else:
            messages.error(request, 'Email ou mot de passe invalide.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('users:login')


@role_required('admin')
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Utilisateur {user.get_full_name()} créé avec succès.')
            return redirect('users:user_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})


@role_required('admin')
def user_list(request):
    users = User.objects.all().select_related()
    return render(request, 'users/user_list.html', {'users': users})


@role_required('admin')
def user_detail(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_detail.html', {'user_obj': user_obj})


@role_required('admin')
def user_edit(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserAdminForm(request.POST, request.FILES, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Utilisateur {user_obj.get_full_name()} modifié avec succès.')
            return redirect('users:user_detail', pk=pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserAdminForm(instance=user_obj)
    return render(request, 'users/user_edit.html', {'form': form, 'user_obj': user_obj})


@role_required('admin')
def user_delete(request, pk):
    if request.method == 'POST':
        user = User.objects.get(pk=pk)
        if user == request.user:
            messages.error(request, 'Vous ne pouvez pas supprimer votre propre compte.')
        else:
            user.delete()
            messages.success(request, 'Utilisateur supprimé avec succès.')
        return redirect('users:user_list')
    return redirect('users:user_list')
