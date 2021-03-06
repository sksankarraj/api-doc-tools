"""
REST API views for reading and writing to the edX Hedgehog Database.

Documented using edx_api_doc_tools.

TODO: also give an example of documenting "traditional" (non-ViewSet) DRF views.
"""
from __future__ import absolute_import, unicode_literals

from rest_framework.exceptions import APIException, NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from edx_api_doc_tools import (
    exclude_schema,
    exclude_schema_for,
    exclude_schema_for_all,
    path_parameter,
    query_parameter,
    schema,
    schema_for,
)

from .data import get_hedgehogs
from .serializers import HedgehogSerializer


HEDGEHOG_KEY_PARAMETER = path_parameter(
    'hedgehog_key', str, "Key identifying the hog. Lowercase letters only."
)
HEDGEHOG_404_RESPONSE = {
    404: 'Hedgehog with given key not found.',
}
HEDGEHOG_ERROR_RESPONSES = {
    401: 'Not authenticated',
    403: 'Operation not permitted.',
    **HEDGEHOG_404_RESPONSE
}


@schema_for(
    'list',
    """
    Fetch the list of edX hedgehogs.

    Hedgehogs can be filtered by minimum weight (grams or ounces),
    their favorite food, whether they graduated college,
    or any combination of those criterion.
    """,
    parameters=[
        query_parameter('min-grams', int, "Filter on whether minimum weight (grams)."),
        query_parameter('min-ounces', float, "Filter hogs by minimum weight (ounces)."),
        query_parameter('fav-food', str, "Filter hogs by favorite food."),
        query_parameter('graduated', bool, "Filter hogs by whether they graudated."),
    ],
    responses=HEDGEHOG_404_RESPONSE,
)
@schema_for(
    'retrieve',
    """
    Fetch details for a _single_ hedgehog by key.
    """,
    parameters=[HEDGEHOG_KEY_PARAMETER],
    responses=HEDGEHOG_404_RESPONSE,
)
@schema_for(
    'create',
    """
    Create a new hedgehog.

    If successful, an absolute URI for the hedgehog is returned in the
    'Location' HTTP response header.
    """,
    parameters=[HEDGEHOG_KEY_PARAMETER],
    responses=HEDGEHOG_ERROR_RESPONSES,
)
# The next line will exclude the PUT and PATCH endpoints from the API docs.
@exclude_schema_for('update', 'partial_update')
@schema_for(
    'destroy',
    """
    Wipe a hedgehog from the database.
    """,
    parameters=[HEDGEHOG_KEY_PARAMETER],
    responses={
        204: 'Hedgehog successfully removed.',
        **HEDGEHOG_ERROR_RESPONSES,
    },
)
class HedgehogViewSet(ModelViewSet):
    """
    A viewset for hedgehogs.

    Supports listing, retrieval, creation, partial-update, and full-update of
    hedgehogs.
    """
    serializer_class = HedgehogSerializer
    lookup_field = 'hedgehog_key'

    def get_queryset(self):
        """
        Return iterable of hedgehog data items.
        """
        return get_hedgehogs()

    def get_object(self):
        """
        Fetch a specific hedgehog by their key.
        """
        hedgehog_key = self.kwargs[self.lookup_field]
        try:
            hedgehog = next(
                hog for hog in self.get_queryset()
                if hog.key == hedgehog_key
            )
        except StopIteration:
            raise NotFound()
        return hedgehog

    def perform_create(self, serializer):
        """
        Create a Hedeghog; result of a POST (Unimplemented).
        """
        raise EndpointNotImplemented()

    def perform_update(self, serializer):
        """
        Update a Hedeghog; result of a PUT (Unimplemented).
        """
        raise EndpointNotImplemented()

    def perform_destroy(self, instance):
        """
        Destroy a Hedeghog; result of a DELETE (Unimplemented).
        """
        raise EndpointNotImplemented()


@exclude_schema_for_all
class HedgehogUndocumentedViewset(ViewSet):
    """
    A view that allows us to retrieve something.

    For whatever reason, we don't want it showing up on the API docs page.
    """
    def retrieve(self, request):
        """
        Retrieve something or other.
        """
        raise EndpointNotImplemented()


class HedgehogInfoView(GenericAPIView):
    """Information about the API."""

    @schema()
    def get(self, request):
        """
        Get information about the Hedgehog API.

        Returns a object with keys and values describing the API.

        Args:
            request: a Request.

        """
        raise EndpointNotImplemented()

    def put(self, request):
        """
        Not really an endpoint at all, but has no @schema decorator.

        This is to show the difference in treatment.  This is a second
        paragraph which will be included in the docs.

        Args:
            request: a Request.

        """
        raise EndpointNotImplemented()

    @exclude_schema
    def patch(self, request):
        """
        Update information about the Hedgehog API.

        Internal-only; this endpoint is not exposed in the docs.
        """
        raise EndpointNotImplemented()


@exclude_schema_for_all
class HedgehogUndocumentedView(GenericAPIView):
    """
    A view that allows us to GET something.

    For whatever reason, we don't want it showing up on the API docs page.
    """
    def get(self, request):
        """
        Get something or other.
        """
        raise EndpointNotImplemented()


class EndpointNotImplemented(APIException):
    """
    Exception that, when raised, triggers a 501 response.
    """
    status_code = 501
    default_detail = 'This example endpoint is not implemented.'
    default_code = 'not_implemented'
