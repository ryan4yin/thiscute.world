---
title: "进程线程协程与并发并行"
date: 2018-01-23T16:39:00+08:00
draft: false

featuredImage: "concurrency-vs-parallelism.webp"
resources:
  - name: featured-image
    src: "concurrency-vs-parallelism.webp"
authors: ["ryan4yin"]

tags: ["进程", "线程", "协程", "并发", "并行", "Coroutines", "Concurrency"]
categories: ["tech"]
---

> 个人笔记，不保证正确。

### 一、进程 Process：（并行运算，分布式）

每一个进程，都可以看作是一个完整的 Program，它有自己完全独立的内容。不与其他进程直接共享数
据。（一个工作(job)可以由多个 process 完成，例如电脑上的qq/360就会有好几个进程，这种程序可
能会有一个守护进程，当主进程挂掉，它会自动重启主进程。）

每个进程可以由多个线程组成。进程抽象由操作系统提供，Linux 是使用 fork 函数，Windows 是用
CreateProcess。

### 二、线程 Thread：（并发执行）

属于同一个进程的线程之间，是共享一套工作内容的。这使得线程的创建和移除开销很小，但同时也使
编程变得复杂。

{{< figure src="/images/process-thread-coroutines-concurrency-parallelism/threads-vs-processes.webp" >}}

关于线程，分用户级线程和内核级线程。不同的语言中，这两种线程的对应关系也不尽相同。

- 多对一模型将多个用户级线程映射到一个内核级线程，线程管理在用户空间完成，这种模型下操作系
  统并不知道多线程的存在。Python 就是这种模型。

  - **优点**：线程管理是在用户空间进行的，切换上下文开销比较小，性能较高。
  - **缺点**：当一个线程在使用内核服务时被阻塞，那么整个进程都会被阻塞；多个线程不能并行地
    运行在多处理机上。

- 一对一模型将每个用户级线程映射到一个内核级线程。Java的线程就属于这种模型。

  - **优点**：当一个线程被阻塞后，允许另一个线程继续执行，所以并发能力较强；能很好的利用到
    CPU的多核心。
  - **缺点**：每创建一个用户级线程都需要创建一个内核级线程与其对应，这样创建线程的开销比较
    大，会影响到应用程序的性能。并且切换线程要进出内核，代价比较大。

- 多对多模型将n个用户级线程映射到m个内核级线程上，要求 m <= n。GO（1.5之后）的协程就属于这
  种线程模型。
  - **特点**：既克服了多对一模型的并发度不高的缺点，又克服了一对一模型的一个用户进程占用太
    多内核级线程，开销太大的缺点。又拥有多对一模型和一对一模型各自的优点。

### 三、协程 Coroutine（并发执行）

如果说线程是轻量级的进程，那么协程就是轻量级的线程。线程跑在进程里，协程就跑在线程里。

优点：

1. 协程是跑在同一个线程里，并且是由程序本身来调度的。协程间的切换就是函数的调用，完全没有
   线程切换那么大的开销。
   - 线程的数量越多，协程的优势越大
1. 因为协程是程序调度的，它实际上是串行运行的，因此不需要复杂的锁机制来保证线程安全。
   - 在协程中控制共享资源不加锁，只需要判断状态就好了。这免去了锁机制带来的开销。

因为协程跑在单个线程内，所占用的 CPU 资源有限，所以多协程**并不能提升计算性能**。不仅如
此，因为多了程序本身的调度开销，计算密集型程序的性能反而会下降。

此外，协程代码中**决不能出现阻塞**，否则整个线程都会停下来等待该操作完成，这就麻烦了。

协程适合用于 IO 密集型任务，可用于简化异步 IO 的 callback hell。例如 Python 的 asyncio 就
是用协程实现的。

### 并发并行

由此，又引出两个名词：

1. 并发（Concurrent）：多个任务交替进行。
1. 并行（Parallel）：多个任务同时进行。

一张图说明两者的差别

{{< figure src="/images/process-thread-coroutines-concurrency-parallelism/concurrency-vs-parallelism.webp" >}}

**Note**：进程 和 线程 都可能是 并发 或 并行 的。关键看你程序的运行状态。多核是并行的前
提。并发则只要求交替执行，因此单核也没问题。

### 同步异步

1. 同步：不同程序单元为了完成某个任务，在执行过程中需靠某种通信方式以协调一致，称这些程序
   单元是同步执行的。
   - 多线程编程中，所有修改共享变量的行为，都必须加锁，保证顺序执行，保证同步。或者加原子
     锁，保证该修改操作是原子的。
   - 同步意味着有序
1. 异步：为完成某个任务，不同程序单元之间过程中无需通信协调，也能完成任务的方式。
   - 不相关的程序单元之间可以是异步的。比如爬虫下载网页
   - 异步意味着无序

- [进程、线程和协程](https://www.cnblogs.com/euphie/p/7008077.html)
