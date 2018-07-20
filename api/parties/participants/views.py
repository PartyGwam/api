from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.parties.participants.serializers import ParticipantsSerializer
from apps.parties.models import Party

from api.utils import send_push_to_single_user


class ParticipantsAPIView(generics.CreateAPIView,
                          generics.RetrieveDestroyAPIView):

    queryset = Party.objects.all()
    lookup_field = 'slug'
    serializer_class = ParticipantsSerializer

    def get_object(self):
        instance = generics.get_object_or_404(
            self.get_queryset(),
            slug=self.kwargs['party_slug']
        )
        instance.update_party_info()
        return instance

    def _get_party_and_profile(self, request):
        instance = self.get_object()
        profile = request.user.profile
        return instance, profile

    def create(self, request, *args, **kwargs):
        instance, profile = self._get_party_and_profile(request)
        serializer = self.get_serializer(instance, partial=True)
        try:
            instance.add_participants(new_participant=profile)
            send_push_to_single_user(
                instance.party_owner,
                instance,
                '[파티에 누군가 참여함]',
                '[{}] 에 새 멤버가 참여했습니다.'.format(
                    instance.title
                )
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise ValidationError(detail=str(e))

    def destroy(self, request, *args, **kwargs):
        instance, profile = self._get_party_and_profile(request)
        try:
            instance.remove_participants(participant=profile)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            raise ValidationError(detail=str(e))
