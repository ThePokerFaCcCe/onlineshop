# from .models import Customer
# class CustomerMiddleware:
#     def __init__(self,get_response):
#         self.get_response = get_response
#     def __call__(self,req):
#         # Called before view
#         response = self.get_response(req)
#         return response
    
#     def process_request(self,req):
#         customer_data=None
#         if req.user.is_authenticated:
#             customer_data = Customer.objects.filter(user=req.user).first()
#             if not customer_data:
#                 customer_data = Customer.objects.create()
            