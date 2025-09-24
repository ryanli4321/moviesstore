from django.db import models

from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint

User = settings.AUTH_USER_MODEL

class Petition(models.Model):
    title       = models.CharField(max_length=120)
    movie_title = models.CharField(max_length=120)
    description = models.TextField(max_length=1000, blank=True)
    proposer    = models.ForeignKey(User, null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name='petitions')
    created_at  = models.DateTimeField(auto_now_add=True)
    is_open     = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.movie_title} (#{self.pk})"

    @property
    def score(self):
        agg = self.votes.aggregate(s=models.Sum('value'))
        return agg['s'] or 0

class PetitionVote(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='votes')
    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petition_votes')
    value    = models.SmallIntegerField(choices=((1, 'Upvote'), (-1, 'Downvote')))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['petition', 'user'], name='unique_vote_per_user')
        ]

    def __str__(self):
        return f"{self.user} -> {self.petition} ({self.value})"
