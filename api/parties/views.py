from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from api.parties.pagination import PartyAPIPagination
from api.parties.permissions import PartyAPIPermission
from api.parties.serializers import \
    PartySerializer, PartyCreateSerializer, PartyUpdateSerializer
from apps.parties.models import Party


class PartyAPIViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    lookup_field = 'slug'
    pagination_class = PartyAPIPagination
    permission_classes = [PartyAPIPermission]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['start_time', 'created_at']

    SERIALIZERS = {
        'GET': PartySerializer,
        'POST': PartyCreateSerializer,
        'PUT': PartyUpdateSerializer,
        'PATCH': PartyUpdateSerializer,
    }

    def get_serializer_class(self):
        return self.SERIALIZERS[self.request.method]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise ValidationError(detail=str(e))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class JoinedPartyAPIView(ListAPIView):
    serializer_class = PartySerializer
    pagination_class = PartyAPIPagination

    def get_queryset(self):
        return Party.objects.filter(participants=self.request.user.profile)


class CreatedPartyAPIView(ListAPIView):
    serializer_class = PartySerializer
    pagination_class = PartyAPIPagination

    def get_queryset(self):
        return Party.objects.filter(party_owner=self.request.user.profile)
