---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
lastmod: {{ .Date }}
draft: true

resources:
- name: "featured-image"
  src: "featured-image.webp"

tags: []
categories: ["tech"]

lightgallery: false

comment:
  utterances:
    enable: true
  waline:
    enable: false
---

TO BE DONE...
