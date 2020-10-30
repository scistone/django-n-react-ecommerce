from django.shortcuts import render


from rest_framework.generics import ListAPIView,RetrieveAPIView,ListCreateAPIView,DestroyAPIView,RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import SessionAuthentication,BasicAuthentication

#our serializers
from api.collections.serializers import ListCollectionsAPIView,ListCollectionDetailAPIView

#models
from products.models import Collection, Product

class CollectionList(ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = ListCollectionsAPIView
    permission_classes = [AllowAny]

class addCollection(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ListCollectionsAPIView
    queryset = Collection.objects.all()

class deleteCollection(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ListCollectionsAPIView
    queryset = Collection.objects.all()
    lookup_field = 'slug'


@api_view(['GET'])
@permission_classes([AllowAny])
def CollectionDetailList(request,slug):
    try:
        category = Collection.objects.get(slug=slug)
        queryset = Product.objects.filter(category=category)
    except Collection.DoesNotExist:
        data            = {'detail':'Collection does not exist'}
        return Response(data)

    category = Collection.objects.filter(slug=slug)
    categorySerializer = ListCollectionsAPIView(category,many=True)
    productsSerializer = ListCollectionDetailAPIView(queryset,many=True)

    responsibleData = {}
    responsibleData['category'] =  categorySerializer.data
    responsibleData['products'] =  productsSerializer.data

    return Response(responsibleData)

# class CollectionDetailList(ListAPIView):
#     serializer_class = ListCollectionDetailAPIView
#     permission_classes = [AllowAny]
#     def get_queryset(self):
#         try:
#             category = Collection.objects.get(slug=self.kwargs['category'])
#             queryset = Product.objects.filter(category=category)
#         except Collection.DoesNotExist:
#             queryset = Product.objects.filter(pk=0)
#             return queryset
#         return queryset

        

        
        