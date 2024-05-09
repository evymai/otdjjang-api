from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from datetime import datetime
from otdjjangapi.models import OutfitPhoto, Outfit

class OutfitPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutfitPhoto
        fields = ["id", "outfit", "worn_on", "image"]


class OutfitPhotos(ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        try:
            # get all OutfitPhotos
            outfitPhotos = OutfitPhoto.objects.all()
            serializer = OutfitPhotoSerializer(
                outfitPhotos, many=True, context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        # get one OutfitPhoto by PK
        try:
            outfitPhoto = OutfitPhoto.objects.get(outfit=pk)
            serializer = OutfitPhotoSerializer(outfitPhoto, context={"request": request})
            return Response(serializer.data)

        except OutfitPhoto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        user = request.user
        try:
            # Create a new OutfitPhoto
            new_outfitPhoto = OutfitPhoto()
            new_outfitPhoto.outfit = Outfit.objects.get(pk=request.data["outfit_id"])
            new_outfitPhoto.image = request.FILES["image"]
            new_outfitPhoto.worn_on = datetime.now() 

            new_outfitPhoto.save()

            serializer = OutfitPhotoSerializer(new_outfitPhoto, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk=None):
        try:
            outfitPhoto = OutfitPhoto.objects.get(pk=pk)
            self.check_object_permissions(request, outfitPhoto)
            outfitPhoto.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except OutfitPhoto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
