---
title: "欧几里得算法求最大公约数(GCD)的数学原理"
date: 2017-05-26T23:58:53+08:00
draft: false

math: true
featuredImage: "gcd.webp"
authors: ["ryan4yin"]

tags: ["算法"]
categories: ["数学", "tech"]
---

很早就学过欧几里得算法，但是一直不知道它的原理。几乎每本算法书都会提到它，但是貌似只有数学
书上才会见到它的原理。。。

前段时间粗粗看了点数论（《什么是数学》），惊讶于这个原理的奇妙。现在把它通俗地写下来，以免
自己忘记。

欧几里得算法是求两个数的最大公约数(Greatest Common Divisor (GCD))的算法，我们首先假设**有
两个数 $a$ 和 $b$，其中 $a$ 是不小于 $b$ 的数**，

记 $a$ 被 $b$ 除的余数为 $r$，那么 $a$ 可以写成这样的形式：

$$a = bq + r$$

其中 $q$ 是整数（我们不需要去管 $q$ 到底是多少，这和我们的目标无关）。

现在假设 $a$ 和 $b$ 的一个约数为 $u$，那么 $a$ 和 $b$ 都能被 $u$ 整除，即

$$a = su$$ $$b = tu$$

$s$ 和 $t$ 都是整数（同样的，我们只需要知道存在这样的整数 $s$ 和 $t$ 就行）。

这样可以得出

$$r = a - bq = su - (tu)q = (s - tq)u$$

所以 $r$ 也能被 $u$ 整除，一般规律如下

> $a$ 和 $b$ 的约数也整除它们的余数 $r$，所以 $a$ 和 $b$ 的任一约数同时也是 $b$ 和 $r$ 的
> 约数。 —— 条件一

反过来可以得出

> $b$ 和 $r$ 的任一约数同时也是 $a$ 和 $b$ 的约数。 ——条件二

这是因为对 $b$ 和 $r$ 每一个约数 $v$，有

$$b = kv$$

$$r = cv$$

于是有

$$a = bq + r = (kv)q + cv = (kq + c)v$$

由条件一和条件二可知

> $a$ 和 $b$ 的约数的集合，全等于 $b$ 和 $r$ 的约数的集合。

于是

> $a$ 和 $b$ 的最大公约数，就是 $b$ 和 $r$ 的最大公约数。

接下来用递推法，

$a \div b$ 余 $r$，现在设

$b \div r$ 余 $r_1$

$r \div r_1$ 余 $r_2$

……

$r_{n-3} \div r_{n-2}$ 余 $r_{n-1}$

$r_{n-2} \div r_{n-1}$ 余 $r_n=0$

</br>

因为 $a \ge b$，可以看出余数 $r_n$ 会越来越小，最终变成 $0$.

当 $r_{n-1} \neq 0$ 且 $r_n = 0$ 时，可知 $r_{n-2}$ 可被 $r_{n-1}$ 整除（余数为 $0$ 嘛）

此时 $r_{n-2}$ 和 $r_{n-1}$ 的约数就只有：$r_{n-1}$ 和 $r_{n-1}$ 的因数，所以他们的最大公
约数就是 $r_{n-1}$！

所以 $r_{n-1}$ 就是 $a$ 和 $b$ 的最大公约数。（若 $r = 0$，则 $b$ 为最大公约数）

这个递推法写成c语言函数是这样的（比推导更简洁...）:

```c
unsigned int Gcd(unsigned int M,unsigned int N){
    unsigned int Rem;
    while(N){
        Rem = M % N;
        M = N;
        N = Rem;
    }
    return Rem;
}
```

可以发现这里没有要求 `M>=N`，这是因为如果那样，循环会自动交换它们的值。

> P.S. 此外，还有最小公倍数(Least Common Multiple (LCM))算法，详见
> [GCD and LCM calculator](https://www.mathportal.org/calculators/numbers-calculators/gcd-lcm-calculator.php)
