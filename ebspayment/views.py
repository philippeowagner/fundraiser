# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.template import RequestContext

import base64
import re
import hashlib

from campaigns.models import Campaign
from ebspayment.forms import PaymentForm

#sample payment page
def ebspayment(request, campaign_id):
    campaign_obj = get_object_or_404(Campaign, pk=campaign_id)
    # hashstring = hashlib.md5(settings.EBS_ACCOUNT_ID+'|'+settings.EBS_SECRET_KEY).hexdigest()
    form = PaymentForm()

    # string = settings.EBS_SECRET_KEY+"|"+form.cleaned_data['account_id']+"|"
    #               +form.cleaned_data['amount']+"|"+form.cleaned_data['reference_no'] +"|"
    #               +form.cleaned_data['return_url']+"|"+form.cleaned_data['mode']
    string = settings.EBS_SECRET_KEY+"|"+'5880'+"|"+'1.00'+"|"+'223'+"|"+settings.EBS_RETURN_URL+"|"+"TEST"
    print string
    secure_hash = hashlib.md5(string).hexdigest()                 
    return render_to_response('ebspayment/payment_form.html', {'form': form,
                                                      'campaign' : campaign_obj,
                                                      'ebs_url': settings.EBS_ACTION_URL,
                                                      'secure_hash' : secure_hash},
                                                      context_instance=RequestContext(request))

#function to process response from EBS and decrypt
def ebsresponse(request):
    if request.method == 'GET':
	 formvalue = request.GET
         drvalue = formvalue.get('DR')
         dr = re.sub('\s','\+',drvalue) 
         data = base64.b64decode(dr)
         key = settings.EBS_SECRET_KEY
	 finalvalue = RC4(data, key)
	 params = []
         params = finalvalue.split('&')        
    	 paramdetail={}
    	 for param in params:
        	k, v = param.split('=')
        	paramdetail[k] = v
	 
    else:
	paramdetail={}	 	
    return render_to_response('ebspayment/response.html', {'response': paramdetail})

#RC4 Decryption function.Do Not edit it.
def RC4(data, key):
    x = 0 
    s = range(256)
    for i in range(256):
        x = (x + s[i] + ord(key[i % len(key)])) % 256 
        s[i], s[x] = s[x], s[i]
    x = y = 0 
    out = ""
    for c in data:
        x = (x + 1) % 256 
        y = (y + s[x]) % 256 
        s[x], s[y] = s[y], s[x]
        out += chr(ord(c) ^ s[(s[x] + s[y]) % 256])
    return out
#Do Not Edit upto this
