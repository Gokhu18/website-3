from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from .models import product,buyer,cart,seller,address,order,review
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import connection
from django.contrib.auth.models import Group
import datetime
from django.views.decorators.cache import never_cache
from django.core.mail import EmailMessage
# Create your views here.
@never_cache
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
@never_cache
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
def index (request):
    if request.user.is_authenticated:
        cursor=connection.cursor()
        user_email=request.user.email
        query="select * from buyer where b_email='"+user_email+"';"
        print(query)
        user=len(list(buyer.objects.raw(query)))
        if(user==0):
            cursor.execute("insert into buyer values('"+user_email+"','"+request.user.username+"')")
        price="90rs"
        products=product.objects.all()
        context= {
                'products':products,
                'price':price,
                'product1':products[0],
                'product2':products[1],
                'product3':products[2],
                #'username':username
        }
        return render(request,'homepage/index.html',context)
    else:
        return render(request,'login.html')
@never_cache
@login_required
def product_detail(request, id):
    product_now=product.objects.get(id=id)
    in_stock=False
    print(product_now.stock)
    if(product_now.stock is not 0):
        in_stock=True
    print(str(in_stock))
    review1=review.objects.raw("select * from review where pid_id="+str(id))
    l=[]
    for r in review1:
        l.append(r)
    print(l)
    context={
    "product":product_now,
    "in_stock":in_stock,
    "reviews":l
    }
    return render(request,"product.html",context)
@never_cache
@login_required
def add_to_cart(request, id):
    product_now=product.objects.get(id=id)
    cursor=connection.cursor()
    user_email=request.user.email
    p_id=str(product_now.id)
    query="select * from cart where bid_id='"+user_email+"' and pid_id="+p_id
    c=len(list(cart.objects.raw(query)))
    print(c)
    if(c==0):
        print("in insert")
        cursor.callproc("add_to_cart",[product_now.id,user_email,product_now.price,product_now.s_id_id])
    else:
        cursor.execute("update cart set quantity=quantity+1 where pid_id="+p_id+" and bid_id='"+user_email+"';")
        cursor.execute("update cart set price="+product_now.price+"*quantity where pid_id="+p_id+" and bid_id='"+user_email+"';")
    context={
    "product":product_now
    }
    return render(request,"product.html",context)
@never_cache
@login_required
def cart1(request):
    if request.user.is_authenticated:
    	user_email=request.user.email
    	cursor=connection.cursor()
    	cursor.execute("select * from show_cart1('"+user_email+"') as f(id integer,quantity integer,price integer,title varchar,image varchar);")
    	items=[]
    	total=0
    	for row in cursor:
    	    l={
    	        'id' : row[0],
    	        'quantity':row[1],
    	        'price' : row[2],
    	        'title' : row[3],
    	        'image':product.objects.get(id=row[0]).image
    	    }
    	    print(l["image"])
    	    total+=row[2]
    	    print(row)
    	    items.append(l)
    	s_total=total+120
    	context={
    	    'items':items,
    	    'total':total,
    	    'total_s':s_total
    	}
    	return render(request,"cart.html",context)
    else:
    	return render(request,'login.html')
@never_cache
@login_required
def sell(request):
    cursor=connection.cursor()
    if(len(list(seller.objects.raw("select * from seller where s_email='"+request.user.email+"'")))):
        print("exists")
    else:
        print("doesnt exist")
        my_group = Group.objects.get(name='seller') 
        my_group.user_set.add(request.user)
    return redirect( "/admin/webapp/product/add/")
