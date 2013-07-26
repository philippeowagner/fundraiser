from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views import generic

from people.models import Beneficiary
from campaigns.models import Campaign
from campaigns.forms import CampaignForm


@login_required
def create_a_campaign(request):
    if request.user.beneficiary.is_approved:
        form = CampaignForm()
        if request.method == 'POST':
            form = CampaignForm(request.POST)
            if form.is_valid():
                beneficiary = Beneficiary.objects.get(user=request.user)
                cam_obj = Campaign.objects.create(beneficiary=beneficiary,
                                                  campaign_name=request.POST['campaign_name'],
                                                  target_amount=request.POST['target_amount'],
                                                  cause=request.POST['cause'])
                if request.POST.getlist('books'):
                    for m2m in request.POST.getlist('books'):
                        cam_obj.books.add(m2m)
                return HttpResponseRedirect(reverse('campaigns:list_of_campaigns'))

        return render_to_response('campaigns/create_a_campaign.html', {'form': form, 'errors': dict(form.errors.viewitems())}, context_instance=RequestContext(request))
    else:
        return render_to_response('campaigns/campaign_unapproved.html', context_instance=RequestContext(request))



class CampaignDetail(generic.DetailView):
    model = Campaign
    template_name = 'campaigns/campaign_detail.html'
    context_object_name = 'campaign'


class CampaignsListView(generic.ListView):
    template_name = 'campaigns/campaigns.html'
    context_object_name = 'campaign_list'

    def get_queryset(self):
        return Campaign.objects.all()
