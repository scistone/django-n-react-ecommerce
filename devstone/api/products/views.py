from django.shortcuts import render


from rest_framework.generics import ListAPIView,RetrieveAPIView,ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
#our serializers
from api.products.serializers import ListProductsAPIView,ListProductDetailAPIView, ListProductMediaAPIView,ListProductTagAPIView

#models
from products.models import Collection, Product, ProductDetail, ProductMedia , Tag

class addProduct(ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ListProductsAPIView
    queryset = Product.objects.all()

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def addProductDetail(request,pk):
    if request.method == 'GET':
        try:
            xproduct        = Product.objects.filter(id=pk)
            product         = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            data            = {'detail':'Parent Product does not exist'}
            return Response(data)

        productDetail       = ProductDetail.objects.filter(product=product)

        productSeri         = ListProductsAPIView(xproduct,many=True)
        productDetailSeri   = ListProductDetailAPIView(productDetail,many=True)

        responsibleData = {}
        responsibleData['product']  = productSeri.data
        responsibleData['variants'] = productDetailSeri.data

        return Response(responsibleData)

    if request.method == 'POST':
        try:
            parentProduct   = Product.objects.get(id=request.data['product'])
            parentProduct   = Product.objects.filter(id=request.data['product'])
        except Product.DoesNotExist:
            data            = {'detail':'Parent product does not exist'}
            return Response(data)

        productSerializer = ListProductDetailAPIView(data=request.data)

        if productSerializer.is_valid():
            productSerializer.save()
            try:
                xproduct        = Product.objects.filter(id=pk)
                product         = Product.objects.get(id=pk)
            except Product.DoesNotExist:
                data            = {'detail':'Parent Product does not exist'}
                return Response(data)

            productDetail       = ProductDetail.objects.filter(product=product)

            productSeri         = ListProductsAPIView(xproduct,many=True)
            productDetailSeri   = ListProductDetailAPIView(productDetail,many=True)

            responsibleData = {}
            responsibleData['message']  = "Product's Detail succesfully created."
            responsibleData['product']  = productSeri.data
            responsibleData['variants'] = productDetailSeri.data

            return Response(responsibleData)
        else:
            data            = {'detail':'error'}
            return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def productDetail(request,pk):
    try:
        xproduct        = Product.objects.filter(id=pk)
        product         = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        data            = {'detail':'Product does not exist'}
        return Response(data)

    productDetail       = ProductDetail.objects.filter(product=product)

    productSeri         = ListProductsAPIView(xproduct,many=True)
    productDetailSeri   = ListProductDetailAPIView(productDetail,many=True)

    responsibleData = {}
    responsibleData['product'] = productSeri.data
    responsibleData['variants'] = productDetailSeri.data

    return Response(responsibleData)



class ProductList(ListAPIView):
    queryset = Product.objects.all()
    permission_classes = [AllowAny]

    serializer_class = ListProductsAPIView

class ProductsTagList(ListAPIView):
    queryset = Tag.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ListProductTagAPIView


class ProductDetailList(ListAPIView):
    # queryset = ProductDetail.objects.all()
    serializer_class = ListProductDetailAPIView
    permission_classes = [AllowAny]
    # lookup_field = "pk"
    def get_queryset(self):
        try:
            product = Product.objects.get(slug=self.kwargs['slug'])
            queryset = ProductDetail.objects.filter(product=product)
        except Product.DoesNotExist:
            queryset = ProductDetail.objects.filter(pk=0)
            return queryset
        return queryset

class ProductMediaList(ListAPIView):
    serializer_class = ListProductMediaAPIView
    permission_classes = [AllowAny]
    def get_queryset(self):
        try:
            product = Product.objects.get(slug=self.kwargs['slug'])
            queryset = ProductMedia.objects.filter(product=product)
        except Product.DoesNotExist:
            queryset = ProductMedia.objects.filter(pk=0)
            return queryset
        return queryset

class ProductTagList(ListAPIView):
    serializer_class = ListProductTagAPIView
    permission_classes = [AllowAny]
    def get_queryset(self):
        try:
            product = Product.objects.get(slug=self.kwargs['slug'])
            queryset = Tag.objects.filter(product=product)
        except Product.DoesNotExist:
            queryset = Tag.objects.filter(pk=0)
            return queryset
        return queryset