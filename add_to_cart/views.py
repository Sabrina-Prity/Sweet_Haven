from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from .models import AddToCart,Order
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from product.models import Mango
from .serializers import AddToCartSerializer, OrderSerializer
from rest_framework.decorators import action
from .models import IsAdminUser
from rest_framework.permissions import IsAuthenticated
# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect




class AddToCartViewSet(viewsets.ModelViewSet):
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AddToCart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        mango = get_object_or_404(Mango, id=request.data.get('mango'))
        quantity = request.data.get('quantity', 1)

        if quantity > mango.available_quantity:
            return Response(
                {"detail": f"Requested quantity exceeds available stock. Available: {mango.available_quantity}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item, created = AddToCart.objects.get_or_create(user=request.user, mango=mango)
        if not created:
            if cart_item.quantity + quantity <= mango.available_quantity:
                cart_item.quantity += quantity
            else:
                return Response(
                    {"detail": f"Requested quantity exceeds available stock. Available: {mango.available_quantity - cart_item.quantity}."})
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)




class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            product_id = request.data.get('product')
            quantity = request.data.get('quantity', 1)

            try:
                mango = Mango.objects.get(id=product_id)

                quantity = int(quantity)
                
                if mango.quantity >= quantity:
                    mango.quantity -= quantity
                    mango.save()

                    total_amount = mango.price*quantity
                    # Send the confirmation email
                    email_subject = "Order Confirmation"
                    email_body = render_to_string(
                        'order_pending_email.html',
                        {'user': request.user, 'product': mango.name, 'quantity': quantity, 'total_amount': total_amount}
                    )

                    email = EmailMultiAlternatives(
                        email_subject, '', to=[request.user.email]
                    )
                    email.attach_alternative(email_body, "text/html")
                    email.send()

                    # Create the order
                    order = serializer.save()
                    return Response({"message": "Order placed successfully. A confirmation email has been sent."})
                else:
                    return Response(
                        {"error": f"Not enough stock available. Only {mango.quantity} items left."},
                        status=400
                    )

            except Mango.DoesNotExist:
                return Response({"error": "Product not found."})
        else:
            return Response(serializer.errors)




class AdminOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        new_status = request.data.get('buying_status')
        if new_status == 'Completed':
            email_subject = "Your Order has been Completed"
            email_body = render_to_string(
                'purchase_completed_email.html',
                {
                    'user': order.user,
                    'product': order.product.name,
                    'quantity': order.quantity,
                }
            )
            email = EmailMultiAlternatives(
                email_subject, '', to=[order.user.email]
            )
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response({"message": "A confirmation email has been sent."})

        return Response(serializer.data)


class OrderHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        orders = self.get_queryset()
        order_data = [
            {
                'product': order.product.name,
                'quantity': order.quantity,
                'status': order.buying_status,
                'purchased_at': order.purchased_at,
            }
            for order in orders
        ]
        return Response({"orders": order_data})