from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from otdjjangapi.models import OutfitArticle, UserArticle, Outfit
from .userarticle import UserArticleSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class OutfitArticleSerializer(serializers.ModelSerializer):
    user_article = UserArticleSerializer(many=False)

    class Meta:
        model = OutfitArticle
        fields = ["id", "outfit", "user_article"]


class OutfitArticles(ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        # Get the authenticated user
        user = request.user

        try:

            # Get all outfit articles for the authenticated user
            outfit_articles = OutfitArticle.objects.filter(user_article__user=user)

            # Serialize the Outfit articles
            serializer = OutfitArticleSerializer(
                outfit_articles, many=True, context={"request": request}
            )

            return Response(serializer.data)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            # Get the outfit articles associated with the outfit
            outfit_articles = OutfitArticle.objects.filter(outfit=pk)

            # Serialize the outfit articles
            serializer = OutfitArticleSerializer(outfit_articles, many=True)

            return Response(serializer.data)

        except OutfitArticle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def create(self, request):
        try:
            # Create a new outfit article
            outfit_article = OutfitArticle()
            outfit_article.outfit = Outfit.objects.get(pk=request.data["outfit_id"])
            outfit_article.user_article = UserArticle.objects.get(pk=request.data["user_article_id"])

            # Save the outfit article
            outfit_article.save()

            # Serialize the Outfit article
            serializer = OutfitArticleSerializer(outfit_article, context={"request": request})

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as key_error:
            return Response({"key error": str(key_error)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None):
        try:
            # Get the Outfit article by PK and for the authenticated Outfit
            outfit_article = OutfitArticle.objects.get(pk=pk)

            # Check permissions
            self.check_object_permissions(request, outfit_article)

            # Delete the Outfit article
            outfit_article.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except OutfitArticle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
