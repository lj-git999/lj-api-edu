<template>
    <div class="login box">
        <img src="../../static/image/1111.jpg" alt="">
        <div class="login">
            <div class="login-title">
                <img src="../../static/image/logo.png" alt="">
                <p>百知教育给你最优质的学习体验!</p>
            </div>
            <div class="login_box">
                <div class="title">
                    <span @click="get_login=0" :class="get_login===0?'active':''">密码登录</span>
                    <span @click="get_login=1" :class="get_login===1?'active':''">短信登录</span>
                </div>
                <div class="inp" v-if="get_login===0">
                    <input v-model="username" type="text" placeholder="用户名 / 手机号码 / 邮箱" class="user" @blur="get_username">
                    <span id="span"></span>
                    <input v-model="password" type="password" name="" class="pwd" placeholder="密码" @blur="get_password">
                    <span id="id"></span>
                    <div id="geetest1"></div>
                    <div class="rember">
                        <p>
                            <input type="checkbox" class="no" v-model="remember"/>
                            <span>记住密码</span>
                        </p>
                        <p>忘记密码</p>
                    </div>
                    <button class="login_btn btn btn-primary" @click="get_captcha">登录</button>
                    <p class="go_login">没有账号
                        <router-link to="/register">立即注册</router-link>
                    </p>
                </div>
                <div class="inp" v-show="get_login===1">
                    <input v-model="account" type="text" placeholder="手机号码" class="user" @blur="get_phone">
                    <span id="span1"></span>
                    <input v-model="code" type="text" class="pwd" placeholder="短信验证码" @blur="get_coder">
                    <span id="span2"></span>
                    <button id="get_code" class="btn btn-primary" @click="get_code">获取验证码</button>
                    <button class="login_btn" @click="get_users">登录</button>
                    <span class="go_login">没有账号
                    <router-link to="/register">立即注册</router-link>
                </span>
                </div>
            </div>
        </div>
    </div>


</template>

<script>
export default {
    name: "Login",
    data(){
        return {
            username:'',
            password:'',
            remember:false,
            get_login:0,
            account:"",
            code:"",
            flag:false,
        }
    },
    methods:{
        handlerPopup(captchaObj) {
            let self=this;
            captchaObj.onSuccess(function () {
                let validate = captchaObj.getValidate();
                self.$axios({
                    url: self.$settings.HOST+"user/captcha/",
                    method: "post",
                    data: {
                        username: self.username,
                        password: self.password,
                        geetest_challenge: validate.geetest_challenge,
                        geetest_validate: validate.geetest_validate,
                        geetest_seccode: validate.geetest_seccode
                    },
                }).then(rst=>{
                    console.log(rst.data.status);
                    if (rst.data.status==="success"){
                        self.user_login();
                    }

                }).catch(error=>{
                    console.log(error);
                })
            });
           document.getElementById("geetest1").innerHTML="";
            // 将验证码加到id为captcha的元素里
            captchaObj.appendTo("#geetest1");
        },
        get_captcha(){
            console.log(this.username)
            if (this.username === null || this.password === null) {
                console.log(this.password)
                this.$alert("不能为空，请填写", "警告!");
                return false
            }
            this.$axios({
                url:this.$settings.HOST+"user/captcha/",
                method:"get",
                params:{
                    username:this.username
                }
            }).then(rst=>{
                console.log(rst.data);
                let data=JSON.parse(rst.data);
                initGeetest({
                    gt: data.gt,
                    challenge: data.challenge,
                    product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
                    offline: !data.success, // 表示用户后台检测极验服务器是否宕机，一般不需要关注
                    new_captcha: data.new_captcha
                }, this.handlerPopup);
            }).catch(error=>{
                console.log(error);
                this.$message.error("您输入的用户不存在")
            })

        },
        user_login(){
            this.$axios({
                url:this.$settings.HOST+"user/login/",
                method:"post",
                data:{
                    username:this.username,
                    password:this.password,
                }
            }).then(rst=>{
                console.log(rst.data,this.remember);
                if (rst.data.token){
                    this.$message({
                        message:"恭喜你，登录成功",
                        type:"success",
                        duration:1000,
                    })
                if (this.remember===false){
                    localStorage.clear();
                }else {
                    localStorage.setItem('password',this.password);
                    localStorage.setItem('username',rst.data.username);
                    localStorage.setItem('token',rst.data.token);
                }
                sessionStorage.setItem('token',rst.data.token);
                sessionStorage.setItem('username',rst.data.username);
                sessionStorage.setItem('user_id',rst.data.user_id);

                this.$router.push("/")
                }
            }).catch(error=>{
                console.log(error);
                this.$message.error("账号或密码错误，请重新输入")
            })
        },
        get_user(){
            this.username=localStorage.getItem("username");
            this.password=localStorage.getItem("password");
        },
        get_username(){
            console.log(this.username)
            if(this.username === null){
                document.getElementById("span").innerHTML="用户名不能为空"
                document.getElementById("span").style.color='red'
            }
        },
        get_password(){
            if (this.password === null){
                document.getElementById("id").innerHTML="密码不能为空"
                document.getElementById("id").style.color='red'
            }
        },
        get_phone(){
            if(this.account===""){
                document.getElementById("span1").innerHTML="手机号不能为空";
                document.getElementById("span1").style.color="red";
            }
            this.$axios({
                url:this.$settings.HOST+"user/verify_phone/",
                method:"get",
                params:{
                    phone:this.account
                }
            }).then(rst=>{
                console.log(rst.data);
                document.getElementById("span1").innerHTML=""
                this.flag=true;
            }).catch(error=>{
                console.log(error);
                document.getElementById("span1").innerHTML="此手机号没有注册，请先注册";
                document.getElementById("span1").style.color="red";
            })

        },
        get_coder(){
            if(this.code===""){
                document.getElementById("span2").innerHTML="短信验证码不能为空";
                document.getElementById("span2").style.color="red";
            }
        },
        get_code(){
            if(!/^(13[0-9]|14[01456879]|15[0-3,5-9]|16[2567]|17[0-8]|18[0-9]|19[0-3,5-9])\d{8}$/.test(this.account) || this.flag===false){
                  this.$alert("手机号不合法|该手机号没有注册","警告");
                  return false
            }
            this.$axios({
                url:this.$settings.HOST+"user/message/",
                method:"get",
                params:{
                    phone:this.account,
                }
            }).then(rst=>{
                console.log(rst.data);
            }).catch(error=>{
                console.log(error);
            })


        },
        get_users(){
            if (this.account==="" || this.code===""){
                this.$alert("不能为空，请输入","警告");
                return false
            }
            this.$axios({
                url:this.$settings.HOST+"user/login_phone/",
                method:"post",
                data:{
                    account:this.account,
                    code:this.code
                }
            }).then(rst=>{
                console.log(rst.data.token);
                if (rst.data.token){
                    this.$message({
                        message:"恭喜你，登录成功",
                        type:"success",
                        duration:1000
                    })
                }
                sessionStorage.setItem("phone",rst.data.user.phone);
                sessionStorage.setItem("token",rst.data.token);
                sessionStorage.setItem("id",rst.data.user.id);
                this.$router.push("/")




            }).catch(error=>{
                console.log(error);
            })
        }

    },
    created() {
        this.get_user();
        let token=sessionStorage.getItem("token");
        if (token){
            this.$router.go(-1);
            this.$message({
                message:"已经登录成功",
                type:"success",
                duration:1000,
            })
        }
    }

}
</script>

<style scoped>
.box {
    width: 100%;
    height: 100%;
    position: relative;
    overflow: hidden;
}

.box img {
    width: 100%;
    min-height: 100%;
}

.box .login {
    position: absolute;
    width: 500px;
    height: 400px;
    top: 0;
    left: 0;
    margin: auto;
    right: 0;
    bottom: 0;
    top: -338px;
}

.login .login-title {
    width: 100%;
    text-align: center;
}

.login-title img {
    width: 190px;
    height: auto;
}

.login-title p {
    font-family: PingFangSC-Regular;
    font-size: 18px;
    color: #fff;
    letter-spacing: .29px;
    padding-top: 10px;
    padding-bottom: 50px;
}

.login_box {
    width: 400px;
    height: auto;
    background: #fff;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
    border-radius: 4px;
    margin: 0 auto;
    padding-bottom: 40px;
}

.login_box .title {
    font-size: 20px;
    color: #9b9b9b;
    letter-spacing: .32px;
    border-bottom: 1px solid #e6e6e6;
    display: flex;
    justify-content: space-around;
    padding: 50px 60px 0 60px;
    margin-bottom: 20px;
    cursor: pointer;
}

.login_box .title .active {
    color: #4a4a4a;
    border-bottom: 2px solid #84cc39;
}

.inp {
    width: 350px;
    margin: 0 auto;
}

.inp input {
    border: 0;
    outline: 0;
    width: 100%;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}

.inp input.user {
    margin-bottom: 16px;
}

.inp .rember {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin-top: 10px;
}

.inp .rember p:first-of-type {
    font-size: 12px;
    color: #4a4a4a;
    letter-spacing: .19px;
    margin-left: 22px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    /*position: relative;*/
}

.inp .rember p:nth-of-type(2) {
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
    cursor: pointer;
}

.inp .rember input {
    outline: 0;
    width: 30px;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}

.inp .rember p span {
    display: inline-block;
    font-size: 12px;
    width: 100px;
    /*position: absolute;*/
    /*left: 20px;*/

}

#geetest {
    margin-top: 20px;
}

.login_btn {
    width: 100%;
    height: 45px;
    background: #84cc39;
    border-radius: 5px;
    font-size: 16px;
    color: #fff;
    letter-spacing: .26px;
    margin-top: 30px;
}

.inp .go_login {
    text-align: center;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .26px;
    padding-top: 20px;
}

.inp .go_login span {
    color: #84cc39;
    cursor: pointer;
}
</style>
