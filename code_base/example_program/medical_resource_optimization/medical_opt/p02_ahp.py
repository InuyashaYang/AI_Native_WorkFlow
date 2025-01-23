"""
AHP模块：实现层次分析法进行权重计算
用于医疗资源优化配置中的多准则决策权重确定
"""

import numpy as np
from typing import List, Dict, Tuple
import logging
from .config import WEIGHT_CONFIG

class AHPCalculator:
    """AHP权重计算器"""
    
    def __init__(self):
        """初始化AHP计算器"""
        self.logger = logging.getLogger(__name__)
        self.RI = WEIGHT_CONFIG["AHP_PARAMS"]["random_index"]
        self.max_iterations = WEIGHT_CONFIG["AHP_PARAMS"]["max_iterations"]
        self.tolerance = WEIGHT_CONFIG["AHP_PARAMS"]["tolerance"]
        
    def calculate_weights(self, comparison_matrix: np.ndarray) -> Tuple[np.ndarray, float, bool]:
        """
        计算权重向量
        
        Args:
            comparison_matrix: 判断矩阵
            
        Returns:
            Tuple[np.ndarray, float, bool]: 
                权重向量、一致性比率CR、是否通过一致性检验
        """
        try:
            # 1. 归一化判断矩阵
            norm_matrix = self._normalize_matrix(comparison_matrix)
            
            # 2. 计算权重向量
            weights = np.mean(norm_matrix, axis=1)
            
            # 3. 一致性检验
            cr = self._consistency_check(comparison_matrix, weights)
            is_consistent = cr < 0.1
            
            if not is_consistent:
                self.logger.warning(f"Consistency check failed: CR = {cr:.4f}")
            
            return weights, cr, is_consistent
            
        except Exception as e:
            self.logger.error(f"Error in weight calculation: {str(e)}")
            raise
            
    def _normalize_matrix(self, matrix: np.ndarray) -> np.ndarray:
        """
        归一化判断矩阵
        
        Args:
            matrix: 原始判断矩阵
            
        Returns:
            np.ndarray: 归一化后的矩阵
        """
        # 按列归一化
        col_sums = matrix.sum(axis=0)
        return matrix / col_sums
        
    def _consistency_check(self, matrix: np.ndarray, weights: np.ndarray) -> float:
        """
        一致性检验
        
        Args:
            matrix: 判断矩阵
            weights: 权重向量
            
        Returns:
            float: 一致性比率CR
        """
        n = len(weights)
        
        # 计算最大特征值
        lambda_max = self._calculate_eigenvalue(matrix, weights)
        
        # 计算一致性指标CI
        ci = (lambda_max - n) / (n - 1)
        
        # 计算一致性比率CR
        ri = self.RI[n - 1]
        cr = ci / ri if ri != 0 else 0
        
        return cr
        
    def _calculate_eigenvalue(self, matrix: np.ndarray, weights: np.ndarray) -> float:
        """
        计算最大特征值
        
        Args:
            matrix: 判断矩阵
            weights: 权重向量
            
        Returns:
            float: 最大特征值
        """
        # Aw
        weighted_sum = np.dot(matrix, weights)
        
        # λmax = average(Aw/w)
        ratios = weighted_sum / weights
        lambda_max = np.mean(ratios)
        
        return lambda_max
        
    def generate_comparison_matrix(self, criteria_names: List[str]) -> np.ndarray:
        """
        生成判断矩阵模板
        
        Args:
            criteria_names: 准则名称列表
            
        Returns:
            np.ndarray: 判断矩阵模板
        """
        n = len(criteria_names)
        matrix = np.ones((n, n))
        
        # 生成上三角矩阵
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i, j] = 0  # 待填充位置
                matrix[j, i] = 0  # 对应的倒数位置
                
        return matrix
        
    def validate_comparison_matrix(self, matrix: np.ndarray) -> bool:
        """
        验证判断矩阵的有效性
        
        Args:
            matrix: 判断矩阵
            
        Returns:
            bool: 是否有效
        """
        try:
            # 检查矩阵是否方阵
            if matrix.shape[0] != matrix.shape[1]:
                return False
                
            # 检查对角线元素是否为1
            if not np.allclose(np.diag(matrix), 1):
                return False
                
            # 检查互反性
            n = len(matrix)
            for i in range(n):
                for j in range(i + 1, n):
                    if not np.isclose(matrix[i, j] * matrix[j, i], 1):
                        return False
                        
            return True
            
        except Exception as e:
            self.logger.error(f"Error in matrix validation: {str(e)}")
            return False
            
    def get_scale_reference(self) -> Dict[int, str]:
        """
        获取AHP标度参考
        
        Returns:
            Dict[int, str]: 标度说明字典
        """
        return {
            1: "同等重要",
            3: "稍微重要",
            5: "明显重要",
            7: "强烈重要",
            9: "极端重要",
            2: "介于1和3之间",
            4: "介于3和5之间",
            6: "介于5和7之间",
            8: "介于7和9之间"
        }
        
def fuzzy_ahp(fuzzy_matrix: np.ndarray) -> np.ndarray:
    """
    模糊AHP方法
    
    Args:
        fuzzy_matrix: 模糊判断矩阵
        
    Returns:
        np.ndarray: 模糊权重向量
    """
    n = len(fuzzy_matrix)
    
    # 计算模糊综合评判值
    row_sums = np.sum(fuzzy_matrix, axis=1)
    total_sum = np.sum(row_sums)
    fuzzy_weights = row_sums / total_sum
    
    return fuzzy_weights

def main():
    """主函数：演示AHP的使用"""
    # 创建AHP计算器
    ahp = AHPCalculator()
    
    # 示例：三个准则的判断矩阵
    criteria = ["效率", "可及性", "成本"]
    matrix = np.array([
        [1, 2, 4],
        [1/2, 1, 2],
        [1/4, 1/2, 1]
    ])
    
    # 计算权重
    weights, cr, is_consistent = ahp.calculate_weights(matrix)
    
    # 输出结果
    print("判断矩阵:")
    print(matrix)
    print("\n权重向量:", weights)
    print(f"一致性比率 CR: {cr:.4f}")
    print(f"一致性检验: {'通过' if is_consistent else '未通过'}")

if __name__ == "__main__":
    main()
