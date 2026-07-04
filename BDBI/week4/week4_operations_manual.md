# Week 4 操作手册 — Power BI 数据分析（Data Analytics）

适用范围：仅 Week 4 实验（BusinessData 数据集：拆表、建立关系、制作可视化）。
使用软件：**Microsoft Power BI Desktop**（运行在阿里云无影云电脑 / Alibaba Cloud Workspace 的 Windows 远程桌面上）。
源文件：`BusinessData.xlsx`（本地 Mac 路径 `BDBI/week4/lab/BusinessData.xlsx`，已复制到远程桌面 `C:\Users\admin\Desktop\AI\BDBI\Week4\lab\`）。
成果文件：`BDBI-week4-lab.pbix`（已同步回 Mac 本地 `BDBI/week4/lab/` 文件夹），内含两个页面：
- **Page 1**：Task 12 要求的四类基础可视化（趋势/类别/对比图 + 切片器 + 洞察文本框）。
- **Dashboard**：按导师提供的参考图 `Capture.JPG`（EXIF 作者 Occhipinti, Annalisa）重做的完整仪表盘页，见第八节。

---

## 一、准备工作

1. 打开「Cloud Computer」远程桌面 App，连接阿里云无影云电脑（Windows 桌面）。
2. 在远程桌面上确认文件夹 `C:\Users\admin\Desktop\AI\BDBI\Week4\lab\` 中已有 `BusinessData.xlsx`。
   - 如果没有，从 Mac 的 Finder 中把文件拖拽/复制（Ctrl+C / Cmd+V 在 Explorer 与 Finder 之间可直接跨系统复制粘贴）到远程桌面对应文件夹。
3. 双击远程桌面上的 **Power BI Desktop** 图标启动软件。

---

## 二、Task 1 — 用 Power Query 把 BusinessData 拆分为 4 张表

BusinessData.xlsx 是一张「宽表」，包含员工、项目、工时、预算等混合列。目标是拆成 4 张规范化的表：`CompanyEmployee`、`ProjectHours`、`CompanyProject`、`ProjectBudget`。

### 2.1 导入数据

1. 功能区（Ribbon）→ **Home** 选项卡 → 点击 **Get data**（获取数据）按钮。
2. 下拉菜单中选择 **Excel workbook**（Excel 工作簿）。
3. 在弹出的 Windows 文件选择框中，导航到 `C:\Users\admin\Desktop\AI\BDBI\Week4\lab\BusinessData.xlsx`，点击 **Open**。
4. 在 **Navigator**（导航器）对话框中，勾选源工作表左侧的复选框。
5. 点击底部的 **Transform Data**（转换数据），进入 Power Query 编辑器（不要直接点 Load，因为后续要拆分列）。

### 2.2 创建 4 个查询（Query）

在 Power Query 编辑器左侧「Queries」面板中，对原始查询重复以下操作 4 次（每次针对一张目标表）：

1. 右键点击原始查询名称 → 选择 **Duplicate**（复制）。
2. 双击新复制出来的查询名称（或在右侧 **Query Settings** 面板的 **Name** 输入框中），重命名为目标表名：
   - `CompanyEmployee`
   - `ProjectHours`
   - `CompanyProject`
   - `ProjectBudget`

### 2.3 每张表只保留需要的列

对每个查询执行：

1. 功能区 → **Home** → **Manage Columns** 组 → 点击 **Choose Columns** 下拉按钮 → **Choose Columns...**。
2. 在弹出的对话框中，只勾选该表需要的列，取消勾选其余列，点击 **OK**。
   - `CompanyEmployee`：`EmployeeName`、`EmployeeTenure`、`EmployeeCity`
   - `ProjectHours`：`Ticket`、`EmployeeName`、`Hours`、`Project Name`、`DateSubmit`
   - `CompanyProject`：`Project Name`、`Priority`
   - `ProjectBudget`：`Project Name`、`BudgetAllocation`、`AllocationDate`
3. 如有需要，双击列标题可直接重命名列名。

### 2.4 去重与清理空值

1. `CompanyEmployee`、`CompanyProject`：右键点击关键列的列标题 → 选择 **Remove Duplicates**（删除重复项），把宽表中每行重复出现的员工/项目信息去重成唯一列表。
2. `ProjectBudget`：点击列标题右侧的下拉筛选按钮 → 取消勾选 `(null)`，过滤掉空的预算行；然后同样执行 **Remove Duplicates** 去重。

结果行数核对：`CompanyEmployee` 6 行、`ProjectHours` 11 行、`CompanyProject` 6 行、`ProjectBudget` 3 行。

### 2.5 应用更改

1. 功能区 → **Home** → 点击 **Close & Apply**（关闭并应用）。
2. 等待底部进度条中的「Apply changes」处理完成。
3. 出现 **Load** 对话框，确认每张表显示 "Schema synchronized"（架构已同步）后自动进入报表视图。

---

## 三、Task 2 — 建立表间关系（Model 视图）

1. 点击软件左侧竖排图标栏中的 **Model view**（模型视图，表格/关系图图标）。
2. Power BI 会根据同名列自动创建关系连线，检查是否生成了 3 条关系：
   - `ProjectHours` — `CompanyProject`（通过 `Project Name`）
   - `CompanyProject` — `ProjectBudget`（通过 `Project Name`）
   - `CompanyEmployee` — `ProjectHours`（通过 `EmployeeName`）
3. **关键修正步骤**：双击 `ProjectHours` 与 `CompanyProject` 之间的关系连线，打开 **Edit relationship**（编辑关系）对话框：
   - 确认 **Cardinality**（基数）为 Many to one（多对一）。
   - 把 **Cross filter direction**（交叉筛选方向）从默认的 **Single**（单向）改为 **Both**（双向）。
   - 点击 **Save**。
   - 原因：如果保持单向，`CompanyEmployee` 的筛选（如城市切片器）无法穿透到 `CompanyProject`/`ProjectBudget`，会导致按 Priority 汇总预算时数据不正确。
4. 其余两条关系保持默认设置不变（`CompanyProject`—`ProjectBudget` 为一对一/双向；`CompanyEmployee`—`ProjectHours` 为多对一/单向）。

---

## 四、Task 12 — 制作四类必需可视化（Report 视图）

点击左侧竖排图标栏中的 **Report view**（报表视图）回到画布，逐一添加以下可视化。每次新建可视化的通用操作：

1. 在画布空白处点击一下，取消任何已选中对象。
2. 在右侧 **Visualizations**（可视化）面板的 **Build visual** 标签下，点击对应图表类型图标。
3. 从最右侧 **Data**（数据）面板中，把需要的字段拖拽/勾选进图表下方出现的「字段井」（如 X-axis、Y-axis、Legend、Values 等）。

### 4.1 趋势图（Trend）— 折线图

- 图表类型：**Line chart**（折线图）。
- 字段：**X-axis** = `ProjectHours[DateSubmit]`（自动生成年/季/月/日层级，本次使用 Year）；**Y-axis** = `ProjectHours[Hours]`（求和）。
- 标题自动显示为 "Sum of Hours by Year"。

### 4.2 类别图（Category）— 簇状柱形图

- 图表类型：**Clustered column chart**（簇状柱形图）。
- 字段：**X-axis** = `ProjectHours[Project Name]`；**Y-axis** = `ProjectHours[Hours]`（求和）。
- 标题自动显示为 "Sum of Hours by Project Name"。

### 4.3 对比图（Comparison）— 簇状条形图

- 图表类型：**Clustered bar chart**（簇状条形图）。
- 字段：**Y-axis（类别轴）** = `CompanyProject[Priority]`；**X-axis（数值轴）** = `ProjectBudget[BudgetAllocation]`（求和）。
- 标题自动显示为 "Sum of BudgetAllocation by Priority"（该图能正确按 Priority 聚合预算，正是因为第三节中把交叉筛选方向改成了 Both）。

### 4.4 筛选器（Slicer）

- 图表类型：**Slicer**（切片器）— 在 Build visual 图标网格中找到带有「Field」字段井和勾选框预览样式的图标。
- 字段：**Field** = `CompanyEmployee[EmployeeCity]`。
- 效果：画布上出现 Redmond / San Jose 两个复选框，勾选后可联动筛选其余图表。

### 4.5 业务洞察文本框（Insight）

1. 功能区 → **Insert** 选项卡 → 点击 **Text box**（文本框）。
2. 在画布上拖出一个文本框区域，直接输入洞察文字，例如：
   > "Priority A has the lowest budget while Green Priority C uses the most hours. Review budget and staffing alignment with priority."
3. 如需移动文本框位置：用鼠标在文本内容区域按住并直接拖动（单击会进入编辑模式，需要用「按住拖动」而不是「点击后再点击」）。
4. 点击画布空白处退出编辑。

---

## 五、保存并同步文件

### 5.1 在远程桌面保存 .pbix

1. 按 **Ctrl+S**（对应 Mac 端 Cmd+S 会被远程会话捕获为 Ctrl+S）。
2. 弹出 **Save this file** 对话框 → 点击 **More options**。
3. 进入「Save a copy」后台视图 → 点击 **Browse this device**。
4. 在原生 **Save As** 对话框中，导航到 `C:\Users\admin\Desktop\AI\BDBI\Week4\lab\`，文件名输入 `BDBI-week4-lab`，点击 **Save**。
5. 标题栏显示 "Last saved: Today at ..." 即保存成功。

### 5.2 把 .pbix 复制回 Mac 本地文件夹

1. 在远程桌面打开 **File Explorer**（文件资源管理器，任务栏图标）。
2. 在「Recent files」或直接导航到 `C:\Users\admin\Desktop\AI\BDBI\Week4\lab\`，找到 `BDBI-week4-lab.pbix`。
3. 点击选中该文件 → 按 **Ctrl+C** 复制。
4. 切换到 Mac 的 **Finder**（Dock 中最左侧的笑脸图标；如果 Dock 被远程会话窗口遮挡，把鼠标移到屏幕最底部边缘即可唤出）。
5. 在 Finder 中用 **Cmd+Shift+G**（前往文件夹）输入 `/Users/hualee/workspace/Applied-AI/BDBI/week4/lab`，回车进入该目录。
6. 在文件列表空白处点击一下，按 **Cmd+V** 粘贴。
7. 确认 `BDBI-week4-lab.pbix` 出现在 Mac 本地的 `BDBI/week4/lab/` 文件夹中，即完成同步。

> 提示：远程 Windows 会话与本地 Mac 之间的**文件**复制粘贴（Explorer ↔ Finder）可以直接、即时生效；但**文本内容**的剪贴板同步（例如在网页里复制一段文字再粘贴到远程应用里）延迟很大且不可靠，不要用它来做文字输入，应使用远程应用内的原生录入方式。

---

## 六、每个可视化说明什么（Lab Checklist 对应）

- **折线图（Sum of Hours by Year）**：展示项目工时随时间的变化趋势。
- **簇状柱形图（Sum of Hours by Project Name）**：按项目对比各项目消耗的工时类别分布。
- **簇状条形图（Sum of BudgetAllocation by Priority）**：按优先级对比预算分配，用于对比分析。
- **切片器（EmployeeCity）**：按员工所在城市筛选整页报表。
- **业务洞察文本框**：指出 Priority A 预算最低，而 Priority C（Green）消耗工时最多，提示需要重新审视预算与人力投入是否与优先级匹配 —— 这是本次实验识别出的可执行业务洞察（actionable business insight）。

---

## 七、常见问题与修复方法（本次实操中遇到的）

- **远程桌面里批量输入文字会出现乱码**（例如整段文字变成一串重复字符）：改为逐个字符发送按键，数字键前先按一次 Escape 再按数字。
- **Choose Columns 对话框里勾选状态看起来不对**：先把鼠标移开复选框再截图确认，避免因为「悬停态」误判勾选情况。
- **文本框无法整体拖动，只会进入编辑模式**：改用「鼠标按下→移动→松开」的一次性拖动手势（而不是先点击选中再拖动）。
- **保存对话框里点了 More options 却跳到了完整的后台视图**：用后台视图左上角的 **Back**（返回）箭头回到报表画布，不要点 Home（会跳转到 Power BI 起始页）。

---

## 八、Dashboard 页 — 按参考图重建完整仪表盘

背景：`lab` 文件夹中原本就存放着两张参考截图 `Capture.JPG`、`Capture_2.JPG`。经 EXIF/XMP 元数据核查，确认作者为 **Occhipinti, Annalisa**（创建时间 2022-10-22），属于导师提供的目标效果图，而非误放文件。因此在 Page 1 之外新建了一个 **Dashboard** 页，尽量在数值上精确复现 `Capture.JPG`。

### 8.1 新建页面并应用深色主题

1. 点击页面标签栏最右侧的 **+**（新增页面），新页面自动命名为 "Page 2"；双击标签重命名为 `Dashboard`。
2. 功能区 → **View** 选项卡 → **Themes**（主题）→ 在主题库中选择 **Innovate**（深灰底色的深色主题），应用到整份报表（两个页面共用同一主题）。

### 8.2 四个 KPI 卡片（Card 新样式）

对每个指标重复：Build visual → **Card**（新版卡片，字段井为 Value/Categories/Tooltips）→ 把字段拖入 **Value**：

| 卡片 | 字段 | 聚合方式 | 显示值 |
|---|---|---|---|
| Total Work Hours | `ProjectHours[Hours]` | Sum | 256 |
| Budget Allocation | `ProjectBudget[BudgetAllocation]` | Sum | 190K |
| Number of Projects | `ProjectBudget[Project Name]` | Count（点字段下拉箭头，从默认的 First 改成 Count） | 6 |
| Total Employees | `CompanyEmployee[EmployeeName]` | Count Distinct | 6 |

四张卡片水平排列在页面顶部，标题栏文字直接用字段默认标题（Sum of Hours / Sum of Budg... / Count of Proj... / Count of Em...）。

### 8.3 Treemap — Project Work Hours

1. Build visual → **Treemap**（注意图标网格中容易和 Scatter/Pie 图标混淆，把鼠标悬停在图标上看 tooltip 文字确认是 "Treemap"）。
2. 字段：**Category** = `ProjectHours[Project Name]`；**Values** = `ProjectHours[Hours]`（Sum）。
3. 标题改为 "Project Work Hours"（Format visual → General → Title → Text）。
4. 结果：Green 63 / Purple 51 / Yellow 44 / Orange 41 / Blue 31 / Red 26，色块大小对应工时。

### 8.4 Donut chart — Project Budget Allocation

1. Build visual → **Donut chart**（同样注意区分 Pie chart，用 tooltip 确认）。
2. 字段：**Legend** = `ProjectBudget[Project Name]`；**Values** = `ProjectBudget[BudgetAllocation]`（Sum）。
3. 标题改为 "Project Budget Allocation"。
4. 结果：Red $100K（52.6%）/ Green $50K（26.3%）/ Blue $40K（21.1%）。

### 8.5 Allocated Number of Projects by Cities（用簇状柱形图替代原图的 dot plot）

这是唯一需要额外核对源数据才能对上数字的图。

1. Build visual → **Clustered column chart**。
2. 字段：**X-axis** = `CompanyEmployee[EmployeeCity]`；**Y-axis** = `ProjectBudget[Project Name]`（Count）。
3. **关键点**：Y 轴必须使用 `ProjectBudget[Project Name]`（只有 3 个项目：Blue/Red/Green），而不是 `ProjectHours[Project Name]`（6 个项目）。用后者会得到 Redmond=6、San Jose=5（因为员工-工单关系把全部 6 个项目都联到了每个城市），对不上参考图的 Redmond=3、San Jose=2。用 `BusinessDataAllTables.xlsx` 反查后确认参考图统计的是"该城市员工可关联到的、且有预算记录的项目数"，即以 ProjectBudget 表（3 行）为准。
4. 标题改为 "Allocated Number of Projects by Cities"。
5. 结果：Redmond=3，San Jose=2。

### 8.6 Employee Work Hours（簇状条形图）

- 字段：**Y-axis（类别）** = `CompanyEmployee[EmployeeName]`；**X-axis（数值）** = `ProjectHours[Hours]`（Sum）。
- 结果：Bowen 66 / Brewer 61 / Ito 56 / Bento 35 / Han 28 / Hamilton 10。

### 8.7 Employee Experience（簇状条形图）

- 字段：**Y-axis（类别）** = `CompanyEmployee[EmployeeName]`；**X-axis（数值）** = `CompanyEmployee[EmployeeTenure]`（Sum）。
- 结果：Bento 15 / Brewer 15 / Bowen 10 / Hamilton 3 / Han 1 / Ito 1。

### 8.8 Project Submission Dates（表格）

1. Build visual → **Table**。
2. **Columns** 依次加入：`ProjectBudget[Project Name]`、`ProjectBudget[BudgetAllocation]`（Sum）、`ProjectBudget[AllocationDate]`、`ProjectHours[DateSubmit]`。
3. 标题改为 "Project Submission Dates"。
4. 结果：5 行数据（Blue/Blue/Green/Green/Red）+ Total 行合计 190000，与参考图一致。

**AllocationDate 显示成年/季/月/日层级的问题与修复**：默认情况下 Power BI 的「Auto date/time」功能会自动把日期字段拆成层级，导致表格列显示成嵌套的 Year > Quarter > Month > Day 而不是原始日期值。修复方法：

1. 功能区 → **File**（后台视图）→ **Options and settings** → **Options**。
2. 左侧栏切换到 **CURRENT FILE** 分组下的 **Data Load**。
3. 取消勾选 **Auto date/time**，点击 **OK**。
4. 回到画布，把 AllocationDate 从 Columns 字段井中移除后重新加入，即可显示为原始日期值（不再带展开箭头）。

### 8.9 所有图表的尺寸与位置（Format visual → General → Properties / Position）

每个可视化选中后，在右侧 Format visual 面板：

1. 点击 **Properties** 展开 → 在 **Height** / **Width** 输入框中分别输入数值（如遇远程会话卡顿导致输错，务必用 zoom 截图核对每个数值再进入下一个字段）。
2. 点击 **Position** 展开 → 在 **Horizontal** / **Vertical** 输入框中输入坐标。
3. 布局参考（按参考图三行排布）：顶部 KPI 卡一行；第二行 Treemap / Donut / 城市对比图；第三行 Employee Work Hours / Employee Experience / Project Submission Dates 表格（大致 Horizontal=10/340/670，Vertical=470，Width≈300-320，Height≈230）。

### 8.10 标题文本框输入的常见坑

远程会话里连续用 `type` 工具输入英文标题时，偶尔会出现整段文字被替换成单一重复字符（例如输入 "Project Submission Dates" 结果变成一串 "a"）。可靠做法：

- 改用**逐字符**发送按键（每个字母单独一次 `key` 调用），大写字母用 `shift+字母`（如 `shift+p`）而不是直接发送大写字母键名。
- 每输入完一个词组，用 `Home`/`End` 移动光标后截图（zoom 局部区域）核对文字，确认无误再继续。

---

## 九、Dashboard 页保存并同步

保存与同步步骤与第五节完全一致（Ctrl+S 保存 → File Explorer 复制 → Finder 粘贴替换），保存时会看到 "An older item named 'BDBI-week4-lab.pbix' already exists... Replace it with the newer one?" 提示，选择 **Replace** 覆盖旧版本即可。
