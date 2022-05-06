---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
lastmod: {{ .Date }}
draft: true

resources:
- name: "featured-image"
  src: "featured-image.webp"

tags: []
categories: ["技术"]

lightgallery: false

comment:
  utterances:
    enable: true
  waline:
    enable: false
---

TO BE DONE...
