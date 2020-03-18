from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import POS
from .permissions import IsAuthenticatedOrReadOnly
from .serializers import POSSerializer, POSGetSerializer
from .pagination import CustomPagination


# class GetDeleteUpdateDevice(RetrieveUpdateDestroyAPIView):
#     serializer_class = POSSerializer
#     permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
#
#     def get_queryset(self):
#         try:
#             device = POS.objects.get(pk=self.kwargs.get('pk'))
#         except POS.DoesNotExist:
#             content = {
#                 'status': 'Not Found'
#             }
#             return Response(content, status=status.HTTP_404_NOT_FOUND)
#         return device
#
#     def get(self, request, *args, **kwargs):
#         device = self.get_queryset()
#         serializer = POSGetSerializer(device)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, *args, **kwargs):
#         device = self.get_queryset()
#         if request.user == device.owner:
#             serializer = DeviceSerializer(device, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             content = {
#                 'status': 'UNAUTHORIZED'
#             }
#             return Response(content, status=status.HTTP_401_UNAUTHORIZED)
#
#     def delete(self, request, *args, **kwargs):
#         device = self.get_queryset()
#         if request.user == device.owner:
#             device.delete()
#             content = {
#                 'status': 'NO CONTENT'
#             }
#             return Response(content, status=status.HTTP_204_NO_CONTENT)
#         else:
#             content = {
#                 'status': 'UNAUTHORIZED'
#             }
#             return Response(content, status=status.HTTP_401_UNAUTHORIZED)


class GetPostPOS(RetrieveUpdateDestroyAPIView):
    serializer_class = POSSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # pagination_class = CustomPagination

    def get_queryset(self):
        try:
            pos = POS.objects.get(p_id=self.kwargs.get('p_id'))
        except POS.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return pos

    def get(self, request, *args, **kwargs):
        pos = self.get_queryset()
        serializer = POSGetSerializer(pos)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # def post(self, request, *args, **kwargs):
    #     """
    #     Upload a device information
    #     """
    #     serializer = POSSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(owner=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
