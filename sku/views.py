from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from pos.pagination import CustomPagination
from .models import SKU
# from .permissions import IsOwnerOrReadOnly, IsAuthenticated
from .permissions import IsAuthenticatedOrReadOnly
from .serializers import SKUSerializer, SKUGetSerializer


class GetSKUList(ListAPIView):
    serializer_class = SKUSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        sku_list = SKU.objects.filter(owner=request.user).order_by('s_id')
        paginate_queryset = self.paginate_queryset(sku_list)
        serializer = SKUGetSerializer(paginate_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Upload a SKU information
        """
        serializer = SKUSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
