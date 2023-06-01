from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, FormView, CreateView, DeleteView, UpdateView, DetailView

# from todolist.forms import AddingForm
from todolist.models import Task


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, CreateView, ListView):
    model = Task
    fields = ['title']
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        return TitleCreate.as_view()(request)


class TitleCreate(CreateView):
    model = Task
    fields = ['title']
    template_name = 'task_list.html'
    success_url = reverse_lazy('tasks')


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'start_time', 'end_time', 'complete']
    template_name = 'task_form.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('tasks')


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'start_time', 'end_time', 'complete']
    template_name = 'task_update.html'
    success_url = reverse_lazy('tasks')


def calendar(request):
    # get the selected date from the request
    selected_date = request.GET.get('selected_date')
    future_activities = ''
    if selected_date:
        # convert the string date to a datetime object
        selected_datetime = timezone.datetime.strptime(selected_date, '%Y-%m-%d')
        # get the activities for the selected date
        activities = Task.objects.filter(start_time__date=selected_datetime.date())
        future_activities = Task.objects.filter(end_time__date__gte=selected_datetime.date())
    else:
        # if no date is selected, show today's activities
        activities = Task.objects.filter(start_time__date=timezone.now().date())
    return render(request, 'calendar.html', {'activities': activities, 'future_activities': future_activities})
