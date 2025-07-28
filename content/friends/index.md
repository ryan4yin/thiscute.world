---
title: "我的小伙伴们"
date: 2021-01-16T00:24:31+08:00
draft: false
hiddenfromsearch: true

comment:
  utterances:
    enable: true
  waline:
    enable: false
---

![一封纸笺](letter-from-friend.webp)

{{< particles_effect_up  >}}

> 感谢 @芝士部落格 提供了友链页面模板~

在友链形成的网络中漫游，是一件很有意思的事情。

**以前的人们通过信笺交流，而我们通过友链串联起一个「世界」。希望你我都能在这个「世界」中有
所收获**

**注：** <span style="color:red;">下方友链次序每次刷新页面随机排列。<span>

<div class="linkpage"><ul id="friendsList"></ul></div>

## 交换友链

{{< admonition type=warning >}} 由于友链数量较多，目前已停止接受友链申请，谢谢！
{{< /admonition >}}

<!-- 有这么几个前提条件：

1. 博客运行时间超过半年，至少有 6 篇自认为有价值的原创文章。如果这个要求都没达到，我会比较担心你的博客能否长期维护下去。
2. 我希望加我友链的朋友们，愿意做个偶尔互访、互相评论两句的博友。如果你只是想多一个外链优化下 SEO，那恕我谢绝添加。
3. 为了能够做到互访，我希望你的博客内容对我也有些吸引力，比如说技术内容比较有意思，或者是有趣的生活类博客。长期不更新的博客，或者内容质量不高的博客，我也会谢绝添加。

