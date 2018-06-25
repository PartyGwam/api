from rest_framework.authentication import TokenAuthentication


class PartyGwamAuthentication(TokenAuthentication):
    keyword = 'PG'
