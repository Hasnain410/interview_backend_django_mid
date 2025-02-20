
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, OrdersByDateRangeView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('', OrderListCreateView.as_view(), name='order-list'),
    path('by-date/', OrdersByDateRangeView.as_view(), name='orders-by-date'),

]