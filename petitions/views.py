from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PetitionForm
from .models import Petition, PetitionVote

def petition_list(request):
    qs = Petition.objects.all().select_related('proposer')
    petitions = sorted(qs, key=lambda p: p.score, reverse=True)
    return render(request, 'petitions/list.html', {'petitions': petitions})

def petition_detail(request, pk):
    p = get_object_or_404(Petition, pk=pk)
    user_vote = None
    if request.user.is_authenticated:
        user_vote = PetitionVote.objects.filter(petition=p, user=request.user).first()
    return render(request, 'petitions/detail.html', {'p': p, 'user_vote': user_vote})

@login_required
def petition_create(request):
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.proposer = request.user
            pet.save()
            messages.success(request, 'Petition created!')
            return redirect('petitions:detail', pk=pet.pk)
    else:
        form = PetitionForm()
    return render(request, 'petitions/create.html', {'form': form})

@login_required
@require_POST
def petition_vote(request, pk):
    p = get_object_or_404(Petition, pk=pk, is_open=True)
    value = 1 if request.POST.get('value') == 'up' else -1
    try:
        with transaction.atomic():
            vote, created = PetitionVote.objects.select_for_update().get_or_create(
                petition=p, user=request.user, defaults={'value': value}
            )
            if not created:
                vote.value = value
                vote.save()
        messages.success(request, 'Your vote was recorded.')
    except IntegrityError:
        messages.error(request, 'Cannot record your vote. Please try again.')
    return redirect('petitions:detail', pk=p.pk)
