from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import View
from django.utils.dateparse import parse_date

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.

class OrderFilterView(APIView):
    """
    View to list orders between a particular start and embargo date.
    """
 
    def get(self, request):
        """
        Handle GET request to list orders between start_date and embargo_date.
 
        Parameters:
            request : HttpRequest
                The HTTP request object containing start_date and embargo_date as query parameters.
 
        Returns:
            Response
                JSON response with the filtered orders or an error message.
        """
        start_date_str = request.query_params.get('start_date')
        embargo_date_str = request.query_params.get('embargo_date')
        if not start_date_str or not embargo_date_str:
            return Response(
                {"error": "Both start_date and embargo_date are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        start_date = parse_date(start_date_str)
        embargo_date = parse_date(embargo_date_str)
        if not start_date or not embargo_date:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )
        orders = Order.objects.filter(start_date__gte=start_date, embargo_date__lte=embargo_date)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

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
