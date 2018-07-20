from rest_framework import viewsets
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from api.parties.pagination import PartyAPIPagination
from api.parties.permissions import PartyAPIPermission
from api.parties.serializers import \
    PartySerializer, PartyCreateSerializer, PartyUpdateSerializer
from apps.parties.models import Party

from api.utils import send_push_to_multiple_user


class PartyAPIViewSet(viewsets.ModelViewSet):
    lookup_field = 'party_slug'
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
        queryset = Party.objects.all()
        for instance in queryset:
            instance.update_party_info()
        return queryset

    def get_object(self):
        instance = get_object_or_404(
            self.get_queryset(),
            slug=self.kwargs['party_slug']
        )
        self.check_object_permissions(self.request, instance)
        return instance

    def get_serializer_class(self):
        return self.SERIALIZERS[self.request.method]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        send_push_to_multiple_user(
            [participant for participant in instance.participants.all()],
            instance,
            '[파티 정보 수정됨]',
            '[{}] 의 정보가 수정되었습니다.'.format(
                instance.title
            )
        )
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
