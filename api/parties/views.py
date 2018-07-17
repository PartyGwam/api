from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from api.parties.pagination import PartyAPIPagination
from api.parties.permissions import PartyAPIPermission
from api.parties.serializers import \
    PartySerializer, PartyCreateSerializer, PartyUpdateSerializer
from apps.parties.models import Party


class PartyAPIViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.filter(has_started=False)
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

    def get_queryset(self):
        queryset = super(PartyAPIViewSet, self).get_queryset()
        for instance in queryset:
            instance.update_party_info()
        return queryset

    def get_object(self):
        instance = super(PartyAPIViewSet, self).get_object()
        instance.update_party_info()
        return instance

    def get_serializer_class(self):
        return self.SERIALIZERS[self.request.method]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            raise ValidationError(detail=str(e))
        except Exception as e:
            raise APIException(detail=str(e))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
            return Response(serializer.data)
        except ValueError as e:
            raise ValidationError(detail=str(e))
        except Exception as e:
            raise APIException(detail=str(e))


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
