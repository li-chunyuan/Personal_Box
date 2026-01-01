# LaTeX 项目协作准则 (C 语言笔记专项)

当你作为 AI 助手参与本项目时，请严格遵守以下指令，以确保文档逻辑一致、编译通过且排版精美。

## 1. 编译与保存规则 (核心限制)
- **严禁在终端执行任何编译命令**（如 `pdflatex`, `xelatex`, `latexmk` 等）。
- **执行逻辑**：本项目已通过 VS Code 的 LaTeX Workshop 插件配置了自动编译。
- **你的任务**：仅负责编写或修改 `.tex` 代码并**执行保存操作**。所有的 `out/` 重定向、中间文件清理均由用户的 `settings.json` 自动处理。

## 2. 项目目录结构规范
必须维持以下文件层级，禁止随意在根目录创建内容文件：
- **根目录**：仅存放 `main.tex`、`.cursorrules` 及管理配置文件。
- **章节内容**：必须存放在 `latex/chapter[n]/[n.tex]`（例如：`latex/chapter1/1.tex`）。
- **资源与配置**：图片统一存放于 `figures/`，全局宏包与样式定义位于 `latex/config.tex`。

## 3. 环境与格式约束
### 3.1 层次结构与列表规则 (Hierarchy & List Rules)

- **标题层级规范**：文档正文默认遵循三级标题结构（即 `\section` -> `\subsection` -> `\subsubsection`）。
- **三级标题后的分点**：在 `\subsubsection` 之后若需进一步细分内容，必须使用 `enumerate` 环境，并带有参数 `[label={(\arabic*)}]`。
- **三级标题前的决策逻辑**：在未达到三级标题前，若需对内容进行拆解，请根据内容体量选择表现形式：
    - **使用列表环境**：若分点内容仅为寥寥数语、短句或摘要性质，必须使用带有 `[label={(\arabic*)}]` 参数的 `enumerate` 环境。
    - **使用下一级标题**：若分点内容包含大量长句、详细的技术推导或需要多个段落展开论述，必须使用下一级标题。
- **禁令**：在任何情况下，禁止使用 `itemize` 或不带参数的默认 `enumerate`。

**代码示例**：
```latex
% 情境 A：内容简短，使用列表
\subsection{指针定义}
本文定义包含以下要素：
\begin{enumerate}[label={(\arabic*)}]
  \item 类型声明
  \item 地址关联
\end{enumerate}

% 情境 B：内容冗长，使用标题
\subsection{指针进阶}
\subsubsection{多级指针的内存模型}
此处有大量的底层原理解析内容...
  ```

### 3.2 文本样式
- **禁止加粗**：除非用户明确要求，否则禁止在 `\item` 开头自动添加 `\textbf{...}`。
- **风格**：保持技术文档的简洁、专业，避免口语化。

## 4. C 语言代码块规范
- **环境选择**：必须使用 `latex/config.tex` 中定义的 `\begin{lstlisting}` 环境，并显式指定 `language=C`。
- **元数据要求**：每个代码块必须包含 `caption`（中文说明）和 `label`（格式：`lst:关键字`）。
- **示例**：
  ```latex
  \begin{lstlisting}[language=C, caption={指针初始化示例}, label={lst:ptr_init}]
  int *p = NULL;
  \end{lstlisting}
  ```

## 5. 图像与绘图 (Figures & TikZ)
- **TikZ 优先**：对于简单的逻辑框图、内存模型或指针指向图，优先尝试使用 **TikZ** 宏包编写代码生成，而非要求用户上传图片。
- **图片固定**：引用外部图片时，必须使用 `[H]` 参数强制固定位置（需确保 config 中加载了 float 宏包）。
- **题注位置**：图片的 `caption` 必须位于图片**下方**，且必须包含 `label`（格式：`fig:关键字`）。

## 6. 表格规范 (Tables)
- **三线表**：必须使用精美的三线表格式（仅包含 `\toprule`, `\midrule`, `\bottomrule`）。
- **题注位置**：表格的 `caption` 必须位于表格**上方**，且必须包含 `label`（格式：`tab:关键字`）。

## 7. 术语一致性与交叉引用
- **专业术语对照**：
    - 内存布局：堆 (Heap)、栈 (Stack)、常量区 (Data Segment)。
    - 指针操作：解引用 (Dereference)、野指针 (Wild Pointer)。
    - 遇到不确定的词汇，采用 `中文 (English)` 格式。
- **交叉引用 (Cross-Referencing)**：
    - 引用章节：`\ref{sec:...}`
    - 引用代码：`\ref{lst:...}`
    - 引用图片：`\ref{fig:...}`
    - **警告**：严禁捏造不存在的标签名，引用前请结合上下文确认标签是否存在。