@"
# 大连交通大学毕业论文 LaTeX 模板（DJTU Thesis Template）

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

---

## 📘 项目简介

本项目是 **大连交通大学毕业论文（设计）LaTeX 模板** 的开源实现，旨在帮助在校学生快速撰写、排版并生成符合学校要求格式的毕业论文 PDF 文件。

---

## ✨ 特性

- 📄 支持中英文排版（`ctex`）
- 🎓 自动生成封面、目录、摘要、参考文献等
- 🧩 模块化章节设计
- 💡 兼容 VS Code + LaTeX Workshop 一键编译
- 🔖 符合大连交通大学论文格式要求

---

## ⚙️ 使用方法

1. 克隆仓库/ Clone the repo：
   ```bash
   git clone https://github.com/<你的GitHub用户名>/DJTU-Thesis-Template.git
   cd DJTU-Thesis-Template


2. 编译主文件 / Compile main file
    xelatex main.tex
    bibtex main
    xelatex main.tex
    xelatex main.tex

3. 生成论文 PDF
    输出文件为 main.pdf


    依赖环境 | Requirements

    TeX Live / MikTeX (≥ 2022)

    编译器：xelatex

    宏包：ctex, geometry, biblatex, graphicx, fancyhdr, titlesec


    📜 开源协议 | License

    本项目采用 CC BY-NC-SA 4.0 国际许可协议。
    允许学习与引用，但禁止商业用途。
    详情请参见 LICENSE


    作者 / Author: ChunYuan
    版本 / Version: 1.0
    发布日期 / Released: 2025年11月