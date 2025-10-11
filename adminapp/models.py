from django.db import models

# Create your models here.
class VoterModel(models.Model):
    phone = models.CharField(max_length=20,null=True)
    aadhar = models.CharField(max_length=50,null=True)
    otp= models.CharField(max_length=5,null=True)
    status = models.CharField(max_length=20,default='Pending')

    class Meta:
        db_table = 'voters_details'

class ElectionModel(models.Model):
    election_name = models.CharField(max_length=100)
    election_head = models.CharField(max_length=100)
    election_date = models.DateField()
    election_picture = models.ImageField(upload_to='images/')
    constituency = models.CharField(max_length=100)
    area = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)
    voters = models.ManyToManyField(VoterModel)
    candidates_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'elction_detials'


class CandidateModel(models.Model):
    election = models.ForeignKey(ElectionModel,on_delete=models.CASCADE,related_name='election_candidates')
    candidate_name=models.CharField(max_length=100)
    party_name=models.CharField(max_length=100)
    symbol=models.ImageField(upload_to='symbols/')
    voters = models.ManyToManyField(VoterModel,related_name='voted_voters')
    votes = models.IntegerField(default=0)

    class Meta:
        db_table = 'candidate_details'


class VotesModel(models.Model):
    election = models.ForeignKey(ElectionModel,
                                on_delete=models.SET_NULL,
                                related_name='election_votes',
                                null=True)
    candidate = models.ForeignKey(CandidateModel,
                                on_delete=models.SET_NULL,
                                related_name='candidates_votes',
                                null=True)
    voter = models.ForeignKey(VoterModel
                                ,on_delete=models.SET_NULL,
                                related_name='voter_voted_list',
                                null=True)
    voter_block = models.CharField(max_length=100)
    candidate_block = models.CharField(max_length=100)
    election_block = models.CharField(max_length=100)

    class Meta:
        db_table = 'votes'