from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.parties.owner.permissions import IsPartyOwner
from api.parties.owner.serializers import \
    PartyOwnerSerializer, PartyOwnerPassSerializer
from apps.parties.models import Party


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
            self.perform_update(serializer)
            return Response(PartyOwnerSerializer(instance).data)
        except Exception as e:
            raise ValidationError(detail=str(e))
