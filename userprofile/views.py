from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from task_manager.models import Task, TaskAnswer
from userprofile.forms import *
from userprofile.models import Comments, Profile


class ProfileView(UpdateView):
    model = User
    form_class = UserForm
    template_name = "userprofile/profile.html"
    pk_url_kwarg = "profile_id"

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.kwargs['profile_id']])

    def get_context_data(self, **kwargs):
        comments = Comments.objects.filter(user_id=self.kwargs['profile_id'])
        context = super().get_context_data(**kwargs)
        context["comments"] = comments
        context['form_profile_photo'] = UpdateProfilePhotoForm
        return context


def profile_view(request, profile_id):
    context = {}
    context['tasks_count'] = Task.objects.filter(customer_id=profile_id).count()
    context['responses_count'] = TaskAnswer.objects.filter(author_id=profile_id).count()
    if request.method == 'POST':
        form_update_info = UserForm(request.POST, instance=request.user)
        form_update_photo = UpdateProfilePhotoForm(request.POST, request.FILES, instance=request.user.profile)
        if form_update_info.is_valid():
            form_update_info.save()
        if form_update_photo.is_valid():
            form_update_photo.save()
        return redirect('profile', profile_id)
    else:
        context["form"] = UserForm(instance=request.user)
        context['form_profile_photo'] = UpdateProfilePhotoForm
        return render(request, 'userprofile/profile.html', context=context)


# def profile_update(request):
#     if request.method == "POST":
#         user_form = UserForm(request.POST, request.FILES, instance=request.user)
#         profile_form = ProfileForm(request.POST, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             return redirect('home')
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#         return render(request, "main/profile_update.html", {
#             'user_form': user_form,
#             'profile_form': profile_form
#         })


def executor_info_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            profile_user = Profile.objects.get(user=request.user)
            profile_user.is_executor = True
            profile_user.save()
            return redirect("home")
        else:
            return render(request, 'userprofile/executor-info.html')
    else:
        return redirect('home')


def update_profile_view(request):
    context = {}
    if request.user.is_authenticated:
        if request.method == "POST":
            form_profile = UpdateProfileForm(request.POST)
            form_resume = UpdateResumeForm(request.POST, instance=request.user.resume)
            if form_profile.is_valid() and form_resume.is_valid():
                profile = Profile.objects.get(user=request.user)
                profile.age = form_profile.cleaned_data['age']
                profile.save()
                form_resume.save()
                return redirect("profile", profile_id=request.user.id)
            else:
                context['form_profile'] = form_profile
                context['form_resume'] = form_resume
                return render(request, 'userprofile/update_profile.html', context=context)
        else:
            profile = Profile.objects.get(user=request.user)
            context['form_profile'] = UpdateProfileForm
            context['form_resume'] = UpdateResumeForm(instance=request.user.resume)
            return render(request, 'userprofile/update_profile.html', context)
    else:
        raise PermissionDenied()
