"""
约束条件模块 (p05_constraints.py)
定义医疗资源优化问题中的约束条件，用于确保优化解的可行性。
"""

import numpy as np
from typing import Dict, Tuple

class Constraints:
    """
    约束条件类
    """

    def __init__(self, budget_config: Dict, hospital_levels: Dict):
        """
        初始化约束条件类

        Args:
            budget_config (Dict): 包含预算限制、需求阈值和单位成本的配置。
            hospital_levels (Dict): 医院等级配置。
        """
        self.budget_limits = budget_config["BUDGET_LIMITS"]
        self.demand_thresholds = budget_config["DEMAND_THRESHOLDS"]
        self.unit_costs = budget_config["UNIT_COSTS"]
        self.hospital_levels = hospital_levels

    def budget_constraint(self, allocation_matrix: np.ndarray) -> bool:
        """
        检查预算约束是否满足。

        Args:
            allocation_matrix (np.ndarray): 资源分配矩阵 (resource_type × hospital_level)，
                                            每个元素表示分配的资源数量。

        Returns:
            bool: 是否满足预算约束。
        """
        try:
            # 计算每种资源的总成本
            total_costs = np.zeros(len(self.budget_limits))
            for resource_type, costs in self.unit_costs.items():
                for hospital_level in range(allocation_matrix.shape[1]):
                    total_costs[resource_type - 1] += (
                        allocation_matrix[resource_type - 1, hospital_level] *
                        sum(costs.values())  # 单位成本之和
                    )

            # 检查总成本是否在预算限制内
            for resource_type, total_cost in enumerate(total_costs, start=1):
                if total_cost > self.budget_limits[resource_type]:
                    return False

            return True

        except Exception as e:
            print(f"Error in budget constraint: {str(e)}")
            return False

    def demand_constraint(self, allocation_matrix: np.ndarray, demand_matrix: np.ndarray) -> bool:
        """
        检查资源分配是否满足医院的最低需求。

        Args:
            allocation_matrix (np.ndarray): 资源分配矩阵 (resource_type × hospital_level)。
            demand_matrix (np.ndarray): 医院需求矩阵 (hospital_level × 1)。

        Returns:
            bool: 是否满足需求约束。
        """
        try:
            # 计算每个医院等级的分配资源总量
            allocated_resources = np.sum(allocation_matrix, axis=0)

            # 检查是否满足每个医院等级的最低需求
            for hospital_level, allocated in enumerate(allocated_resources, start=1):
                if allocated < self.demand_thresholds[hospital_level]:
                    return False

            return True

        except Exception as e:
            print(f"Error in demand constraint: {str(e)}")
            return False

    def non_negativity_constraint(self, allocation_matrix: np.ndarray) -> bool:
        """
        检查非负性约束：所有资源分配数量必须为非负数。

        Args:
            allocation_matrix (np.ndarray): 资源分配矩阵 (resource_type × hospital_level)。

        Returns:
            bool: 是否满足非负性约束。
        """
        try:
            return np.all(allocation_matrix >= 0)
        except Exception as e:
            print(f"Error in non-negativity constraint: {str(e)}")
            return False

    def validate_constraints(self, allocation_matrix: np.ndarray, demand_matrix: np.ndarray) -> bool:
        """
        验证所有约束条件是否满足。

        Args:
            allocation_matrix (np.ndarray): 资源分配矩阵 (resource_type × hospital_level)。
            demand_matrix (np.ndarray): 医院需求矩阵 (hospital_level × 1)。

        Returns:
            bool: 是否满足所有约束条件。
        """
        try:
            return (
                self.budget_constraint(allocation_matrix) and
                self.demand_constraint(allocation_matrix, demand_matrix) and
                self.non_negativity_constraint(allocation_matrix)
            )
        except Exception as e:
            print(f"Error in validating constraints: {str(e)}")
            return False


# 测试代码
if __name__ == "__main__":
    # 示例配置
    from .config import BUDGET_CONFIG, HOSPITAL_LEVELS

    # 初始化约束条件类
    constraints = Constraints(BUDGET_CONFIG, HOSPITAL_LEVELS)

    # 示例分配矩阵 (3种资源 × 3个医院等级)
    allocation_matrix = np.array([
        [50, 40, 30],  # 医疗设备分配
        [60, 50, 40],  # 医护人员分配
        [20, 15, 10]   # 床位资源分配
    ])

    # 示例需求矩阵 (3个医院等级)
    demand_matrix = np.array([200, 150, 100])

    # 验证约束条件
    if constraints.validate_constraints(allocation_matrix, demand_matrix):
        print("所有约束条件均满足！")
    else:
        print("约束条件未满足！")
