from django.conf.urls import patterns, url

from campaigns.views import create_a_campaign, CampaignDetail, CampaignsListView, CampaignUpdate


urlpatterns = patterns('',
    url(r'^$', CampaignsListView.as_view(), name='list_of_campaigns'),
    url(r'^create_a_campaign/$',create_a_campaign, name='create_a_campaign'),
    url(r'^campaign_detail/(?P<pk>\d+)/$',CampaignDetail.as_view(), name='campaign_detail'),
    url(r'^campaign/edit/(?P<pk>\d+)/$',CampaignUpdate.as_view(), name='edit_campaign'),    
    )
