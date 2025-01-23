分级医疗资源优化配置模型。这个模型结合了多目标规划、层次分析和模糊评价,既有一定的数学深度,又便于小规模测试。


# 概念

### 1. 基本集合与下标
- 资源类型：$i \in \{1,2,3\}$
- 医院等级：$j \in \{1,2,3\}$

### 2. 变量与参数
**决策变量：**
- $x_{ij}$：i类资源在j级医院的配置数量

**资源参数：**
- $B_i$：i类资源总预算上限
- $w_i$：i类资源权重
- $D_j$：j级医院最低服务需求

**权重参数：**
- $\alpha_j$：效率权重
- $\beta_j$：可及性权重
- $\gamma_j$：成本权重
- $w_1,w_2,w_3$：目标函数权重，满足$\sum_{k=1}^3 w_k = 1$

### 3. 函数定义
**目标函数：**
- 效率：$Z_1 = \sum_{j=1}^{3} \alpha_j E_j(x_{ij})$
- 可及性：$Z_2 = \sum_{j=1}^{3} \beta_j A_j(x_{ij})$
- 成本：$Z_3 = \sum_{j=1}^{3} \gamma_j C_j(x_{ij})$
- 综合：$Z = w_1Z_1 + w_2Z_2 - w_3Z_3$

### 4. 约束条件
1. 资源约束：$\sum_{j=1}^{3} x_{ij} \leq B_i, \forall i$
2. 需求约束：$\sum_{i=1}^{3} w_i x_{ij} \geq D_j, \forall j$
3. 非负约束：$x_{ij} \geq 0, \forall i,j$

### 5. 模糊评价系统
- 评价矩阵：$R = [r_{ij}]_{3×3}$
- 权重向量：$W = [w_1, w_2, w_3]^T$
- 综合评价：$S = W^T \cdot R$

### 6. 最终优化问题
$$
\begin{aligned}
&\max Z = w_1Z_1 + w_2Z_2 - w_3Z_3 \\
&s.t. \begin{cases}
\sum_{j=1}^{3} x_{ij} \leq B_i, &\forall i \\
\sum_{i=1}^{3} w_i x_{ij} \geq D_j, &\forall j \\
x_{ij} \geq 0, &\forall i,j
\end{cases}
\end{aligned}
$$

# 代码架构

```python
📁 medical_resource_optimization/
┣━━ 📁 documents/
┃   ┣━━ 📄 problem_description.md
┃   ┗━━ 📄 mathematical_model.md
┣━━ 📁 test_medical_opt/
┃   ┣━━ 📄 test_01_data_loader.py
┃   ┣━━ 📄 test_02_ahp.py
┃   ┣━━ 📄 test_03_fuzzy.py
┃   ┣━━ 📄 test_04_objective.py
┃   ┣━━ 📄 test_05_constraints.py
┃   ┣━━ 📄 test_06_optimizer.py
┃   ┣━━ 📄 test_07_visualizer.py
┃   ┗━━ 📄 test_08_integration.py
┣━━ 📁 medical_opt/
┃   ┣━━ 📄 __init__.py
┃   ┣━━ 📄 p01_data_loader.py      # 数据加载与预处理
┃   ┣━━ 📄 p02_ahp.py              # AHP权重计算
┃   ┣━━ 📄 p03_fuzzy.py            # 模糊评价系统
┃   ┣━━ 📄 p04_objective.py        # 目标函数实现
┃   ┣━━ 📄 p05_constraints.py      # 约束条件实现
┃   ┣━━ 📄 p06_optimizer.py        # 优化求解器
┃   ┣━━ 📄 p07_visualizer.py       # 结果可视化
┃   ┣━━ 📄 p08_utils.py            # 工具函数
┃   ┗━━ 📄 config.py               # 配置参数
┣━━ 📄 main.py                     # 主程序入口
┣━━ 📄 requirements.txt            # 项目依赖
┗━━ 📄 README.md                   # 项目说明
```