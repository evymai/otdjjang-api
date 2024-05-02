from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.response import Response
from otdjjangapi.models import Size


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ["id", "size"]


class Sizes(ViewSet):

    def list(self, request):
        # get all Sizes
        sizes = Size.objects.all()
        serializer = SizeSerializer(sizes, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # get one Size by PK
        try:
            size = Size.objects.get(pk=pk)
            serializer = SizeSerializer(size, context={"request": request})
            return Response(serializer.data)

        except Size.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
