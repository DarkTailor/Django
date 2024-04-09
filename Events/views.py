from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import Events
from users.models import UserProfile
from .forms import EventsForm

from django.contrib.auth.decorators import user_passes_test

# Decorator to check if the user is a staff member
def is_staff(user):
    return user.is_staff

@login_required
def list_events(request):
    template = "Events/list.html"
    events = Events.objects.all()
    profile = UserProfile.objects.get_or_create(user=request.user)
    context = {"events": events, "events_active_list": "active", "profile": profile}
    return render(request, template, context)


@user_passes_test(is_staff)
def add_events(request):
    template = "Events/add.html"
    form = EventsForm()
    profile = UserProfile.objects.get_or_create(user=request.user)
    context = {"form": form, "events_active_add": "active", "profile": profile}
    return render(request, template, context)


@user_passes_test(is_staff)
def create_event(request):
    if request.method == "POST":
        form = EventsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Created Successfully")
            return redirect('list_events')
        else:
            messages.error(request, "Event Creation Failed")
            return redirect('add_events')


@user_passes_test(is_staff)
def edit_event(request, pk):
    event = get_object_or_404(Events, pk=pk)
    template = "Events/edit.html"
    form = EventsForm(instance=event)
    profile = UserProfile.objects.get_or_create(user=request.user)
    context = {"form": form, "events_active_add": "active", "profile": profile}
    if request.method == "POST":
        form = EventsForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect('list_events')
        else:
            messages.error(request, "Event Update Failed")
    return render(request, template, context)


@user_passes_test(is_staff)
def delete_event(request, pk):
    event = get_object_or_404(Events, pk=pk)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event Deleted Successfully")
        return redirect('list_events')
    return render(request, "Events/confirm_delete.html", {"event": event})





def api_get_event(request):
    Events = Events.objects.all()
    data = {"Events": Events}
    return JsonResponse(data, content_type="Application/json", safe=False)


def api_edit_event(request, pk):
    if request.method == "POST":
        Events = get_object_or_404(Events, pk=pk)
        form = EventsForm(request.POST or None, instance=Events)
        if form.is_valid():
            form.save()
            data = {"STATUS": "OK", "CODE": 0}
        else:
            data = {"STATUS": "INVALID"}
        return JsonResponse(data, content_type="Application/json", safe=False)


# def api_delete_ministry(request, pk):



def api_create_event(request):
    if request.method == "POST":
        form = EventsForm(request.POST, request.FILES or None)
        if form.is_valid():
            Events = form.save(commit=False)
            Events.save()
            data = {"STATUS": "OK", "MINISTRY_ID": ministry.pk}
            return JsonResponse(data, content_type="Application/json", safe=False)
        else:
            data = {"STATUS": "INVALID"}
            return JsonResponse(data, content_type="Application/json", safe=False)

