from cmath import exp
from django import http
import random
import razorpay
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from gk.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
import os
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from random import randint
from django.shortcuts import render
from .models import Order
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import redirect
from .models import Newslatter, Product 


from .models import *



def home(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if email:  # check empty
            # check if email already exists
            if not Newslatter.objects.filter(email=email).exists():
                Newslatter.objects.create(email=email)

                subject = "Thanku for Subscribing!"
                message = "You have successfully subscribed to our newslatter 😊"

                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently = False,
                )

        return redirect("/")  

    products = Product.objects.all().order_by('-id')  # better than reverse slicing

    return render(request, "index.html", {"Products": products})

def shop(request,mc,sc,br):
    if(request.method=="POST"):
        search = request.POST.get("search")
        products = Product.objects.filter(Q(name__icontains=search)) 

    else:

        if(mc == "All" and sc == "All" and br == "All"):
            products = Product.objects.all()
        elif(mc != "All" and sc == "All" and br == "All"):
            products = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc))
        elif(mc == "All" and sc != "All" and br == "All"):
            products = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc))
        elif(mc == "All" and sc == "All" and br != "All"):
            products = Product.objects.filter(brand=Brand.objects.get(name=br))
        elif(mc != "All" and sc != "All" and br == "All"):
            products = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc), subcategory=Subcategory.objects.get(name=sc))
        elif(mc != "All" and sc == "All" and br != "All"):
            products = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc), brand=Brand.objects.get(name=br))
        elif(mc == "All" and sc != "All" and br != "All"):
            products = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc), brand=Brand.objects.get(name=br))
        elif(mc != "All" and sc != "All" and br != "All"):
            products = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc), subcategory=Subcategory.objects.get(name=sc), brand=Brand.objects.get(name=br))

    products = products[::-1]
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brand = Brand.objects.all()
    return render(request,"shop.html",{"Products":products,
                                        "Maincategory":maincategory,
                                        "Subcategory":subcategory,
                                        "Brand":brand,
                                        "MC":mc,
                                        "SC":sc,
                                        "BR":br,
                                    })

def singleProduct(request,id):
    p = Product.objects.get(id=id)
    return render(request,"single-product.html",{"Product":p})


