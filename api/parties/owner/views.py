from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.parties.owner.permissions import IsPartyOwner
from api.parties.owner.serializers import \
    PartyOwnerSerializer, PartyOwnerPassSerializer
from apps.parties.models import Party

from api.utils import send_push_to_single_user


class PartyOwnerAPIView(generics.RetrieveUpdateAPIView):
    queryset = Party.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsPartyOwner]

    def get_object(self):
        instance = generics.get_object_or_404(
            self.get_queryset(),
            slug=self.kwargs['party_slug']
        )
        instance.update_party_info()
        self.check_object_permissions(self.request, instance)
        return instance

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PartyOwnerSerializer
        else:
            return PartyOwnerPassSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        try:
            instance = serializer.save()
            send_push_to_single_user(
                instance.party_owner,
                instance,
                '[방장 위임됨]',
                '[{}] 의 방장을 위임받았습니다.'.format(
                    instance.title
                )
            )
            return Response(PartyOwnerSerializer(instance).data)
        except ValueError as e:
            raise ValidationError(detail=str(e))