可通过 [Issues](https://github.com/ryan4yin/ryan4yin.space/issues) 或者评论区提交友链申请（**但是请注意，我不保证会通过申请**），格式如下：

    站点名称：This Cute World
    站点地址：https://thiscute.world/
    个人形象：https://thiscute.world/avatar/myself.webp
    站点描述：赞美快乐~  -->

<script type="text/javascript">
// 以下为样例内容，按照格式可以随意修改
var myFriends = [
    // ["https://blog.z-xl-t.top/", "https://blog.z-xl-t.top/favicon.jpg", "@薯条流浪法师", "快走吧，趁风停止之前"], 
    ["https://rea.ink/", "/avatar/rea.ink.webp", "@倾书", "清风皓月，光景常新 <= 前端"], 
    ["https://jdragon.club/", "/avatar/jdragon.webp", "@谭宇", "Hello world! <= Java"], 
    ["https://nopdan.com/", "https://nopdan.com/avatar.webp", "@单单", "但知行好事，莫要问前程"], 
    ["https://farer.org/", "/avatar/farer.webp", "@Stray Episode", "Scientific Evocation"], 
    ["https://wasteland.touko.moe", "https://wasteland.touko.moe/images/avatar.png", "@Touko Hoshino", "My Exploration, My Whisper"], 
    ["https://blog.k8s.li/", "/avatar/muzi.webp", "@木子", "垃圾佬、搬砖社畜、运维工程师 <= 莫得感情的读书机器"], 
    ["https://www.addesp.com", "https://www.addesp.com/avatar", "@ADD-SP", "记录 & 分享 & 感受 <= 网络协议"], 
    ["https://tianheg.co/", "/avatar/tianheg.webp", "@一大加贝", "学习技术，热爱生活"], 
    ["https://guanqr.com/", "https://cdn.jsdelivr.net/gh/guanqr/blog/static/icons/android-chrome-512x512.png", "@荷戟独彷徨", "爱光学，爱生活，爱创造"], 
    // 无法访问 SSL_ERROR_RX_RECORD_TOO_LONG ["https://exploro.one", "https://avatars.githubusercontent.com/u/4038871?s=460&u=d2f1c2eea96acb15578f2e513ba5fa673aa3d250&v=4", "@探索子", "Learn by doing. <= 硬核数学"], 
    ["https://panqiincs.me/", "https://panqiincs.me/images/avatar.jpg", "@辛未羊", "人生如逆旅，我亦是行人 <= 信号系统"], 
    ["https://a-wing.top/", "https://a-wing.top/assets/avatar.png", "@新一", "Hi! 上天不? <= 无人机大佬来卷互联网了"], 
    ["https://www.cnblogs.com/hellxz/", "/avatar/hellxz.webp", "@东北小狐狸", "若你不能簡單解釋一件事，那麼你就是不夠了解它。"], 
    ["https://stdrc.cc/", "/avatar/richardchien.webp", "@Richard Chien", "一只腊鸡的技术成长 <= Nonebot作者/OS大佬"], 
    ["https://fmcf.cc/", "https://q1.qlogo.cn/g?b=qq&nk=2357307393&s=640", "@我的飛鳥集", "他戴着花冠，踏于风雪，探寻迷途的救赎，绽放生命的曙光"], 
    ["https://www.lionad.art/", "/avatar/lionad-morotar.webp", "@仿生狮子", "前端攻城狮 | 砸吉他 | 午夜恶魔 | 兴趣泛滥 | 逃离地球"], 
    ["https://naccl.top/", "https://naccl.top/img/avatar.jpg", "@Naccl", "游龙当归海，海不迎我自来也。"], 
    ["https://ilimeng.cn/", "https://ilimeng.cn/SLiMan.png", "@离梦", "一个记性不好的00后博主"], 
    ["https://www.eatrice.cn", "/avatar/eatrice.jpg", "@吃白饭的休伯利安号", "非专业搬砖的土木工程师"], 
    ["https://blog.010sec.cn/", "/avatar/c4rt1y.webp", "@c4rt1y", "<= 运维搬砖人"], 
    ["https://ferryxie.com/", "/avatar/ferryxie.webp", "@Ferry", "金融科技与人文思考并存"], 
    ["https://imcbc.cn/", "https://imcbc.cn/apple-touch-icon.png", "@BBing", "自由 分享 合作 <= C/C++/Linux 高手"], 
    ["https://blognas.hwb0307.com/", "https://blognas.hwb0307.com/logo.jpg", "@Bensz", "浮云翩迁之间 <= Linux/Docker/R语言爱好者"], 
    ["https://lisenhui.cn", "https://lisenhui.cn/imgs/avatar.png", "@凡梦星尘", "再平凡的人也有属于他的梦想！"], 
    ["https://blog.li2niu.com/", "https://blog.li2niu.com/img/logo.png", "@李二牛", "Addicted to marathons <= Developer & Runner"], 
    ["https://wiki.eryajf.net/", "https://wiki.eryajf.net/img/logo.png", "@二丫讲梵", "💻学习📝记录🔗分享 <= 运维领域的前辈"], 
    [" https://zhsher.cn/", " https://q1.qlogo.cn/g?b=qq&nk=1310446718&s=5", "@张时贰", "环转码，爱敲代码的小张！<= 很有干劲的后辈"], 
    ["https://tftree.top/", "https://cdn.tftree.top/i/wp-content/uploads/2022/07/TFTree_avatar.png", "@虚空裂隙", "心有猛虎,细嗅蔷薇"], 
    ["https://zgq.me/", "https://zgq.me/favicon.png", "@zgq354", "多一些思考与记录 <= 0xffff 站长，前端佬"], 
    ["https://bleatingsheep.org/", "https://bleatingsheep.org/favicon.ico", "@bleatingsheep", "偶像咩咩"], 
    ["https://vian.top/", "https://www.vian.top/avatar.ico", "@Vian", "想要的都拥有，得不到的都释怀..."], 
    ["https://wangyunzi.com/", "https://blog.wangyunzi.com/avatar.png", "@王云子", "此行山高路远，我只剩口袋玫瑰一片 <= 法学在读的文艺少女"], 
    ["https://wenderfeng.top/", "https://wenderfeng.top/favicon.ico", "@wenderfeng", "Step by step <= 机械 PhD 在读的机器人玩家"], 
    ["https://lado.me", "https://lado.me/static/img/gravatar-black.png", "@啦哆咪", "用 Linux 做音乐"], 
    ["https://sxyz.blog/", "/avatar/sxyazi.jpg", "@三咲雅 · Misaki Masa", "四時行焉，百物生焉，天何言哉？"],
    ["https://blog.youmuwhisper.space/", "https://blog.youmuwhisper.space/images/avatar.jpg", "@芝士部落格", "有思想，也有忧伤和理想，芝士就是力量"], 
    ["https://raxcl.cn/", "https://raxcl.cn/img/avatar.jpg", "@raxcl", "剑未佩妥，出门已是江湖。"], 
    ["https://www.xuezhao.space/", "https://www.xuezhao.space/apple-touch-icon.png", "@碎冰冰", "挥剑破云迎星落，举酒高歌引凤游。"], 

    ["https://blog.ny4.dev/", "/avatar/guanran928.png", "@Guanran928", "&'a ::ny4::Blog"], 
    ["https://prince213.top/", "/avatar/prince213.png", "@prince213", "Ad astra abyssosque!"], 
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
