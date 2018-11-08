from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.forms import model_to_dict
from django.http import HttpResponse, QueryDict, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View
from axf import models
from .axf_utils import *
from .tasks import *
cache = caches['confirm']


def home(req):
    title = "首页"
    swipers = models.Wheel.objects.all()
    navs = models.Nav.objects.all()
    mustbuys = models.MustBuy.objects.all()
    shops = models.Shop.objects.all()
    maininfos = models.MainInfo.objects.all()
    shop0 = shops[0]
    data = {
        'title': title,
        'swipers': swipers,
        'mynavs': navs,
        'mustbuys': mustbuys,
        'shop0': shop0,
        'shop1_3': shops[1:3],
        'shop3_7':shops[3:7],
        'shop7_11': shops[7:],
        'maininfos': maininfos
    }
    return render(req, 'home/home.html', context=data)

def market(req):
    return redirect(reverse("axf:market_with_params", args=("104749","0","0")))



def market_with_params(req, type_id, sub_type_id , sort_id):
    types =  models.GoodsTypes.objects.all()

    goods = models.Goods.objects.filter(
        categoryid= int(type_id)
    )
    if sub_type_id == '0':
        pass
    else:
        goods = goods.filter(childcid=int(sub_type_id))
    # user = req.user
    # if isinstance(user, models.MyUser):
    #     # 问题
    #     tem_dict = {}
    #     cart_num = models.Cart.objects.filter(user_id = user.id)
    #     for i in cart_num:
    #         tem_dict[i.goods.id] = i.num
    #         print(tem_dict)
    #     for i in goods:
    #         i.productnum = tem_dict.get[i.id]  if tem_dict.get[i.id] else 0
    #         print(i.productnum)

    # 二级分类
    current_type = types.filter(typeid = type_id)[0]
    childtypenames = current_type.childtypenames.split("#")
    sub_types = []
    for i in childtypenames:

        tmp = i.split(':')
        sub_types.append(tmp)
    '''
    0: 综合排序
    1：价格排序
    2：销量排序
    
    '''
    zero_id = 0
    price_id = 1
    num_id = 2
    if int(sort_id) == zero_id:
        pass
    elif int(sort_id) == price_id:
        goods = goods.order_by("price")
    elif int(sort_id) == num_id:
        goods = goods.order_by("productnum")

    user = req.user
    if isinstance(user, models.MyUser):
        tmp_dict = {}
        # 去购物车查该用户的商品数据
        cart_nums = models.Cart.objects.filter(user=user)
        for i in cart_nums:
            tmp_dict[i.goods.id] = i.num

        # tmp_dict = {i.goods.id:i.num for i in Cart.objects.filter(user=user)}
        # print(cart_nums)
        # {1245: 3}
        # print(tmp_dict)
        for i in goods:
            # 添加商品数量
            i.num = tmp_dict.get(i.id) if tmp_dict.get(i.id) else 0
            # for j in cart_nums:
            #     if i.id == j.goods_id:
            #         i.num = j.num

    data = {
        "title": "闪购超市",
        "types":types,
        "goods":goods,
        "current_type_id": type_id,
        'sub_types': sub_types,
        'current_sub_type_id': sub_type_id,
        'sort_id': int(sort_id),
    }

    return  render(req, 'market/market.html',context=data)




@login_required(login_url='/axf/login')
def cart(req):
    user = req.user
    data = models.Cart.objects.filter(user_id = user.id)
    sum_money = get_cart_money(data)
    if data.exists() and not data.filter(is_selected=False).exists():
        is_all_select = True
    else:
        is_all_select = False
    result = {
        "title": "购物车",
        "uname": user.username,
        "phone": user.phone if user.phone else "暂无",
        "address": user.address if user.address else "暂无",
        "cart_items": data,
        "sum_money": sum_money,
        "is_all_select": is_all_select,
    }
    return  render(req, 'cart/cart.html',result)

