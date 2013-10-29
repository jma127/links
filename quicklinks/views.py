from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from quicklinks.models import Link
from django import forms
from datetime import datetime

class CreateLinkForm(forms.Form):
    url = forms.URLField(label="URL", max_length=1000, initial="https://www.google.com/")
    days = forms.IntegerField(min_value=0, max_value=365, initial=1)
    hours = forms.IntegerField(min_value=0, max_value=365*24, initial=0)
    minutes = forms.IntegerField(min_value=0, max_value=365*24*60, initial=0)

def index(request):
    twenty_recent = Link.objects.order_by('-created')[:20]
    context = {
        'links': twenty_recent,
        'create_form': CreateLinkForm(),
    }
    return render(request, 'quicklinks/index.html', context)

def create(request):
    if request.method == 'POST':
        form = CreateLinkForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            secs = form_data['days']
            secs = secs * 24 + form_data['hours']
            secs = secs * 60 + form_data['minutes']
            secs = secs * 60
            if secs > 365 * 24 * 3600 or secs < 60:
                return HttpResponse('Error: the expiration time cannot exceed one year and cannot be less than one minute.')
            form_url = form_data['url']
            link = Link()
            try:
                link = Link.objects.get(url=form_url)
                link.lifetime = max(secs, int(link.lifetime - (timezone.now() - link.created).total_seconds()))
            except ObjectDoesNotExist:
                link.url = form_url
                link.lifetime = secs
            link.save()
            full_url = request.build_absolute_uri(reverse('quicklinks:redirect', args=[link.pk]))
            context = {
                'link': link,
                'full_url': full_url,
            }
            return render(request, 'quicklinks/create.html', context)
        return HttpResponse('Error: submitted URL or expiry date was not valid.')
    raise Http404

def external_redirect(request, pageid):
    try:
        link = Link.objects.get(pk=pageid)
        return redirect(link.url)
    except ObjectDoesNotExist:
        raise Http404
