from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404, GenericAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework import viewsets, generics, request ,serializers,status
from .serializers import CarSerializer, RentalSerializer, UserSerializer, RentalCreateSerializer, RentalDeleteSerializer,ChangePasswordSerializer
from .models import Rental,Car
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CarDetailView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
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
    permission_classes = (IsAuthenticated,)

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


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
