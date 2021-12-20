from django.shortcuts import render


# Create your views here.
def store(request):
    context = {}
    return render(request, 'store/store.html', context)


def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)


def login(request):
    context = {}
    return render(request, 'store/login.html', context)


def register(request):
    context = {}
    return render(request, 'store/register.html', context)


def mypage(request):
    context = {}
    return render(request, 'store/mypage.html', context)


def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

def customerservice(request):
    context = {}
    return render(request, 'store/customerservice.html', context)

def faq(request):
    context = {}
    return render(request, 'customerservice/faq.html', context)

def onetoone(request):
    context = {}
    return render(request, 'customerservice/onetoonequestion.html', context)


def product_detail(request):
    context = {}
    return render(request, 'store/productdetail.html', context)






#주문 관리 view
def orderhistory(request):
    context = {}
    return render(request, 'mypage/orderhistory.html', context)

def ordercancel(request):

    context = {}
    return render(request, 'mypage/ordercancel.html', context)

def orderrefund(request):

    context = {}
    return render(request, 'mypage/orderrefund.html', context)

#마이페이지
def favoritelist(request):
    context = {}
    return render(request, 'mypage/favoritelist.html',context)

def couponlist(request):
    context = {}
    return render(request, 'mypage/couponlist.html',context)

def orderrefund(request):
    context = {}
    return render(request, 'mypage/orderrefund.html',context)

def pointlist(request):
    context = {}
    return render(request, 'mypage/pointlist.html',context)

def qnalist(request):
    context = {}
    return render(request, 'mypage/qnalist.html',context)

def refundlist(request):
    context = {}
    return render(request, 'mypage/refundlist.html',context)

def reviewlist(request):
    context = {}
    return render(request, 'mypage/reviewlist.html',context)

def userinfo(request):
    context = {}
    return render(request, 'mypage/userinfo.html',context)

def orderdetail(request):
    context = {}
    return render(request, 'mypage/orderdetail.html',context)