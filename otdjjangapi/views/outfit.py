from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from otdjjangapi.models import Outfit
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class OutfitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outfit
        fields = ["id", "name", "user"]


class Outfits(ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        user = request.user

        try:
            # get all outfits
            outfits = Outfit.objects.filter(user=user)
            serializer = OutfitSerializer(
                outfits, many=True, context={"request": request}
            )
            return Response(serializer.data)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        user = request.user

        # get one Outfit by PK
        try:
            outfit = Outfit.objects.get(user=user, pk=pk)
            serializer = OutfitSerializer(outfit, context={"request": request})
            return Response(serializer.data)

        except Outfit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            user = request.user

            # Create a new Outfit
            new_outfit = Outfit()
            new_outfit.name = request.data["name"]
            new_outfit.user = user

            new_outfit.save()

            serializer = OutfitSerializer(new_outfit, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self, request, pk=None):
        try:
            outfit = Outfit.objects.get(pk=pk)
            self.check_object_permissions(request, outfit)
            outfit.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Outfit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
