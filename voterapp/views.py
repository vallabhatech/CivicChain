import requests
import random
from datetime import date
from django.shortcuts import render,redirect
from django.contrib import messages
from decouple import config
from .models import *
from adminapp.models import *
from decentralizedvoting.BlockcahinAlgo import HashDataBlock
import urllib.request
import urllib.parse

#send sms function
def sendSMS(user, otp, mobile):
    """Send an OTP only when an SMS provider is explicitly configured."""
    api_key = config("SMS_API_KEY", default="")
    if not api_key:
        return None
    data = urllib.parse.urlencode({
        "username": config("SMS_USERNAME", default=""),
        "apikey": api_key,
        "mobile": mobile,
        "message": f"Hello {user}, your OTP for account activation is {otp}.",
        "senderid": config("SMS_SENDER_ID", default="CODEBK"),
    }).encode("utf-8")
    request = urllib.request.Request(config("SMS_API_URL", default="https://smslogin.co/v3/api.php?"))
    with urllib.request.urlopen(request, data, timeout=10) as response:
        return response.read()


# Create your views here.
def voter_register(request,cand_id):
    candidate = CandidateModel.objects.get(pk=cand_id)
    election_obj = ElectionModel.objects.get(pk=candidate.election.id)

    if request.method == 'POST':
        phone = request.POST.get('phone')
        aadhar = request.POST.get('aadhar')

        otp = str(random.randint(1111, 9999))
        print(f"Generated OTP for testing: {otp}")

        voter, created = VoterModel.objects.get_or_create(aadhar=aadhar)
        if not created:
            if voter.phone != phone:
                messages.error(request, 'Please Enter Valid Mobile Number Associated with this Aadhar Number')
                return redirect('voter_voting',id=election_obj.id)

        voter.phone = phone
        voter.otp = otp
        voter.save()
        if voter in election_obj.voters.all():
            messages.error(request, "you have already submited your vote")
            return redirect('voter_voting',id=election_obj.id)


        # # SMS API CODE
        # url = "https://www.fast2sms.com/dev/bulkV2"
        # # create a dictionary
        # my_data = {'sender_id': 'FSTSMS', 
        #                 'message': 'Dear Voter For Aadhar No: '+str(voter.aadhar)+', Your OTP for Verification from DecentralizedVoting is '+ str(otp), 
        #                 'language': 'english', 
        #                 'route': 'q', 
        #                 'numbers':voter.phone,
        # }
            
        #     # create a dictionary
        # headers = {
        #         'authorization': "BHDFHdnBtRXSrBTvu6hYEHPoocj3TwmCk7hQlL1Y31AnHYwE78DWDpbtbV07",
        #         'Content-Type': "application/x-www-form-urlencoded",
        #         'Cache-Control': "no-cache"
        # }
        #     # make a post request
        # response = requests.request("POST",
        #                                 url,
        #                                 data = my_data,
        #                                 headers = headers)

        
        #calling sms function
        sendSMS(voter.aadhar, otp, voter.phone)
        messages.success(request, 'OTP generated. Configure SMS_API_KEY to deliver it by SMS.')
        return redirect('voter_otp',id=voter.id,cand_id=cand_id)


    return render(request, 'voter/voter-register.html')

def voter_otp(request,id,cand_id):
    voter = VoterModel.objects.get(pk=id)
    if request.method == 'POST':
        otp1 = request.POST.get('otp1')
        otp2 = request.POST.get('otp2')
        otp3 = request.POST.get('otp3')
        otp4 = request.POST.get('otp4')
        otp = otp1+otp2+otp3+otp4
        print(voter.otp,'org otp')
        print(otp,'entered otp')
        if otp == voter.otp:
            voter.status = "Verified"
            voter.otp = None
            voter.save()
            messages.success(request, 'OTP verification successful')
            return redirect('cast_vote',id,cand_id)
        else:
            messages.error(request, 'Incorrect OTP')
            return redirect('voter_otp',id,cand_id)
            
    return render(request, 'voter/voter-otp.html')

def voter_elections(request):
#   elections = ElectionModel.objects.filter(election_date__gte = date.today())
    elections = ElectionModel.objects.all()
    return render(request, 'voter/voter-elections.html',{
        'elections':elections
    })

def voter_results(request):
    elections = ElectionModel.objects.filter(election_date__lte = date.today())

    return render(request, 'voter/voter-results.html',{'elections':elections})

def voter_voting_page(request,id):
    election = ElectionModel.objects.get(pk=id)
#    if election.election_date != date.today():
#        messages.error(request, 'Voting has not started Yet')
#        return redirect('voter_elections')
    candidates = election.election_candidates.all()
    return render(request, 'voter/voter-voting-page.html',{
        'election':election,
        'candidates':candidates
    })

def cast_vote(request,id,cand_id):
    # voter_id = request.session["voter_id"]
    voter = VoterModel.objects.get(pk=id)
    candidate = CandidateModel.objects.get(pk=cand_id)
    election_obj = ElectionModel.objects.get(pk=candidate.election.id)
    
    if voter not in election_obj.voters.all():
        election_obj.voters.add(voter)
        candidate.voters.add(voter)
        candidate.votes += 1
        candidate.save()

        # Blockchain code for every vote
        key = config('BLOCKCHAIN_GENESIS_KEY')
        initial_block = HashDataBlock(key,[str(voter.aadhar),str(voter.phone),str(voter.id)])
        second_block = HashDataBlock(initial_block.block_hash,[str(candidate.candidate_name),str(candidate.party_name)])
        third_block = HashDataBlock(second_block.block_hash,[str(election_obj.election_name),str(election_obj.election_head)])
        
        VotesModel.objects.create(election=election_obj,candidate=candidate,voter=voter,
                                    voter_block = initial_block.block_hash,
                                    candidate_block = second_block.block_hash,
                                    election_block = third_block.block_hash)
        
        # Blockchain code for overal votes

        # Optional SMS provider integration can be enabled via environment variables.
        url = config('SMS_API_URL', default='')
                messages.success(request, 'Vote submitted sucessfully')
        return redirect('voter_elections')
    else:
        messages.error(request, "you have already submited your vote")
        return redirect('voter_voting',id=election_obj.id)

def voter_verify_results(request,id):
    election = ElectionModel.objects.get(pk=id)
    votes = VotesModel.objects.filter(election=election)
    total_votes = votes.count()
    
    verified = 0
    unverified = 0
    candidates = CandidateModel.objects.filter(election=election)
    winner = candidates.order_by('-votes')[0]
    print(winner.votes,'votesss')
    for i in votes:
        key = config('BLOCKCHAIN_GENESIS_KEY')
        voter = VoterModel.objects.get(pk=i.voter.pk)
        candidate = CandidateModel.objects.get(pk=i.candidate.pk)
        initial_block = HashDataBlock(key,[str(voter.aadhar),str(voter.phone),str(voter.id)])
        second_block = HashDataBlock(initial_block.block_hash,[str(candidate.candidate_name),str(candidate.party_name)])
        third_block = HashDataBlock(second_block.block_hash,[str(election.election_name),str(election.election_head)])

        if i.voter_block == initial_block.block_hash and \
            i.candidate_block == second_block.block_hash and \
            i.election_block == third_block.block_hash:
            verified+=1
            i.status = 'Valid'

        else:
            unverified+=1
            i.status = 'Invalid'

            
        
    return render(request, 'voter/voter-result-details.html',{
        'verified':verified,
        'unverified':unverified,
        'candidates':candidates,
        'total_votes':total_votes,
        'votes':votes,
        'winner':winner
        })
  