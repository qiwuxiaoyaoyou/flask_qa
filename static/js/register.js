function bindCaptchaBtnClick(){
    //jquery将自动在网页中寻找id为captcha-btn的元素
    $("#captcha-btn").on("click",function (event){
        var $this = $(this);
        var email = $("input[name='email']").val();     //获取email输入框的值
        if(!email){     //如果没有邮箱
            alert('请先输入邮箱！');
            return;
        }
        //通过js发送网络请求：ajax ( Async JavaScript AND XML )  现在一般都用JSON格式
        $.ajax({
            url:"/user/captcha",
            method:"POST",
            data:{
                "email":email
            },
            success:function (res){
                var code = res['code'];
                if(code == 200){
                    $this.off("click");     //取消点击事件
                    var countDown = 60;     //倒计时为60秒
                    var timer = setInterval(function (){     //setInterval是js内置的用于倒计时的功能
                        countDown -= 1;     //每次减1秒
                        if(countDown > 0){
                            $this.text(countDown+"秒后重新发送");  //如果倒计时还大于0秒，显示xx秒后重新发送
                        }else {
                            $this.text("获取验证码");       //否则，显示‘获取验证码’
                            bindCaptchaBtnClick();      //重新执行验证码的函数，重新绑定点击事件
                            clearInterval(timer);       //如果不再需要倒计时，那么应当清楚倒计时
                        }
                    },1000);            //此处timeout:1000 单位为毫秒，1000毫秒=1秒
                    alert("验证码发送成功！");
                }else{
                    alert(res['message']);
                }
            }
        })
    });
}

//等网页文档所有元素都加载完成后再执行
$(function (){
    bindCaptchaBtnClick();
});