def login(request):
    if(request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if(user is not None):
            auth.login(request,user)
            return HttpResponseRedirect("/profile")
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect("/login")
    return render(request, "login.html")

def signup(request):
    if(request.method=="POST"):
        type = request.POST.get("actype")
        if(type=="seller"):
            s = Seller()
            s.name = request.POST.get("name")
            s.username = request.POST.get("username")
            s.email = request.POST.get("email")
            s.phone = request.POST.get("phone")
            password = request.POST.get("password")
            cpassword = request.POST.get("cpassword")
            if(password==cpassword):
                try:
                    user = User.objects.create_user(username = s.username, password = password, email = s.email)
                    user.save()
                    s.save()
                    subject = 'Your Account has Been Created Successfully!!!!'
                    message = """
                            Thanks to create account in our site 
                            Now you can sell Products with us
                            Visit for lattest product and offers                         
                            http://localhost:8000/
                            Team : Eshop.com  
                            
                            """
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [user.email, ]
                    send_mail( subject, message, email_from, recipient_list )
                    return HttpResponseRedirect("/login")
                except:
                    messages.error(request,"User Name already Taken")

            else:
                messages.error(request,"Password and Confirm PAssword Does not Match")
        else:
            #pass
            b = Buyer()
            b.name = request.POST.get("name")
            b.username = request.POST.get("username")
            b.email = request.POST.get("email")
            b.phone = request.POST.get("phone")
            password = request.POST.get("password")
            cpassword = request.POST.get("cpassword")
            if(password==cpassword):
                try:
                    user = User.objects.create_user(username = b.username, password = password, email = b.email)
                    user.save()
                    b.save()
                    subject = 'Your Account has Been Created Successfully!!!!'
                    message = """
                            Thanks to create account in our site 
                            Now you can Buy Products from us
                            Visit for lattest product and offers                         
                            http://localhost:8000/
                            Team : Eshop.com  
                            
                            """
                    return HttpResponseRedirect("/login")
                except:
                    messages.error(request,"User Name already Taken")

            else:
                messages.error(request,"Password and Confirm PAssword Does not Match")
    return render(request,"signup.html")

@login_required(login_url="/login/")
def profilePage(request):
    try:
        user = User.objects.get(username = request.user)
        if(user.is_superuser):
            return HttpResponseRedirect("/admin")
        else:
            try:
                seller = Seller.objects.get(username = request.user)
                products = Product.objects.filter(seller=seller)
               
                return render(request,"sellerprofile.html",{"User":seller,
                                                            "Products":products
                                                            })
            except:
                buyer = Buyer.objects.get(username = request.user)
                wishlist = Wishlist.objects.filter(user = buyer)
                orders = Checkout.objects.filter(buyer=buyer)
                return render(request,"buyerProfile.html",{"User":buyer,
                                                           "Wishlist":wishlist,
                                                           "Orders":orders,
                                                           })
    except:
        return HttpResponseRedirect("/login")
    

@login_required(login_url="/login/")
def updateSellerProfile(request):
    try:
        seller = Seller.objects.get(username=request.user)
        if(request.method == "POST"):
            seller.name = request.POST.get("name")
            seller.email = request.POST.get("email")
            seller.phone = request.POST.get("phone")
            seller.addressline1 = request.POST.get("addressline1")
            seller.addressline2 = request.POST.get("addressline2")
            seller.addressline3 = request.POST.get("addressline3")
            seller.city = request.POST.get("city")
            seller.state = request.POST.get("state")
            seller.pin = request.POST.get("pin")
            if(request.FILES.get("pic")):
                if(seller.pic):
                    os.remove("media/"+str(seller.pic))
                seller.pic = request.FILES.get("pic")
            seller.save()
            return HttpResponseRedirect("/profile")
        return render(request, "update-profile.html", {"User": seller})
    except:
        try:
            buyer = Buyer.objects.get(username=request.user)
            if(request.method == "POST"):
                buyer.name = request.POST.get("name")
                buyer.email = request.POST.get("email")
                buyer.phone = request.POST.get("phone")
                buyer.addressline1 = request.POST.get("addressline1")
                buyer.addressline2 = request.POST.get("addressline2")
                buyer.addressline3 = request.POST.get("addressline3")
                buyer.city = request.POST.get("city")
                buyer.state = request.POST.get("state")
                buyer.pin = request.POST.get("pin")
                if(request.FILES.get("pic")):
                    if(buyer.pic):
                        os.remove("media/"+str(buyer.pic))
                    buyer.pic = request.FILES.get("pic")
                buyer.save()
                return HttpResponseRedirect("/profile")
            return render(request, "update-profile.html", {"User": buyer})
        except:
            return HttpResponseRedirect("/admin")


@login_required(login_url="/login/")
def addProduct(request):
    try:
        seller = Seller.objects.get(username = request.user)
        maincat = Maincategory.objects.all()
        subcat = Subcategory.objects.all()
        brand = Brand.objects.all()
        if(request.method=="POST"):
            p = Product()
            p.name = request.POST.get('name')
            p.maincategory = Maincategory.objects.get(name=request.POST.get('maincategory'))
            p.subcategory = Subcategory.objects.get(name=request.POST.get('subcategory'))
            p.brand = Brand.objects.get(name=request.POST.get('brand'))
            p.basePrice = int(request.POST.get('baseprice'))
            p.discount = int(request.POST.get('discount'))
            p.finalPrice = p.basePrice-p.basePrice*p.discount/100
            p.color = request.POST.get('color')
            p.size = request.POST.get('size')
            p.stock = request.POST.get('stock')
            p.description = request.POST.get('description')
            p.pic1 = request.FILES.get('pic1')
            p.pic2 = request.FILES.get('pic2')
            p.pic3 = request.FILES.get('pic3')
            p.pic4 = request.FILES.get('pic4')
            p.seller = seller
            p.save()
            subject = 'Checkout Our Latest Products : Eshop.com'
            message = ''''
                        Hey User!!!!
                        Checkout our latest Products with Best Discount
                        http://localhost:8000//singleProduct/%d/
                        Team : Eshop.com  
                        
                        '''%p.id
            email_from = settings.EMAIL_HOST_USER
            subscribers = Newslatter.objects.all()
            #for i in subscribers:
            recipient_list = subscribers
            send_mail( subject, message, email_from, recipient_list )
            return HttpResponseRedirect("/profile/")
        return render(request, "add-product.html", {
                                    "MainCat": maincat,
                                    "SubCat": subcat,
                                    "Brand": brand,
                                })
    except:
      return HttpResponseRedirect("/profile")


@login_required(login_url="/login/")
def deleteProduct(request,id):
    try:
        seller = Seller.objects.get(username = request.user)
        p = Product.objects.get(id=id)
        if(p.seller==seller):
            p.delete()
        return HttpResponseRedirect("/profile")
    except:
        return HttpResponseRedirect("/profile")


@login_required(login_url="/login/")
def updateProduct(request, id):
    try:
        seller = Seller.objects.get(username=request.user)
        p = Product.objects.get(id=id)
        if(p.seller == seller):
            if(request.method == "POST"):
                p.name = request.POST.get('name')
                p.maincategory = Maincategory.objects.get(name=request.POST.get('maincategory'))
                p.subcategory = Subcategory.objects.get(name=request.POST.get('subcategory'))
                p.brand = Brand.objects.get(name=request.POST.get('brand'))
                p.basePrice = int(request.POST.get('baseprice'))
                p.discount = int(request.POST.get('discount'))
                p.finalPrice = p.basePrice-p.basePrice*p.discount/100
                p.color = request.POST.get('color')
                p.size = request.POST.get('size')
                p.stock = request.POST.get('stock')
                p.description = request.POST.get('description')
                if(request.FILES.get("pic1") == ""):
                    if(p.pic1):
                        os.remove("media/"+str(p.pic1))
                    p.pic1 = request.FILES.get('pic1')

                if(request.FILES.get("pic2") == ""):
                    if(p.pic2):
                        os.remove("media/"+str(p.pic2))
                    p.pic2 = request.FILES.get('pic2')

                if(request.FILES.get("pic3") == ""):
                    if(p.pic3):
                        os.remove("media/"+str(p.pic3))
                    p.pic3 = request.FILES.get('pic3')

                if(request.FILES.get("pic4") == ""):
                    if(p.pic4):
                        os.remove("media/"+str(p.pic4))
                    p.pic4 = request.FILES.get('pic4')
                p.save()
                return HttpResponseRedirect("/profile")
            else:
                maincat = Maincategory.objects.exclude(name=p.maincategory)
                subcat = Subcategory.objects.exclude(name=p.subcategory)
                brand = Brand.objects.exclude(name=p.brand)
                return render(request, "update-product.html", {"Product": p,
                                                               "MainCat": maincat,
                                                               "SubCat": subcat,
                                                               "Brand": brand,
                                                               })
        return HttpResponseRedirect("/profile")
    except:
        return HttpResponseRedirect("/profile")


@login_required(login_url="/login/")
def addToWishlist(request,id):
    try:
        user = Buyer.objects.get(username = request.user)
        wishlist = Wishlist.objects.filter(user=user)
        flag = False
        for i in wishlist:
            if(id==i.product.id):
                flag = True
                break
        if(flag==False):
            wish = Wishlist()
            p = Product.objects.get(id=id)
            wish.user = user
            wish.product = p
            wish.save()
        return HttpResponseRedirect("/profile/")
         
    except:
       return HttpResponseRedirect("/profile/")


@login_required(login_url="/login/")
def deleteWishlist(request,id):
    try:
        user = Buyer.objects.get(username = request.user)
        w = Wishlist.objects.get(id=id)
        if(w.user==user):
            w.delete()
        return HttpResponseRedirect("/profile")
    except:
        return HttpResponseRedirect("/profile")




@login_required(login_url="/login/")
def addToCart(request,id):
    id = str(id)
    try:
        #user = Buyer.objects.get(username = request.user)
        cart = request.session.get("cart",None)
        
        try:
            user = Buyer.objects.get(username = request.user)
            p = Product.objects.get(id=id)
            wish = Wishlist.objects.get(product=p,user=user)
            wish.delete()
        except:
            pass
        if(cart):

            if(str(id) in cart):
                q = cart[id]
                cart[id] = q+1
            else:
                cart.setdefault(id,1)
            request.session["cart"]=cart
            request.session.set_expiry(60*60*24*30)
        else:
            cart={id:1}
            request.session["cart"]=cart
            request.session.set_expiry(60*60*24*30)
        return HttpResponseRedirect("/cart/")
         
    except: 
        return HttpResponseRedirect("/profile/")

@login_required(login_url='/login/')
def cartPage(request):
    cart = request.session.get("cart", None)
    products = []
    total = 0
    shipping = 0
    final = 0
    if(cart):
        for key, value in cart.items():
            p = Product.objects.get(id=key)
            products.append(p)
            total = total+p.finalPrice*value
            if(total < 1000 and len(cart.keys())):
                shipping = 150
            final = total+shipping
    return render(request, "cart.html", {"Products": products,
                                         "Total": total,
                                         "Shipping": shipping,
                                         "Final": final,
                                         })


@login_required(login_url="/login/")
def removeFromCart(request,id):
    try:
       cart = request.session.get("cart",None)
       if(cart):
        cart.pop(str(id))
        request.session["cart"]=cart
        return HttpResponseRedirect("/cart/")
    except:
        return HttpResponseRedirect("/profile")
        

@login_required(login_url="/login/")
def updateCart(request,num,id):
    try:
       cart = request.session.get("cart",None)
       if(cart):
        q = cart[str(id)]
        if(num==1 ):
            if(q>1):
                cart[str(id)] = q-1
        else:
            cart[str(id)] = q+1
        request.session["cart"]=cart
        return HttpResponseRedirect("/cart/")
    except:
        return HttpResponseRedirect("/profile")



#client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
@login_required(login_url="/login/")
def checkoutPage(request):
    try:
        buyer = Buyer.objects.get(username = request.user)
        cart = request.session.get("cart",None)
        products = []
        total = 0
        shipping = 0
        final = 0
        for key,value in cart.items():
            p = Product.objects.get(id=key)
            products.append(p)
            total = total+p.finalPrice*value
        if(total<1000 and len(cart.keys())):
            shipping = 150
        final = total+shipping
        if(request.method=="POST"):
            check = Checkout()
            check.buyer = buyer
            check.total=total
            check.shipping=shipping
            check.final = final
            check.save()
            for key in cart.keys():
                cp = CheckoutProducts()
                p = Product.objects.get(id=key)
                cp.productid = int(key)
                cp.q = cart[key]
                cp.total = cart[key]*p.finalPrice
                cp.checkout=check
                cp.save()
            user_email = request.user.email
            if user_email:
                try:
                    send_mail(
                        "ORder Confirmed 🎉",
                        f"Hello {request.user.username},\n\nYour order has been placed successfully.\nTotal Amount: ₹{final}",
                        settings.EMAIL_HOST_USER,
                        [user_email],
                        fail_silently=False,
                    )
                    print("EMAIL SENT ✅")
                except Exception as e:
                    print("EMAIL ERROR ❌:", e)
            mode = request.POST.get("mode")
            if(mode=="COD"):
                return HttpResponseRedirect("/place_order/")
            else:
                pass
        
        return render(request,"checkout.html",{"User":buyer,
                                                "Products":products,
                                                "Total":total,
                                                "Shipping":shipping,
                                                "Final":final,
                                                })

    except:
        return HttpResponseRedirect("/profile/")


@login_required(login_url="/login/")
def place_order(request):
    if request.method == "POST":

        # Get user email
        user_email = request.POST.get("email")  # or from form

        print("USER EMAIL:", user_email)  # ✅ debug

        if user_email:
                send_mail(
                    "Order Confirmed 🎉",
                    "Your order has been placed successfully. Thank you for shopping!",
                    settings.EMAIL_HOST_USER,
                    [user_email],
                    fail_silently=False,
            )

        return render(request, "place_order.html")


@login_required(login_url="/login/")
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login")


def aboutPage(request):
    return render(request,"about.html")


def newslatterPage(request):
    try:
        email = request.POST.get("email")
        n = Newslatter()
        n.email = email
        n.save()
        subject = 'Thanks to Subscribe out Newslatter Service'
        message = """
                  Thanks to Subscribe out Newslatter Service
                  Now you get an Email related to our latest products
                  and offers
                  visit for latest Product  and offers
                  http://localhost:8000/
                  Team : Eshop.com  
                   
                """
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail( subject, message, email_from, recipient_list )

        return HttpResponseRedirect("/")
    except:
        return HttpResponseRedirect('/')


def contactpage(request):
    if(request.method == "POST"):
        c = Contact()
        c.name = request.POST.get("name")
        c.email = request.POST.get("email")
        c.phone = request.POST.get("phone")
        c.subject = request.POST.get("subject")
        c.message = request.POST.get("message")
        c.save()
        messages.success(request,"Your Query has been submitted!!! Our team Will Conract You Soon")
        subject = 'Thanks to Contact US'

        send_mail(
            subject,
            Contact,
            'gkapoor2612@gmail.com',   # your Gmail
            ['gkapoor2612@gmail.com'],  # admin email
            fail_silently=False,
        )
        
        message = """
                
                Thanks to share your Query with us our
                Team Will Contact You Soon
                
                http://localhost:8000/
                Team : Eshop.com  
                   
                """
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [c.email, ]
        send_mail( subject, message, email_from, recipient_list )
    return render(request,"contact.html")


def forget_password(request):
    if request.method == "POST":
        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username)

            # Generate OTP
            otp = random.randint(100000, 999999)

            # Save in session
            request.session['reset_username'] = username
            request.session['otp'] = str(otp)   # store as string

            # Send Email
            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP is {otp}',
                'gkapoor2612@gmail.com',
                [user.email],
                fail_silently=False,
            )

            return HttpResponseRedirect('verify_otp')   # ✅ use name instead of URL

        except User.DoesNotExist:
            messages.error(request, "User does not exist")

    return render(request, 'forget.html')


