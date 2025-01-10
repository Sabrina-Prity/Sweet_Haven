from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from .models import AddToCart,Order
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from product.models import Mango
from .serializers import AddToCartSerializer, OrderSerializer
from rest_framework.decorators import action
from .models import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from .models import Cart
# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status  # for HTTP status codes

class CartApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = serializers.CartSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cart Created"}, status=status.HTTP_201_CREATED)
        else:
            # Return validation errors if the serializer is not valid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, format=None):
        objects = Cart.objects.all()
        print(objects)
        serializer = serializers.CartSerializer(objects, many=True)
        return Response(serializer.data)


class CartDetails(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        print("Pk" ,pk)
        object = Cart.objects.get(user = pk)
        print(object)
        serializer = serializers.CartSerializer(object)
        return Response(serializer.data)

    
class ProductGetCartID(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        object = AddToCart.objects.all()
        # print(object)
        serializer = serializers.AddToCartSerializer(object, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = serializers.CartItemsUpdateSerializer(data=request.data)

        if serializer.is_valid():
            product = Mango.objects.get(pk=request.data['mango'])
            if product.quantity > 0:
                # Decrement the product quantity
                product.quantity -= int(request.data['quantity'])
                product.save()

                # Check if the cart item already exists
                cart_item = AddToCart.objects.filter(cart=request.data['cart'], mango=request.data['mango']).first()

                if cart_item:  # If the item exists in the cart
                    cart_item.quantity += int(request.data['quantity'])
                    cart_item.price += int(request.data['quantity']) * int(product.price)
                    print("Cart Item:", cart_item)
                    cart_item.save()
                    return Response('Product updated')

                # If the cart item does not exist, create a new one
                ans = serializer.save()
                ans.price = int(request.data['quantity']) * int(product.price)
                ans.save()
                return Response('Product Cart Added')
            else:
                return Response('Product Empty!')
        else:
            return Response(serializer.errors)


    
class CartProductsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, cart_id, format=None):
            cart = Cart.objects.get(id=cart_id)
            cart_items = AddToCart.objects.filter(cart=cart)
            
            serializer = serializers.AddToCartSerializer(cart_items, many=True)
            return Response(serializer.data, status=200)
         
class CartItemsUpdate(APIView):
    
    permission_classes = [IsAuthenticated]
        
    def get(self,request,pk,format=None):
            obj = AddToCart.objects.get(pk=pk)
            serializer = AddToCartSerializer(obj)
            return Response(serializer.data)
        
        
    def delete(self, request, pk, format=None):
        obj = AddToCart.objects.get(pk=pk)
        cart_id = obj.cart.id  
        obj.delete()

        cart_items = AddToCart.objects.filter(cart=cart_id)
        updated_cart_items = serializers.AddToCartSerializer(cart_items, many=True).data

        return Response({"cart_items": updated_cart_items})


# class AddToCartViewSet(viewsets.ModelViewSet):
#     serializer_class = AddToCartSerializer
#     permission_classes = [IsAuthenticated]  
#     def get_queryset(self):
#         return AddToCart.objects.filter(cart__id=self.kwargs.get('pk'), user=self.request.user)

#     def create(self, request, *args, **kwargs):

#         cart_id = self.kwargs.get('pk')

#         if not cart_id:
#             return Response({"detail": "Cart ID is required."}, status=status.HTTP_400_BAD_REQUEST)

#         cart = get_object_or_404(Cart, id=cart_id, user=request.user)

#         mango_id = request.data.get('mango')
#         if not mango_id:
#             return Response({"detail": "Mango ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
#         mango = get_object_or_404(Mango, id=mango_id)
#         print("Mango:", mango)

#         quantity = request.data.get('quantity', 1)
#         quantity = int(quantity)

#         if quantity > mango.quantity:
#             return Response(
#                 {"detail": f"Requested quantity exceeds available stock. Available: {mango.quantity}."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         cart_item, created = AddToCart.objects.get_or_create(cart=cart, mango=mango, user=request.user)

#         if not created:
#             if cart_item.quantity + quantity <= mango.quantity:
#                 cart_item.quantity += quantity
#             else:
#                 return Response(
#                     {"detail": f"Requested quantity exceeds available stock. Available: {mango.quantity - cart_item.quantity}."},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
        
#         # Ensure the user field is set to the current user (either when creating or updating)
#         cart_item.user = request.user
#         cart_item.save()

#         serializer = serializers.AddToCartSerializer(cart_item)
#         return Response(serializer.data)




class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    def get_queryset(self):
        print(f"User ID: {self.request.user.id}")  
        print(f"User ID: {self.request.user}")  
        return Order.objects.filter(user=self.request.user.id)
        # object = Order.objects.filter(user=self.request.user)
        # print("Object", object)
        # serializer = self.serializer_class(object, many=True)
        # return Response(serializer.data)
    
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

                    total_amount = mango.price * quantity
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

                    # Assign the current user to the order
                    order = serializer.save(user=request.user)
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




    

class UserOrdersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        # print("User", request.user)
        param = self.request.query_params.get('user_id')
        # print("Params", param)
        # params = request.data.get.query_params()
        object = Order.objects.filter(user = param)
        serializer = serializers.OrderGetSerializer(object, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated."}, status=401)

        try:
            quantity = int(request.data.get('quantity'))
        except (ValueError, TypeError):
            return Response({"error": "Invalid quantity. Must be an integer."}, status=400)

        try:
            product_id = int(request.data.get('product'))
        except (ValueError, TypeError):
            return Response({"error": "Invalid product ID. Must be an integer."}, status=400)

        serializer = serializers.OrderSerializer(data={
            'quantity': quantity,
            'buying_status': request.data.get('buying_status'),
            'user': request.data.get('user'),
            'product': product_id
        })

        if serializer.is_valid():
            try:
                product = Mango.objects.get(pk=product_id)
            except Mango.DoesNotExist:
                return Response({"error": "Product not found."}, status=404)

            if not hasattr(product, 'quantity') or product.quantity is None:
                return Response({"error": "Invalid product quantity."}, status=400)

            total_amount = product.price * quantity
            
            if product.quantity >= quantity:
                product.quantity -= quantity
                product.save()
            else:
                return Response({"error": "Not enough stock available."}, status=400)

            email_subject = "Order Confirmation"
            email_body = render_to_string(
                'order_pending_email.html',
                {
                    'user': request.user,
                    'product': product.name,
                    'quantity': quantity,
                    'total_amount': total_amount
                }
            )
            
            if hasattr(request.user, 'email'):
                email = EmailMultiAlternatives(
                    email_subject, '', to=[request.user.email]
                )
                email.attach_alternative(email_body, "text/html")
                email.send()

            # Save the order
            serializer.save()
            return Response({"message": "Post Successful", "order": serializer.data})
        else:
            print("Errors:", serializer.errors)
            return Response({"error": "Invalid data", "details": serializer.errors}, status=400)
    
  


class UserSpecificOrderView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated."}, status=401)
        
        user_id = request.user.id  
        
        try:
            order = Order.objects.get(pk=pk, user_id=user_id)
            serializer = serializers.OrderGetSerializer(order)
            return Response(serializer.data)

        except Order.DoesNotExist:
            return Response({"error": "Order not found for this user."}, status=404)

    def delete(self, request, pk, format=None):
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated."}, status=401)
        
        user_id = request.user.id 
        
        try:
            order = Order.objects.get(pk=pk, user_id=user_id)
            order.delete()

            updated_orders = Order.objects.filter(user_id=user_id)
            serializer = serializers.OrderGetSerializer(updated_orders, many=True)
            return Response({
                "message": "Order deleted successfully.",
                "updated_orders": serializer.data
            })

        except Order.DoesNotExist:
            return Response({"error": "Order not found for this user."}, status=404)
     


class AdminOrderAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serializer = serializers.OrderGetSerializer(orders, many=True)
        return Response(serializer.data)


    def get_order(self, order_id):
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None
        

class AdminOrderUpdateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        order = self.get_order(kwargs['pk'])
        if not order:
            return Response({"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.OrderGetSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            new_status = request.data.get('buying_status')

            if new_status == 'Completed':
                self.send_order_completion_email(order)  
                return Response({"message": "Order updated to 'Completed' and email sent."})

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
    def delete(self, request, *args, **kwargs):
        order = self.get_order(kwargs['pk'])
        if not order:
            return Response({"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response({"message": "Order deleted successfully."})

    def get_order(self, order_id):
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    def send_order_completion_email(self, order):
        email_subject = "Your Order has been Completed"
        email_body = render_to_string(
            'purchase_completed_email.html',
            {
                'user': order.user,
                'product': order.product.name,
                'quantity': order.quantity,
            }
        )
        user_email = EmailMultiAlternatives(
            email_subject, '', to=[order.user.email]
        )
        user_email.attach_alternative(email_body, "text/html")
        user_email.send()

        



class OrderHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]

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