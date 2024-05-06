from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from otdjjangapi.models import Size


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ["id", "size"]


class Sizes(ViewSet):

    def list(self, request):
        try: 
            # get all Sizes
            sizes = Size.objects.all()
            serializer = SizeSerializer(sizes, many=True, context={"request": request})
            return Response(serializer.data)
        
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, pk=None):
        # get one Size by PK
        try:
            size = Size.objects.get(pk=pk)
            serializer = SizeSerializer(size, context={"request": request})
            return Response(serializer.data)

        except Size.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
