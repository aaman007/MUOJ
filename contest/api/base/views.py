from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from contest.api.base.serializers import ApplyRatingSerializer
from contest.models import Contest
from contest.tasks import task_apply_contest_rating
from core.api.base.permissions import IsObjectOwner


class ApplyRatingGenericAPIView(GenericAPIView):
    serializer_class = ApplyRatingSerializer
    permission_classes = [IsAuthenticated, IsObjectOwner]

    def get_object(self):
        contest = get_object_or_404(Contest,  pk=self.request.data.get('contest_id'))
        self.check_object_permissions(self.request, contest.author)
        return contest

    def post(self, request, *args, **kwargs):
        contest = self.get_object()

        if contest.state != 'Finished':
            return Response({
                'detail': 'Contest has not ended yet!'
            }, status=status.HTTP_400_BAD_REQUEST)

        elif not contest.is_rated:
            return Response({
                'detail': 'Contest is not rated!'
            }, status=status.HTTP_400_BAD_REQUEST)

        elif contest.rating_applied:
            return Response({
                'detail': 'Ratings already applied for this contest'
            }, status=status.HTTP_400_BAD_REQUEST)

        elif not len(contest.standings):
            return Response({
                'detail': 'No one participated in this contest!'
            }, status=status.HTTP_400_BAD_REQUEST)

        task_apply_contest_rating.delay(contest.id)
        Contest.objects.filter(id=contest.id).update(rating_applied=True)
        return Response(data={'detail': 'Ratings Will be applied soon!'}, status=status.HTTP_200_OK)