def verify_otp(request):
    if request.method == "POST":
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')

        # Convert session OTP to string for comparison
        if session_otp and str(user_otp) == str(session_otp):
            # Use redirect with URL name
            return HttpResponseRedirect('reset_password')  # ✅ Correct URL name
        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'verify_otp.html')


def reset_password(request):
    if request.method == "POST":
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password == confirm:
            username = request.session.get('reset_username')

            if not username:
                messages.error(request, "Session expired. Try again.")
                return HttpResponseRedirect('forget_password')

            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()

            # Clear session
            request.session.flush()

            messages.success(request, "Password reset successful")
            return HttpResponseRedirect('login')

        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'reset_password.html')






@login_required(login_url="/login/")
def place_order(request):
    if request.method == "POST":
        user = request.user
        order_id = 123  # Replace with actual order ID logic

        # --- Send confirmation email ---
        subject = f"Order #{order_id} Placed Successfully"
        message = f"Hi {user.username},\n\nYour order #{order_id} has been placed successfully!\nThank you for shopping with us."
        recipient_list = [user.email]

        send_mail(
            subject,
            message,
            'gkapoor2612@gmail.com',  # Replace with your email
            recipient_list,
            fail_silently=False,
        )

        messages.success(request, "Order placed successfully! Check your email for confirmation.")

        # Redirect to confirmation page (use the URL name, not template path)
        return redirect('confirmation')

    # --- For GET requests, render a template ---
    # Ensure 'place_order.html' exists in your templates folder
    return render(request, 'place_order.html')


def confirmation(request):
    """
    Confirmation page after placing order
    """
    return render(request, 'confirmation.html')

    

@login_required(login_url="/login/")
def delete_order(request, id):
    if request.method == "POST":
        # Try to get the order belonging to the logged-in user
        order = Order.objects.filter(id=id, user=request.user).first()
        if order:
            order.delete()
            
    return redirect("/profile")


def newsletter_signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            # Optionally save the email in DB
            # NewsletterSubscriber.objects.create(email=email)

            # Send a confirmation email
            send_mail(
                'Thank You for Subscribing!',
                'You have successfully subscribed to our newsletter.',
                'gkapoor2612@example.com',  # sender
                [email],                  # recipient list
                fail_silently=False,
            )
            messages.success(request, 'Thanks for subscribing! Check your inbox.')
        return redirect('/')  # or wherever you want
    


def payment_page(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    payment = client.order.create({
        "amount": 50000,  # amount in paisa (500 INR)
        "currency": "INR",
        "payment_capture": 1
    })

    return render(request, "payment.html", {"payment": payment})