def mine(req):
    user = req.user
    is_login = True
    if isinstance(user, AnonymousUser):
        is_login = False

    u_name = user.username if is_login else ""
    icon = "http://" + req.get_host() + "/static/uploads/" + user.icon.url if is_login else ""
    result = {
        "title": "我的",
        "is_login": is_login,
        "u_name": u_name,
        "icon": icon
    }
    return render(req, "mine/mine.html", result)





class register(View):
    def get(self,req):
        return  render(req,'mine/register.html')
    def post(self,req):
        params = req.POST
        icon = req.FILES.get("u_icon")
        pwd = params.get("u_pwd")
        confirm_pwd = params.get("u_confirm_pwd")
        email = params.get("email")
        name = params.get("u_name")

        if pwd and confirm_pwd and pwd == confirm_pwd:
            if models.MyUser.objects.filter(username=name).exists():
                return  render(req,'mine/register.html',{'help_msg': "已存在"})
            else:
              user = models.MyUser.objects.create_user(
                    username=name,
                    password=pwd,
                    email=email,
                    icon=icon,
                    is_active=False,
                )
        url = "http://" + req.get_host() + "/axf/confirm/" + get_token()
        send_verify_mail.delay(url, user.id, email)
        return  render(req,'mine/login.html')
class login_1(View):
    def get(self,req):
        return render(req,'mine/login.html')
    def post(self, req):
        # 1 解析参数
        params = req.POST
        name = params.get("name")
        pwd = params.get("pwd")
        # 2 校验数据
        if not name or not pwd:
            data = {
                "code": 2,
                "msg": "账号或密码不能为空",
                "data": ""
            }
            return JsonResponse(data)
        # 3 使用用户名 密码校验用户，
        user = authenticate(username=name, password=pwd)
        # 4 如果校验成功 登录
        if user:
            login(req, user)
            data = {
                'code': 1,
                "msg": "ok",
                "data": "/axf/mine"
            }
            return JsonResponse(data)
        # 5 失败的话返回错误提示
        else:
            data = {
                "code": 3,
                "msg": "账号或密码错误",
                "data": ""
            }
            return JsonResponse(data)
class logout_1(View):

    def get(self,req):
        logout(req)
        return  redirect(reverse('axf:mine'))

def confirm(req, uuid_str):
    user_id = cache.get(uuid_str)
    if user_id:
        user = models.MyUser.objects.get(pk = int(user_id))
        user.is_active = True
        user.save()
        return redirect(reverse("axf:login"))
    else:
        return HttpResponse("<h2>链接失效</h2>")

def check_uname(req):
    uname = req.GET.get("uname")
    data = {
        "code": 1,
        "data": "",
        }
    print(uname)
    if uname and len(uname)>=3:
        if models.MyUser.objects.filter(username = uname):
            data["msg"] = "账号已存在"
        else:
            data["msg"] = "可用"
    else:
        data["msg"]="账号太短"
    return  JsonResponse(data)

class cart_api(View):
    def post(self,req):
        user = req.user
        print(user)
        if not isinstance(user,models.MyUser):
            data = {
                "code": 2,
                "data": "/axf/login",
                "msg": "没登陆"}
            return  JsonResponse(data)
        op_type = req.POST.get("type")
        g_id = int(req.POST.get("g_id"))
        # print(g_id)
        # print(type(g_id))
        goods = models.Goods.objects.get(pk=g_id)
        print(goods)
        if op_type == "add":
            goods_num = 1
            if goods.storenums>1:
                cart_goods = models.Cart.objects.filter(
                    user = user,
                    goods = goods
                )
                if cart_goods.exists():
                    cart_item = cart_goods.first()
                    cart_item.num += 1
                    cart_item.save()
                    goods_num = cart_item.num
                else:
                   models.Cart.objects.create(
                        user=user,
                        goods=goods
                    )
                data = {
                    "code": 1,
                    "data": goods_num,
                    "msg": "ok"}
                return  JsonResponse(data)
            else:
                data = {
                    "code": 3,
                    "data": "",
                    "msg": "库存不足"}
                return JsonResponse(data)
        elif op_type == "sub":
            goods_num = 0
            # 先去查购物车的数据
            cart_item = models.Cart.objects.get(
                user=user,
                goods=goods
            )
            cart_item.num -= 1
            cart_item.save()
            if cart_item.num == 0:
                # 如果减到0 就删除购物车商品
                cart_item.delete()
            else:
                goods_num = cart_item.num

            data = {
                "code": 1,
                "msg": "ok",
                "data": goods_num
            }
            return JsonResponse(data)

