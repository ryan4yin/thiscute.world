---
title: "{{ replace .TranslationBaseName "-" " " | title }}"
subtitle: ""
description: ""
date: {{ .Date }}
lastmod: {{ .Date }}
draft: true

resources:
- name: "featured-image"
  src: "featured-image.webp"

tags: []
categories: ["tech"]
series: []
hiddenFromHomePage: false
hiddenFromSearch: false

lightgallery: false

# 否开启表格排序
table:
  sort: false

toc:
  enable: true

comment:
  utterances:
    enable: true
  waline:
    enable: false
  disqus:
    enable: false
---

TO BE DONE...
