from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from decentralizedvoting.BlockcahinAlgo import HashDataBlock

# Create your views here.
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin':
            messages.success(request, 'Login Successful')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid Login Credentials')
            return redirect('admin_login')
    return render(request, 'main/admin-login.html')

def admin_dashboard(request):
    elections = ElectionModel.objects.all().count()
    candidates = CandidateModel.objects.all().count()
    votes = VotesModel.objects.all().count()
    return render(request, 'admin/admin-dashboard.html',{
        'elections':elections,
        'candidates':candidates,
        'votes':votes
    })

def admin_add_election(request):
    if request.method == 'POST':
        election_name = request.POST.get('electionname')
        head_of_election = request.POST.get('headofelection')
        election_picture = request.FILES['electionpicture']
        election_date = request.POST.get('electiondate')
        constituency = request.POST.get('constituency')
        area = request.POST.get('electionarea')
        address = request.POST.get('electionaddress')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        print(election_name,head_of_election,election_picture,election_date,constituency,area,
                address,city,state,zip)
        ElectionModel.objects.create(election_name=election_name,election_head=head_of_election,
                                    election_date=election_date,election_picture=election_picture,constituency=constituency,
                                    area=area,address=address,state=state,city=city,zip=zip)
        messages.success(request, 'Election has been added successfully')
        return redirect('admin_add_election')
    return render(request, 'admin/admin-addelection.html')

def admin_add_candidates(request):
    elections = ElectionModel.objects.all()
    if request.method == 'POST':
        candidate_name = request.POST.get('candidatename')
        party_name = request.POST.get('partyname')
        election_id = request.POST.get('electionname')
        symbol = request.FILES['symbol']
        election  = ElectionModel.objects.get(pk=election_id)
        CandidateModel.objects.create(election=election,candidate_name=candidate_name,party_name=party_name,symbol=symbol)
        election.candidates_count +=1
        election.save()
        messages.success(request, 'Candidate added successful')
        return redirect('admin_add_candidates')
    return render(request, 'admin/admin-addcandidates.html',{
        'elections':elections
    })



def admin_view_elections(request):
    elections = ElectionModel.objects.all()

    return render(request, 'admin/admin-view-elections.html',{
        'elections':elections
    })


def admin_view_candidates(request,id):
    election = ElectionModel.objects.get(pk=id)
    candidates = election.election_candidates.all()
    return render(request, 'admin/admin-view-candidates.html',{
        'candidates':candidates,
        'election':election
    })


def admin_results(request):
    elections = ElectionModel.objects.all()
    return render(request, 'admin/admin-results.html',{
        'elections':elections
    })

def verify_results(request,id):
    election = ElectionModel.objects.get(pk=id)
    votes = VotesModel.objects.filter(election=election).order_by('-id')
    total_votes = votes.count()
    
    verified = 0
    unverified = 0
    candidates = CandidateModel.objects.filter(election=election)
    for i in votes:
        key = 'dk84dfao63o94wsghl3o14'
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

            
        
    return render(request, 'admin/admin-result-details.html',{
        'verified':verified,
        'unverified':unverified,
        'candidates':candidates,
        'total_votes':total_votes,
        'votes':votes
    })
