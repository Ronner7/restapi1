from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import viewsets, generics, request ,serializers
from .serializers import CarSerializer, RentalSerializer, UserSerializer, RentalCreateSerializer, RentalDeleteSerializer
from .models import Rental,Car,User
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CarDetailView(generics.RetrieveAPIView):
    queryset = Car.objects.all()  # You can customize this queryset based on your needs
    serializer_class = CarSerializer
    lookup_field = 'id'


class CarView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class BrandView(generics.ListAPIView):
    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.values('brand').distinct()


class BrandCarsView(generics.ListAPIView):
    serializer_class = CarSerializer

    def get_queryset(self):
        brand = self.kwargs['brand']
        queryset = Car.objects.filter(brand__iexact=brand)
        return queryset


class RentalCreate(generics.ListCreateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class CarDetailView(generics.ListAPIView):
    serializer_class = CarSerializer

    def get_queryset(self):
        car_id = self.kwargs['id']
        queryset = Car.objects.filter(pk=car_id)
        return queryset





class UserView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        user_id = user.id
        queryset = User.objects.filter(id=user_id)
        return queryset

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class RentalView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RentalSerializer

    def get_queryset(self):
        user = self.request.user
        user_id = user.id
        queryset = Rental.objects.filter(user_id=user_id)
        return queryset


class RentalDestroyView(generics.DestroyAPIView):
    serializer_class = RentalDeleteSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Rental.objects.all()
    lookup_field = 'pk'




