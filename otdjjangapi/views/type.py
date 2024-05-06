from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from otdjjangapi.models import Type


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ["id", "name"]


class Types(ViewSet):

    def list(self, request):
        try:
            # get all types
            types = Type.objects.all()
            serializer = TypeSerializer(types, many=True, context={"request": request})
            return Response(serializer.data)
        
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, pk=None):
        # get one type by PK
        try:
            type = Type.objects.get(pk=pk)
            serializer = TypeSerializer(type, context={"request": request})
            return Response(serializer.data)

        except Type.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
