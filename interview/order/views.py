from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.utils.dateparse import parse_date

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer
    
    
class OrdersByDateRangeView(APIView):
    """
    GET endpoint to list orders between a given start_date and embargo_date.
    
    Expects query parameters:
      - start_date: string in 'YYYY-MM-DD' format
      - embargo_date: string in 'YYYY-MM-DD' format
    """
    def get(self, request: Request, *args, **kwargs) -> Response:
        start_date_str = request.query_params.get('start_date')
        embargo_date_str = request.query_params.get('embargo_date')
        
        if not start_date_str or not embargo_date_str:
            return Response(
                {'error': "Both 'start_date' and 'embargo_date' query parameters are required."},
                status=400
            )
        
        start_date = parse_date(start_date_str)
        embargo_date = parse_date(embargo_date_str)
        
        if not start_date or not embargo_date:
            return Response(
                {'error': "Invalid date format. Please use 'YYYY-MM-DD'."},
                status=400
            )
        
        orders = Order.objects.filter(start_date__gte=start_date, embargo_date__lte=embargo_date)
        
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=200)

