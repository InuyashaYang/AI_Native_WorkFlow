# p07_visualizer.py

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Tuple
import logging

class Visualizer:
    """可视化类，用于展示优化结果和相关数据"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        sns.set(style="whitegrid")

    def plot_pareto_front(self, objectives: np.ndarray, save_path: str = None) -> None:
        """
        绘制帕累托前沿

        Args:
            objectives (np.ndarray): 目标函数值数组，形状为 (n_samples, n_objectives)
            save_path (str, optional): 图像保存路径。如果为 None，则不保存。
        """
        try:
            plt.figure(figsize=(10, 6))
            plt.scatter(objectives[:, 0], objectives[:, 1], c='blue', marker='o', label='Pareto Front')
            plt.xlabel('效率损失 (Efficiency Loss)')
            plt.ylabel('可及性损失 (Accessibility Loss)')
            plt.title('Pareto Front')
            plt.legend()
            plt.tight_layout()
            if save_path:
                plt.savefig(save_path)
                self.logger.info(f"帕累托前沿图已保存至 {save_path}")
            plt.show()
        except Exception as e:
            self.logger.error(f"绘制帕累托前沿图时出错: {str(e)}")

    def plot_resource_allocation(self, allocation_matrix: np.ndarray, hospital_levels, resource_types, save_path: str = None) -> None:
        """
        绘制资源分配热图

        Args:
            allocation_matrix (np.ndarray): 资源分配矩阵，形状为 (n_resources, n_hospitals)
            hospital_levels (Dict): 医院等级字典
            resource_types (Dict): 资源类型字典
            save_path (str, optional): 图像保存路径。如果为 None，则不保存。
        """
        try:
            plt.figure(figsize=(12, 8))
            sns.heatmap(allocation_matrix, annot=True, fmt=".2f", cmap="YlGnBu",
                        xticklabels=[f'Level {k}: {v}' for k, v in hospital_levels.items()],
                        yticklabels=[f'Type {k}: {v}' for k, v in resource_types.items()])
            plt.xlabel('医院等级')
            plt.ylabel('资源类型')
            plt.title('资源分配热图')
            plt.tight_layout()
            if save_path:
                plt.savefig(save_path)
                self.logger.info(f"资源分配热图已保存至 {save_path}")
            plt.show()
        except Exception as e:
            self.logger.error(f"绘制资源分配热图时出错: {str(e)}")

    def plot_objective_trends(self, history, save_path: str = None) -> None:
        """
        绘制目标函数值的变化趋势

        Args:
            history (List[Tuple[float, float, float]]): 历史目标函数值
            save_path (str, optional): 图像保存路径。如果为 None，则不保存。
        """
        try:
            history = np.array(history)
            plt.figure(figsize=(10, 6))
            plt.plot(history[:, 0], label='效率损失')
            plt.plot(history[:, 1], label='可及性损失')
            plt.plot(history[:, 2], label='成本损失')
            plt.xlabel('迭代次数')
            plt.ylabel('目标函数值')
            plt.title('目标函数值变化趋势')
            plt.legend()
            plt.tight_layout()
            if save_path:
                plt.savefig(save_path)
                self.logger.info(f"目标函数变化趋势图已保存至 {save_path}")
            plt.show()
        except Exception as e:
            self.logger.error(f"绘制目标函数变化趋势图时出错: {str(e)}")

# 示例使用
if __name__ == "__main__":
    import numpy as np
    from config import HOSPITAL_LEVELS, RESOURCE_TYPES

    logging.basicConfig(level=logging.INFO)

    visualizer = Visualizer()

    # 假设有一些模拟数据
    pareto_objectives = np.random.rand(50, 3)  # (效率损失, 可及性损失, 成本损失)
    allocation_matrix = np.random.rand(3, 3) * 100

    # 绘制帕累托前沿
    visualizer.plot_pareto_front(pareto_objectives[:, :2], save_path="pareto_front.png")

    # 绘制资源分配热图
    visualizer.plot_resource_allocation(allocation_matrix, HOSPITAL_LEVELS, RESOURCE_TYPES, save_path="resource_allocation.png")

    # 绘制目标函数变化趋势
    history = [tuple(np.random.rand(3)) for _ in range(100)]
    visualizer.plot_objective_trends(history, save_path="objective_trends.png")
