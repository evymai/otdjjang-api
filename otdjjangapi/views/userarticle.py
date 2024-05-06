from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from otdjjangapi.models import UserArticle, Article, Size
from .article import ArticleSerializer
from .size import SizeSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class UserArticleSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(many=False)
    size = SizeSerializer(many=False)

    class Meta:
        model = UserArticle
        fields = ["id", "user", "article", "size"]


class UserArticles(ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        # Get the authenticated user
        user = request.user

        try:
            # Get all user articles for the authenticated user
            user_articles = UserArticle.objects.filter(user=user)

            # Serialize the user articles
            serializer = UserArticleSerializer(
                user_articles, many=True, context={"request": request}
            )

            return Response(serializer.data)

        except Exception as ex:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        # Get the authenticated user
        user = request.user

        try:
            # Get the user article by PK and for the authenticated user
            user_article = UserArticle.objects.get(user=user, pk=pk)

            # Serialize the user article
            serializer = UserArticleSerializer(
                user_article, context={"request": request}
            )

            return Response(serializer.data)

        except UserArticle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            # Get the authenticated user
            user = request.user

            # Create a new user article
            user_article = UserArticle()
            user_article.user = user
            user_article.article = Article.objects.get(pk=request.data["article_id"])
            user_article.size = Size.objects.get(pk=request.data["size_id"])

            # Save the user article
            user_article.save()

            # Serialize the user article
            serializer = UserArticleSerializer(
                user_article, context={"request": request}
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response(
                {"message": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk=None):
        # Get the authenticated user
        user = request.user

        try:
            # Get the user article by PK and for the authenticated user
            user_article = UserArticle.objects.get(user=user, pk=pk)

            # Check permissions
            self.check_object_permissions(request, user_article)

            # Delete the user article
            user_article.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except UserArticle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
