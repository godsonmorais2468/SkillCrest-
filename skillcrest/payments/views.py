import razorpay
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from decouple import config
from django.http import HttpResponseForbidden
from courses.models import Course
from .models import CoursePurchase
from django.contrib import messages


#  Create Razorpay Order
class CreateOrderView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('login')

        course = get_object_or_404(Course, pk=pk)

        #  Trainer cannot purchase their own course
        if course.trainer == request.user:
            messages.error(request, "You are the trainer of this course. You cannot purchase your own course.")
            return redirect('course-detail', pk=course.pk)


        #  Prevent duplicate purchase
        if CoursePurchase.objects.filter(user=request.user, course=course, is_paid=True).exists():
            return redirect('course-lessons', pk=pk)

        amount = 49900  # ₹499 in paise

        client = razorpay.Client(auth=(
            config('RZP_CLIENT_ID'),
            config('RZP_CLIENT_SECRET')
        ))

        payment = client.order.create({
            'amount': amount,
            'currency': 'INR',
            'payment_capture': 1
        })

        purchase, _ = CoursePurchase.objects.get_or_create(
            user=request.user,
            course=course,
        )

        purchase.razorpay_order_id = payment['id']
        purchase.amount = amount
        purchase.save()

        context = {
            'course': course,
            'order_id': payment['id'],
            'razorpay_key': config('RZP_CLIENT_ID'),
            'amount': amount,
        }

        return render(request, 'payments/payment-page.html', context)



#  Verify Razorpay Payment
@method_decorator(csrf_exempt, name='dispatch')
class VerifyPaymentView(View):
    def post(self, request):
        client = razorpay.Client(auth=(
            config('RZP_CLIENT_ID'),
            config('RZP_CLIENT_SECRET')
        ))

        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            purchase = CoursePurchase.objects.get(razorpay_order_id=order_id)
            purchase.razorpay_payment_id = payment_id
            purchase.razorpay_signature = signature
            purchase.is_paid = True
            purchase.save()

            # After successful payment go to lessons
            return redirect('course-lessons', pk=purchase.course.id)

        except Exception as e:
            print("Payment Verification Failed:", e)
            return render(request, 'payments/payment-failed.html')
