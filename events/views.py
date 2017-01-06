from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Event
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EventForm


def events_list(request):
    #events = event.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    contact_list = Event.objects.all()
    paginator = Paginator(contact_list, 6)# Show 25 contacts per page

    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        events = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        events = paginator.page(paginator.num_pages)
    return render(request, 'events/events_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)

    return render(request, 'events/event_detail.html', {'event': event})


def event_new(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.published_date = timezone.now()
            event.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
        return render(request, 'events/event_edit.html', {'form': form})


def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES,  instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.published_date = timezone.now()
            event.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_edit.html', {'form': form})

def event_remove(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return redirect('events_list')

