from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.response import Response
from otdjjangapi.models import Brand
from rest_framework import status


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name"]


class Brands(ViewSet):

    def list(self, request):
        try:
            # Get all brands
            brands = Brand.objects.all()
            serializer = BrandSerializer(
                brands, many=True, context={"request": request}
            )
            return Response(serializer.data)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        # Get one brand by PK
        try:
            brand = Brand.objects.get(pk=pk)
            serializer = BrandSerializer(brand, context={"request": request})
            return Response(serializer.data)

        except Brand.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            # Extracting brand name from request data
            name = request.data.get("name")

            # Creating and saving instance of brand
            brand = Brand.objects.create(name=name)

            serializer = BrandSerializer(brand, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response(
                {"message": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk=None):
        try:
            brand = Brand.objects.get(pk=pk)
            self.check_object_permissions(request, brand)
            brand.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Brand.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