class cart_status(View):

    def post(self,req):
        params = req.POST
        c_id = int(params.get("c_id"))
        user = req.user
        cart_items = models.Cart.objects.filter(user_id=user.id)
        cart_data = cart_items.get(id = c_id)
        cart_data.is_selected = not cart_data.is_selected
        cart_data.save()
        sum_money = get_cart_money(cart_items)
        if cart_items.filter(is_selected=False):
            is_all_select = False
        else:
            is_all_select = True
        result = {
            "code":1,
            "msg":"ok",
            "data":{
                "is_all_select":is_all_select,
                "sum_money": sum_money,
                "status": cart_data.is_selected
                    }
            }
        return JsonResponse(result)
class cartall_status(View):
    def put(self,req):
        user = req.user
        cart_items = models.Cart.objects.filter(user_id=user.id)
        is_select_all = False
        if cart_items.exists() and cart_items.filter(is_selected=False).exists():
            is_select_all = True
            for i in cart_items.filter(is_selected=False):
                i.is_selected = True
                i.save()
            sum_money = get_cart_money(cart_items)
        else:
            cart_items.update(is_selected = False)
            sum_money = 0
        result = {
            "code":1,
            "msg": "ok",
            "data":{
                "sum_money":sum_money,
                "is_all_select": is_select_all
            }
        }
        return JsonResponse(result)

# class cart_item(View):
#     def post(self,req):
#         user = req.user
#         c_id = req.POST.get("c_id")
#         cart_item = models.Cart.objects.get(id = int(c_id))
#         if cart_item.goods.storenums<1:
#             data={
#                 "code": 2,
#                 "msg": "库存不够",
#                 "data": "",
#             }
#             return  JsonResponse(data)
#         cart_item.num += 1
#         cart_item.save()
#         cart_items = models.Cart.objects.filter(
#             user_id=user.id, is_selected=True
#         )
#         sum_money = get_cart_money(cart_items)
#         data = {
#             "code":1,
#             "msg": "ok",
#             "data":{
#                 "sum_money":sum_money,
#                 "num": cart_item.num
#             }
#         }
#         return JsonResponse(data)
#     def delete(self,req):
#         user = req.user
#
#         c_id=QueryDict(req.body).get("c_id")
#         cart_item = models.Cart.objects.get(pk = int(c_id))
#         cart_item.num -= 1
#         cart_item.save()
#         if cart_item.num == 0:
#             good_num = 0
#             cart_item.delete()
#         else:
#             good_num = cart_item.num
#         cart_items = models.Cart.objects.filter(
#             user_id= user.id, is_selected=True
#         )
#         sum_money = get_cart_money(cart_items)
#         data = {
#             "code": 1,
#             "msg": "ok",
#             "data": {
#                 "sum_money": sum_money,
#                 "num": cart_item.num
#             }
#         }
#         return  JsonResponse(data)


# class order(View):
#     def get(self,req):
#         user = req.user
#         cart_item = models.Cart.objects.get(
#             user_id=user.id,is_selected=True
#         )
#         if not cart_item.objects.exists():
#             return render(req, 'order/order_detail.html')
#         order = models.Order.objects.create(
#             user = user
#         )
#         for i in cart_item:
#             models.OrderItem.objects.create(
#                 order = order,
#                 goods = i.goods,
#                 num = i.num,
#                 buy_money = i.goods.price
#             )
#         sum_money = get_cart_money(cart_item)
#         cart_item.delete()
#         data = {
#             "sum_money":sum_money,
#             "order": order
#
#         }
#         return render(req,'order/order_detail.html',data)
