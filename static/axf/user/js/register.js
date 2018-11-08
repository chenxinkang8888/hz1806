//
// $(function () {
//     $("#myform").submit(function ()
//      {
//         var name = $("#uid").val();
//          if(name.length<3){
//             alert("用户名过短");
//              return false}
//           var pwd = $("#u_pwd").val();
//           var confirm_pwd = $("#u_confirm_pwd").val();
//           if(pwd == confirm_pwd && pwd.length>6){
//                 var enc_pwd = md5(pwd);
//                 var enc_confirmpwd = md5(confirm_pwd);
//                 $("#u_pwd").val(enc_pwd);
//                 $("#u_confirm_pwd").val(enc_confirmpwd)
//           }
//           else {
//               alert("密码太短");
//               return false
//           }
//          }
//     )
//
// });
$(function () {
    $("#myform").submit(function () {
    //    拿用户名 判断不能为空 并且大于三位
        var name = $("#uid").val();
        if (name.length < 3){
            alert("用户名过短");
            //阻止提交
            return false;
        }

        var pwd = $("#u_pwd").val();
        var confirm_pwd = $("#u_confirm_pwd").val();
        if (pwd == confirm_pwd & pwd.length>=6){
        //    做加密
            var enc_pwd = md5(pwd);
            var enc_confirm_pwd = md5(confirm_pwd);
        //    设置回去
            $("#u_pwd").val(enc_pwd);
            $("#u_confirm_pwd").val(enc_confirm_pwd);
        } else {
            alert("密码过短或不一致");
            return false;
        }

    });
    $("#uid").change(function () {
        var name = $("#uid").val();
        $.ajax({
            url: "/axf/check_uname",
            data: {
                uname: name
            },
            method: "get",
            success: function (res) {
                if(res.code == 1){
                    $("#uname_msg").html(res.msg)
                }
                else {
                    alert(res.msg)
                }
            }
        })
    })
})