@never_cache
def order1(request):
    if request.user.is_authenticated:
    	rs=cart.objects.raw("select * from cart where bid_id='"+request.user.email+"'")
    	cursor=connection.cursor()
    	if(len(list(address.objects.raw("select * from address where bid_id='"+request.user.email+"'")))):
    	    print("exists")
    	else:
    	    print(request.POST.get('pincode'))
    	    str1="insert into address(bid_id,name,address,state,pincode,ccnum,exp_month,exp_year) values('"+request.user.email+"','"+request.POST.get('firstname')+"','"+request.POST.get('address')+"','"+request.POST.get('state')+"',"+str(request.POST.get('pincode'))+","+str(request.POST.get('ccnum'))+","+str(request.POST.get('expmonth'))+","+str(request.POST.get('expyear'))+")"
    	    print(str1)
    	    cursor.execute(str1)
    	rs1=address.objects.raw("select id from address where bid_id='"+request.user.email+"'")
    	for u in rs1:
    	    id1=u.id
    	for r in rs:
    	    print(str(r.pid_id)+" "+r.bid_id+" "+str(r.sid_id)+" ")
    	    cursor.execute("insert into order1(created_at,price,bid_id,pid_id,sid_id,address_id,quantity) values('"+str(datetime.datetime.now())+"',"+str(r.price)+",'"+r.bid_id+"',"+str(r.pid_id)+","+str(r.sid_id)+","+str(id1)+","+str(r.quantity)+") ")
    	    cursor.execute("select title from product where id="+str(r.pid_id))
    	    pname=""
    	    for i in cursor:
    	        pname=i[0]
    	        print(i)
    	    order_now="\nproduct:"+pname+"\nquanity:"+str(r.quantity)
    	    cursor.execute("select s_email from seller where id="+str(r.sid_id))
    	    s_email=""
    	    for i in cursor:
    	        s_email=i[0]
    	    email1=EmailMessage('New Order',order_now,to=[s_email])
    	    email1.send()
    	    order_now="buyer:"+r.bid_id+"\nseller:"+str(r.sid_id)+order_now+"\ntotal price:"+str(r.price)+"\n"
    	    email1=EmailMessage('New Order',order_now,to=['kvivek1339@gmail.com'])
    	    email1.send()
    	return redirect("/")
    else:
    	return render(request,'login.html')
@never_cache
def checkout(request):
    user_email=request.user.email
    cursor=connection.cursor()
    cursor.execute("select * from show_cart1('"+user_email+"') as f(id integer,quantity integer,price integer,title varchar,image varchar);")
    items=[]
    total=0
    for row in cursor:
        l={
            'id' : row[0],
            'quantity':row[1],
            'price' : row[2],
            'title' : row[3],
            'image':product.objects.get(id=row[0]).image
        }
        print(l["image"])
        total+=row[2]
        items.append(l)
    length=len(items)
    print(items)
    context={
        'products':items,
        'total':total,
        'len':length
    }
    return render(request,"checkout.html",context)
@never_cache
def remove_cart(request,id):
    user_email=request.user.email
    cursor=connection.cursor()
    cursor.callproc('remove_from_cart',[id,user_email])
    return cart1(request)
@never_cache
def cart_update(request,id):
    quantity=request.GET.get('quantity')
    print(quantity)
    return cart1(request)
def p1(request,id):
    cursor=connection.cursor()
    product_now=list(product.objects.filter(category=id))
    context={
        "product":product_now,
        "id":id
    }
    return render(request,'products.html',context)
def orders(request):
    if request.user.is_authenticated:
    	cursor=connection.cursor()
    	cursor.execute("select * from peek_orders('"+request.user.email+"') as f(id integer,title varchar,image varchar,quantity integer,price integer)")
    	items=[]
    	for row in cursor:
    	    l={
    	        'id':row[0],
    	        'title' : row[1],
    	        'image':row[2],
    	        'quantity' : row[3],
    	        'price' : row[4],
    	    }
    	    print(row[1])
    	    items.append(l)
    	context={
    	'cursor':items
    	}
    	return render(request,'sample.html',context)
    else:
    	return render(request,'login.html')
def review_now(request,id):
    cursor=connection.cursor()
    review1=request.POST.get('review')
    rating=request.POST.get('rating')
    rs=review.objects.raw("select * from review where bid_id='"+request.user.email+"' and pid_id="+str(id))
    if(len(list(rs))==0):
        cursor.execute("insert into review(bid_id,pid_id,review,rating) values('"+request.user.email+"',"+str(id)+",'"+review1+"',"+str(rating)+")")
    else:
        cursor.execute("update review set review='"+review1+"' where bid_id='"+request.user.email+"' and pid_id="+str(id))
        cursor.execute("update review set rating='"+rating+"' where bid_id='"+request.user.email+"' and pid_id="+str(id))
    cursor.execute("select avg(rating) from review where pid_id="+str(id))
    rate=0
    for r in cursor:
        rate=r[0]
    print(rate)
    cursor.execute("update product set rating="+str(rate)+" where id="+str(id))
    return redirect('/product/'+id)
