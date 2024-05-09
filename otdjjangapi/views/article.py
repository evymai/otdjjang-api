from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from otdjjangapi.models import Article, Brand, Type
from .brand import BrandSerializer
from .type import TypeSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ArticleSerializer(serializers.ModelSerializer):

    brand = BrandSerializer(many=False)
    type = TypeSerializer(many=False)

    class Meta:
        model = Article
        fields = ["id", "name", "brand", "type", "image", "creator"]


class ArticleUpdateSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all())
    creator = serializers.ReadOnlyField(source="creator.id")

    class Meta:
        model = Article
        fields = ["id", "name", "brand", "type", "creator"]


class Articles(ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        try:
            # get all articles
            articles = Article.objects.all()
            serializer = ArticleSerializer(
                articles, many=True, context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        # get one article by PK
        try:
            article = Article.objects.get(pk=pk)
            serializer = ArticleSerializer(article, context={"request": request})
            return Response(serializer.data)

        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        user = request.user
        try:
            # Create a new article
            new_article = Article()
            new_article.name = request.data["name"]
            new_article.brand = Brand.objects.get(pk=request.data["brand_id"])
            new_article.type = Type.objects.get(pk=request.data["type_id"])
            new_article.image = request.FILES["image"]
            new_article.creator = user
            new_article.save()

            serializer = ArticleSerializer(new_article, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Brand.DoesNotExist:
            return Response(
                {"message": "Brand does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        except Type.DoesNotExist:
            return Response(
                {"message": "Type does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, pk=None):
        try:
            article = Article.objects.get(pk=pk)
            self.check_object_permissions(request, Article)

            serializer = ArticleUpdateSerializer(article, data=request.data)
            if serializer.is_valid():
                article.name = request.data["name"]
                article.brand_id = request.data["brand"]
                article.type_id = request.data["type"]

                article.save()

                serializer.save()
                return Response(serializer.data, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            article = Article.objects.get(pk=pk)
            self.check_object_permissions(request, article)
            article.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
