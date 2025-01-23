"""
目标函数模块
定义医疗资源优化配置的多个目标函数
包括效率目标、可及性目标和成本目标
"""

import numpy as np
from typing import List, Tuple, Dict
from .config import WEIGHT_CONFIG, BUDGET_CONFIG

class ObjectiveFunction:
    """目标函数类"""
    
    def __init__(self):
        """初始化目标函数"""
        self.weights = WEIGHT_CONFIG["OBJECTIVE_WEIGHTS"]
        self.budget_limits = BUDGET_CONFIG["BUDGET_LIMITS"]
        
    def efficiency_objective(self, x: np.ndarray, resource_matrix: np.ndarray) -> float:
        """
        效率目标函数
        最大化资源利用效率
        
        Args:
            x: 决策变量(资源分配方案)
            resource_matrix: 资源效率矩阵
            
        Returns:
            float: 效率目标值
        """
        # 计算资源利用效率
        efficiency = np.sum(x * resource_matrix) / np.sum(x)
        return -efficiency  # 转换为最小化问题
        
    def accessibility_objective(self, x: np.ndarray, distance_matrix: np.ndarray) -> float:
        """
        可及性目标函数
        最小化服务可及性差异
        
        Args:
            x: 决策变量
            distance_matrix: 距离矩阵
            
        Returns:
            float: 可及性目标值
        """
        # 计算加权平均距离
        weighted_distance = np.sum(x * distance_matrix) / np.sum(x)
        # 计算可及性差异
        accessibility_variance = np.var(weighted_distance)
        return accessibility_variance
        
    def cost_objective(self, x: np.ndarray, cost_matrix: np.ndarray) -> float:
        """
        成本目标函数
        最小化总成本
        
        Args:
            x: 决策变量
            cost_matrix: 成本矩阵
            
        Returns:
            float: 成本目标值
        """
        total_cost = np.sum(x * cost_matrix)
        return total_cost
        
    def evaluate(self, x: np.ndarray, 
                resource_matrix: np.ndarray,
                distance_matrix: np.ndarray, 
                cost_matrix: np.ndarray) -> Tuple[float, float, float]:
        """
        评估目标函数值
        
        Args:
            x: 决策变量
            resource_matrix: 资源效率矩阵
            distance_matrix: 距离矩阵
            cost_matrix: 成本矩阵
            
        Returns:
            Tuple[float, float, float]: 三个目标函数值
        """
        efficiency = self.efficiency_objective(x, resource_matrix)
        accessibility = self.accessibility_objective(x, distance_matrix)
        cost = self.cost_objective(x, cost_matrix)
        
        return efficiency, accessibility, cost
        
    def weighted_sum(self, objectives: Tuple[float, float, float]) -> float:
        """
        计算加权目标和
        
        Args:
            objectives: 目标函数值元组
            
        Returns:
            float: 加权和
        """
        weights = [
            np.mean(self.weights["efficiency"]),
            np.mean(self.weights["accessibility"]), 
            np.mean(self.weights["cost"])
        ]
        return np.sum(np.array(objectives) * weights)
        
    def normalize_objectives(self, objectives: List[Tuple[float, float, float]]) -> np.ndarray:
        """
        目标函数值归一化
        
        Args:
            objectives: 目标函数值列表
            
        Returns:
            np.ndarray: 归一化后的目标函数值
        """
        objectives_array = np.array(objectives)
        min_vals = np.min(objectives_array, axis=0)
        max_vals = np.max(objectives_array, axis=0)
        
        # 避免除零
        ranges = np.maximum(max_vals - min_vals, 1e-10)
        
        return (objectives_array - min_vals) / ranges

def main():
    """主函数:演示目标函数的使用"""
    # 创建示例数据
    x = np.random.rand(3, 3)  # 3x3的决策矩阵
    resource_matrix = np.random.rand(3, 3)  # 资源效率矩阵
    distance_matrix = np.random.rand(3, 3)  # 距离矩阵
    cost_matrix = np.random.rand(3, 3)  # 成本矩阵
    
    # 创建目标函数实例
    obj_func = ObjectiveFunction()
    
    # 计算目标函数值
    objectives = obj_func.evaluate(x, resource_matrix, distance_matrix, cost_matrix)
    
    # 输出结果
    print("决策变量:")
    print(x)
    print("\n目标函数值:")
    print(f"效率目标: {objectives[0]:.4f}")
    print(f"可及性目标: {objectives[1]:.4f}")
    print(f"成本目标: {objectives[2]:.4f}")
    print(f"\n加权目标和: {obj_func.weighted_sum(objectives):.4f}")

if __name__ == "__main__":
    main()
