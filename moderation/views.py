from django.shortcuts import render, HttpResponse, get_object_or_404
from spotteds.models import PendingSpotted, Spotted
from django.http import JsonResponse, Http404
from api.api_interface import api_process_approved, api_process_rejected, api_reject_options, api_process_deleted
from .forms import WorkHourFormSet
from django.contrib import messages
from .models import Moderator
from django.contrib.auth.decorators import user_passes_test
from .decorators import is_moderator
# Create your views here.


# Generic Views

@user_passes_test(is_moderator)
def pending_spotteds(request):
    spotteds = PendingSpotted.objects.filter(polemic=False).order_by('-id')
    return render(request, 'moderation/pending_spotteds.html', {
        'spotteds': spotteds,
    })


@user_passes_test(is_moderator)
def polemic_spotteds(request):
    spotteds = PendingSpotted.objects.filter(polemic=True).order_by('-id')
    return render(request, 'moderation/polemic_spotteds.html', {
        'spotteds': spotteds,
    })


@user_passes_test(is_moderator)
def history_spotteds(request):
    spotteds = Spotted.objects.filter(reported='').order_by('-id')
    return render(request, 'moderation/history_spotteds.html', {
        'spotteds': spotteds,
    })


@user_passes_test(is_moderator)
def reported_spotteds(request):
    spotteds = Spotted.objects.exclude(reported='').order_by('-id')
    return render(request, 'moderation/reported_spotteds.html', {
        'spotteds': spotteds,
    })


@user_passes_test(is_moderator)
def change_shifts(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = WorkHourFormSet(request.POST, instance=request.user.moderator)
        # check whether it's valid:
        if form.is_valid():
            # Aplly it
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Turnos atualizados!')
        else:
            return render(request, 'moderation/shifts.html', {'formset': form})

    # if a GET (or any other method) we'll create a blank form
    form = WorkHourFormSet(instance=request.user.moderator)
    return render(request, 'moderation/shifts.html', {'formset': form})


@user_passes_test(is_moderator)
def show_shifts(request):
    mods = Moderator.objects.all()
    return render(request, 'moderation/show_shifts.html', {'moderators': mods})


# Action Views

@user_passes_test(is_moderator)
def polemic_submit(request):
    instance = get_object_or_404(PendingSpotted, id=request.POST['id'])
    instance.polemic = True
    instance.save()
    return HttpResponse('Success')


@user_passes_test(is_moderator)
def approve_submit(request):
    instance = get_object_or_404(PendingSpotted, id=request.POST['id'])
    response = api_process_approved(instance)
    if not response:
        raise Http404
        return

    instance.post_spotted(request.user.moderator)
    return HttpResponse('Success')


@user_passes_test(is_moderator)
def reject_options(request):
    data = api_reject_options()
    return JsonResponse(data)


@user_passes_test(is_moderator)
def reject_submit(request):
    instance = get_object_or_404(PendingSpotted, id=request.POST['id'])
    response = api_process_rejected(instance, request.POST['option'])
    if not response:
        raise Http404
        return

    instance.delete()
    return HttpResponse('Success')


@user_passes_test(is_moderator)
def un_report_submit(request):
    instance = get_object_or_404(Spotted, id=request.POST['id'])
    instance.reported = ''
    instance.save()
    return HttpResponse('Success')


@user_passes_test(is_moderator)
def report_submit(request):
    instance = get_object_or_404(Spotted, id=request.POST['id'])
    response = api_process_deleted(instance, request.POST['option'], "reported")
    if not response:
        raise Http404
        return

    instance.remove_spotted(True)
    return HttpResponse('Success')