from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from userprofile.forms import UserForm, UpdateProfileForm, UpdateResumeForm
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
        return context


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
    if request.user.is_authenticated:
        if request.method == "POST":
            form_profile = UpdateProfileForm(request.POST, instance=request.user.profile)
            form_resume = UpdateResumeForm(request.POST, instance=request.user.resume)
            form_profile.save()
            form_resume.save()
            return redirect("profile", profile_id=request.user.id)
        else:
            context = {}
            context['form_profile'] = UpdateProfileForm(instance=request.user)
            context['form_resume'] = UpdateResumeForm(instance=request.user)
            return render(request, 'userprofile/update_profile.html', context)
    else:
        raise PermissionDenied()
