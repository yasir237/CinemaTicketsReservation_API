from django.http import Http404
from django.shortcuts import render
from django.http.response import JsonResponse
from tickets.models import Movie, Guest, Reservation, Post
from rest_framework.decorators import api_view
from rest_framework import status
from tickets.serializers import MovieSerializer, GuestSerializer, ReservationSerializer, PostSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets, filters

from rest_framework.authentication import BaseAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAuthorOrReadOnly

# from database but without rest
def no_rest_from_model(request):

    data = Guest.objects.all()


    response = {
        'guests': list(data.values('name', 'mobile')),
    }

    return JsonResponse(response) 


# 3 FBV Function based views

# 3.1 GET POST
@api_view(['GET', 'POST'])
def FBV_List(request):
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializers = GuestSerializer(guests, many=True)
        return Response(serializers.data)

    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():      
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def FBV_pk (request, pk):  
    
    try:
        # Get the guest by primary key
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# CVB Class based views
# 4.1 List and Create == GET POST

class CBV_List(APIView):

    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 4.2 GET PUT and DELETE class based views -- pk

class CBV_pk(APIView):

    def get_object(self, pk):
        try:
           # Get the guest by primary key
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
             raise Http404
    
    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    
    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 5. Mixins
# 5.1 mixins list

class mixins_list( mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)


# 5.1 get put delete
class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)
    
    def put(self, request,pk):
        return self.update(request, pk=pk)
    
    def delete(self, request, pk):
        return self.destroy(request, pk=pk)
    

# 6. Generics
# 6.1 get and post
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]

# 6.2 get put delete
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]

# 7 viewsets

class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']
    

class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


# 8 Find movie
@api_view(['GET'])
def find_movie(request):
    hall = request.query_params.get('hall')
    movie = request.query_params.get('movie')

    movies = Movie.objects.filter(
        hall=hall,
        movie=movie
    )

    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


# 9 create new reservation
@api_view(['POST'])
def create_new_reservation(request):
    movie = Movie.objects.get(
        hall = request.query_params.get('hall'),
        movie = request.query_params.get('movie')
    )

    guest = Guest()
    guest.name = request.query_params.get('name')
    guest.mobile = request.query_params.get('mobile')
    guest.save()


    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()


    return Response(status=status.HTTP_201_CREATED)



# 10 post author editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer