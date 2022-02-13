---
title: "我的小伙伴们"
date: 2021-01-16T00:24:31+08:00
draft: false
---

![一封纸笺](letter-from-friend.jpg)

{{< particles_effect_up  >}}

>感谢 @芝士部落格 提供了友链页面模板~

在友链形成的网络中漫游，是一件很有意思的事情。

**以前的人们通过信笺交流，而我们通过友链串联起一个「世界」。希望你我都能在这个「世界」中有所收获**

**注：** <span style="color:red;">下方友链次序每次刷新页面随机排列。<span>

<div class="linkpage"><ul id="friendsList"></ul></div>

## 交换友链

如果你觉得我的博客有些意思，而且也有自己的独立博客，欢迎与我交换友链~

可通过 [Issues](https://github.com/ryan4yin/ryan4yin.space/issues) 或者评论区提交友链申请，格式如下：

    站点名称：Ryan4Yin's Space
    站点地址：https://thiscute.world/
    个人形象：https://www.gravatar.com/avatar/2362ce7bdf2845a92240cc2f6609e001?s=240
    站点描述：赞美快乐~


<script type="text/javascript">
// 以下为样例内容，按照格式可以随意修改
var myFriends = [
    ["https://chee5e.space", "https://chee5e.space/images/avatar.jpg", "@芝士部落格", "有思想，也有忧伤和理想，芝士就是力量"], 
    ["https://sanshiliuxiao.top/", "https://cdn.jsdelivr.net/gh/vensing/static@latest/avatar/sanshiliuxiao.jpg", "@三十六咲", "快走吧，趁风停止之前"], 
    ["https://rea.ink/", "https://rea.ink/head.png", "@倾书", "清风皓月，光景常新 <= 前端"], 
    ["https://jdragon.club/", "/avatar/jdragon.jpg", "@谭宇", "Hello world! <= Java"], 
    ["https://www.jianshu.com/u/af3a36ae8d16", "/avatar/li2niu.png", "@李二牛", "深耕Web服务端 马拉松爱好者(PB330) <= Java"], 
    // ["https://www.i-lab.top/", "https://www.i-lab.top/favicon.ico", "@震邦的算法日常", "南北传"], 
    ["https://cxcn.xyz/", "https://cxcn.xyz/avatar.png", "@单单", "但知行好事，莫要问前程"], 
    ["https://farer.org/", "/avatar/farer.jpg", "@Stray Episode", "Scientific Evocation"], 
    ["https://wasteland.touko.moe", "https://wasteland.touko.moe/images/avatar.png", "@Touko Hoshino", "My Exploration, My Whisper"], 
    ["https://blog.k8s.li/", "/avatar/muzi.png", "@木子", "垃圾佬、搬砖社畜、运维工程师 <= 莫得感情的读书机器"], 
    ["https://www.addesp.com", "https://www.addesp.com/avatar", "@ADD-SP", "记录 & 分享 & 感受 <= 硬核网络协议分析"], 
    ["https://thautwarm.github.io/Site-32/", "/avatar/thautwarm.jpg", "@thautwarm", "Driven by the desire of making a difference. <= PLT 专家"], 
    ["https://yidajiabei.xyz/", "/avatar/tianheg.png", "@一大加贝", "学习技术，热爱生活"], 
    ["https://guanqr.com/", "https://cdn.jsdelivr.net/gh/guanqr/blog/static/icons/android-chrome-512x512.png", "@荷戟独彷徨", "爱光学，爱生活，爱创造"], 
    ["https://exploro.one", "https://avatars.githubusercontent.com/u/4038871?s=460&u=d2f1c2eea96acb15578f2e513ba5fa673aa3d250&v=4", "@探索子", "Learn by doing. <= 硬核数学博客"], 
    ["https://panqiincs.me/", "https://panqiincs.me/images/avatar.jpg", "@辛未羊", "人生如逆旅，我亦是行人 <= 是熟悉 CS 跟信号系统的高中教师哦"], 
    ["https://a-wing.top/", "https://a-wing.top/assets/avatar.png", "@新一", "Hi! 上天不? <= 无人机大佬来卷互联网了"], 
    ["https://www.foreverblog.cn/", "https://www.foreverblog.cn/favicon.ico", "@十年之约", "我们的博客十年不关闭，保持活力"], 
    ["https://www.cnblogs.com/hellxz/", "/avatar/hellxz.jpg", "@东北小狐狸", "若你不能簡單解釋一件事，那麼你就是不夠了解它。 <= Java+DevOps"], 
    ["https://stdrc.cc/", "/avatar/richardchien.png", "@Richard Chien", "一只腊鸡的技术成长 <= Nonebot 作者，OS 大佬"], 
    ["https://www.symbk.cn/", "https://q1.qlogo.cn/g?b=qq&nk=2357307393&s=640", "@幸吾有志", "幸于吾志尚存 <= 是个文学家~"], 
];



// 以下为核心功能内容，修改前请确保理解您的行为内容与可能造成的结果
var  targetList = document.getElementById("friendsList");
while (myFriends.length > 0) {
    var rndNum = Math.floor(Math.random()*myFriends.length);
    var friendNode = document.createElement("li");
    var friend_link = document.createElement("a"), 
        friend_img = document.createElement("img"), 
        friend_name = document.createElement("h4"), 
        friend_about = document.createElement("p")
    ;
    friend_link.target = "_blank";
    friend_link.href = myFriends[rndNum][0];
    friend_img.src=myFriends[rndNum][1];
    friend_name.innerText = myFriends[rndNum][2];
    friend_about.innerText = myFriends[rndNum][3];
    friend_link.appendChild(friend_img);
    friend_link.appendChild(friend_name);
    friend_link.appendChild(friend_about);
    friendNode.appendChild(friend_link);
    targetList.appendChild(friendNode);
    myFriends.splice(rndNum, 1);
}
</script>


<style>

.linkpage ul {
    color: rgba(255,255,255,.15)
}

.linkpage ul:after {
    content: " ";
    clear: both;
    display: block
}

.linkpage li {
    float: left;
    width: 48%;
    position: relative;
    -webkit-transition: .3s ease-out;
    transition: .3s ease-out;
    border-radius: 5px;
    line-height: 1.3;
    height: 90px;
    display: block
}

.linkpage h3 {
    margin: 15px -25px;
    padding: 0 25px;
    border-left: 5px solid #51aded;
    background-color: #f7f7f7;
    font-size: 25px;
    line-height: 40px
}

.linkpage li:hover {
    background: rgba(230,244,250,.5);
    cursor: pointer
}

.linkpage li a {
    padding: 0 10px 0 90px
}

.linkpage li a img {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    position: absolute;
    top: 15px;
    left: 15px;
    cursor: pointer;
    margin: auto;
    border: none
}

.linkpage li a h4 {
    color: #333;
    font-size: 18px;
    margin: 0 0 7px;
    padding-left: 90px
}

.linkpage li a h4:hover {
    color: #51aded
}

.linkpage li a h4, .linkpage li a p {
    cursor: pointer;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
    line-height: 1.4;
    margin: 0 !important;
}

.linkpage li a p {
    font-size: 12px;
    color: #999;
    padding-left: 90px
}

@media(max-width: 460px) {
    .linkpage li {
        width:97%
    }

    .linkpage ul {
        padding-left: 5px
    }
}

</style>
