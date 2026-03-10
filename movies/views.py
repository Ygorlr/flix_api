from django.db.models import Count, Avg
from rest_framework import generics, views, response, status
from rest_framework.permissions import IsAuthenticated
from movies.models import Movie
from movies.serializers import MovieSerializer, MovieStatsSerializer, MovieListDetailSerializer
from app.permissions import GlobalDefaultPermission
from reviews.models import Review


class MovieCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Movie.objects.all()
    # serializer_class = MovieSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieListDetailSerializer
        return MovieSerializer


class MovieRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Movie.objects.all()
    # serializer_class = MovieSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieListDetailSerializer
        return MovieSerializer

class MovieStatsView(views.APIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Movie.objects.all()

    def get(self, request):
        # Buscar todos os dados
        total_movies = self.queryset.count()
        movies_by_genre = self.queryset.values('genre__name').annotate(count=Count('id'))
        total_reviews = Review.objects.count()
        average_stats = Review.objects.aggregate(avg_stars=Avg('stars'))['avg_stars']
        # Montar resposta
        # Devolve resposta pro user com estatísticas
        data = {
            'total_movies': total_movies,
            'movies_by_genre': movies_by_genre,
            'total_reviews': total_reviews,
            'average_stars': round(average_stats, 1) if average_stats else 0,
        }
        serializer = MovieStatsSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return response.Response(data=serializer.validated_data, status=status.HTTP_200_OK)
        '''return response.Response(data={
            'total_movies': total_movies,
            'movies_by_genre': movies_by_genre,
            'total_reviews': total_reviews,
            'average_stars': round(average_stats, 1) if average_stats else 0,
        }, status=status.HTTP_200_OK,)'''
