from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from django.views import View

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
 
class DeactivateOrderView(View):
    """
    A view to deactivate an order by setting its is_active field to False.
    """
    def post(self, request, pk):
        """
        Handles the POST request to deactivate an order.
 
        Parameters:
            request : HttpRequest
                The HTTP request object.
            pk : int
                The primary key of the order to deactivate.
 
        Returns:
            HttpResponseRedirect
                Redirects to the order list view or another specified URL after deactivating the order.
        """
        # Retrieve the order by its primary key
        order = get_object_or_404(Order, pk=pk)
        # Deactivate the order by setting is_active to False
        order.is_active = False
        order.save()
        # Redirect to a success page
        return redirect('order_list')

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer
