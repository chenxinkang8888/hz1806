// $(function () {
//     var type_icon_is_up = false;
//     $("#all_types_btn").click(function () {
//         $("#category_container").toggle();
//         type_icon_is_up = icon_toggle(type_icon_is_up)
//     })
//     $("#category_container").click(function () {
//         $(this).toggle()
//         type_icon_is_up = icon_toggle(type_icon_is_up)
//     })
//
//     var sort_icon_is_up = false;
//     $("#all_sort_btn").click(function () {
//         $("#sort_container").toggle();
//         sort_icon_is_up = sort_icon_toggle(sort_icon_is_up)
//     })
//     $("#sort_container").click(function () {
//         $(this).toggle()
//         sort_icon_is_up = sort_icon_toggle(sort_icon_is_up)
//     })
//
// //    给加号添加点击事件
//     $(".addShopping").click(function () {
//     //    获取点击的那个按钮的goods_id
//         var item_id = $(this).attr("goods_id");
//         var $addbtn = $(this);
//         console.log(item_id);
//         $.ajax({
//             url:'/axf/api/v1/cart',
//             data:{
//                 'item_id': item_id,
//                 'operate_type': 'add'
//             },
//             method:"get",
//             success: function (data) {
//                 //json转 object
//                 var json_data = JSON.parse(data);
//                 console.log(json_data);
//             //    更新span 数据（显示数量的）
//                 if (json_data.code == 1){
//                     var item_num = json_data.data;
//                     $addbtn.prev().html(item_num);
//                 }
//             //    没登陆
//                 if (json_data.code == 2) {
//                     var url = "http://139.199.112.199:12358"+json_data.data
//                     window.open(url=url, target="_self");
//                 }
//             }
//         })
//     })
//
//
//     //    给减号添加点击事件
//     $(".subShopping").click(function () {
//     //    获取点击的那个按钮的goods_id
//         var item_id = $(this).attr("goods_id");
//         var $subbtn = $(this);
//         console.log(typeof $subbtn.next().text(), $subbtn.next().text());
//         if ($subbtn.next().text() == '0'){
//             return;
//         }
//         $.ajax({
//             url:'/axf/api/v1/cart',
//             data:{
//                 'item_id': item_id,
//                 'operate_type': 'sub'
//             },
//             method:"get",
//             success: function (data) {
//                 //json转 object
//                 var json_data = JSON.parse(data);
//             //    更新span 数据（显示数量的）
//                 if (json_data.code == 1){
//                     var item_num = json_data.data;
//                     //拿span
//                     $subbtn.next().html(item_num);
//                 }
//             //    没登陆
//                 if (json_data.code == 2) {
//                     var url = "http://139.199.112.199:12358"+json_data.data
//                     window.open(url=url, target="_self");
//                 }
//             }
//         })
//     })
//
//
//
// })
// function icon_toggle(type_icon_is_up) {
//         var $type_icon = $("#type_icon");
//         if (type_icon_is_up == false) {
//             $type_icon.removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up")
//             type_icon_is_up = true
//         } else {
//             $type_icon.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down")
//             type_icon_is_up = false
//         }
//         return type_icon_is_up
// }
//
// function sort_icon_toggle(type_icon_is_up) {
//         var $type_icon = $("#sort_icon");
//         if (type_icon_is_up == false) {
//             $type_icon.removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up")
//             type_icon_is_up = true
//         } else {
//             $type_icon.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down")
//             type_icon_is_up = false
//         }
//         return type_icon_is_up
// }
//
var cat_toggle_tag = false;
var sort_toggle_tag = false;
$(function () {
    $("#all_cate").click(cate_toggle);
    $("#cates").click(cate_toggle);


    $("#all_sort").click(sort_toggle);
    $("#sorts").click(sort_toggle);
    $(".addShopping").click(function () {
        $current_bt = $(this);
        var g_id = $current_bt.attr("g_id");
        $.ajax(
            {
                url:"/axf/cart_api",
                data:{
                    type: "add",
                    g_id: g_id
                },
                method: "post",
                success:function (res) {
                    if(res.code == 1){
                        $current_bt.prev().html(res.data)
                    }
                    if(res.code==2){
                        window.open(res.data, target="_self");
                    }
                }


            }
        )
    });
    $(".subShopping").click(function () {
        $current_bt = $(this);
    //    获取点击的那个商品的id
        var g_id = $current_bt.attr("g_id");
        //判断一下当前显示的是不是0 如果是0 那就return 不发送请求
        if ($current_bt.next().html() == "0"){
            return;
        }

        $.ajax({
            url:"/axf/cart_api",
            data:{
                g_id: g_id,
                type: "sub"
            },
            method:"post",
            success:function (res) {
                // console.log(res);
                if (res.code == 1){
                    //修改显示的数字
                    $current_bt.next().html(res.data);
                }
                if (res.code == 2){
                    //跳转到登录
                    window.open(res.data, target="_self");
                }
            }
        });
    });
});
function sort_toggle() {
    $("#sorts").toggle();
    if (sort_toggle_tag == false) {
        $("#all_sort").find("span").removeClass("glyphicon glyphicon-chevron-down").addClass("glyphicon glyphicon-chevron-up")
       sort_toggle_tag = true
    } else {
        $("#all_sort").find("span").removeClass("glyphicon glyphicon-chevron-up").addClass("glyphicon glyphicon-chevron-down")
        sort_toggle_tag = false
    }

}
function cate_toggle() {
    $("#cates").toggle();
    if (cat_toggle_tag == false){
        $(this).find("span").removeClass("glyphicon glyphicon-chevron-down").addClass("glyphicon glyphicon-chevron-up")
        cat_toggle = true
    } else {
        $(this).find("span").removeClass("glyphicon glyphicon-chevron-up").addClass("glyphicon glyphicon-chevron-down")
        cat_toggle = false
    }
}