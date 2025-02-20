from django.shortcuts import render
from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer
    
    

class DeactivateOrderView(APIView):
    """
    View to deactivate an order by setting its is_active field to False.
    """
    def patch(self, request, *args, **kwargs):

        order_id = kwargs.get('id')
        order = get_object_or_404(Order, id=order_id)
        
        if not order.is_active:
            return Response(
                {"detail": "Order is already deactivated."},
                status=status.HTTP_400_BAD_REQUEST
            )
        

        order.is_active = False
        order.save()
        

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
