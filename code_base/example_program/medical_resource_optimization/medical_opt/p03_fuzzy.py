"""
模糊AHP模块：基于模糊数的层次分析法
用于处理判断中的不确定性和模糊性
"""

import numpy as np
from typing import List, Tuple, Dict
import logging


class FuzzyAHP:
    """模糊层次分析法 (Fuzzy AHP) 实现"""

    def __init__(self):
        """初始化模糊AHP"""
        self.logger = logging.getLogger(__name__)
        self.scale_reference = self._get_fuzzy_scale_reference()

    @staticmethod
    def _get_fuzzy_scale_reference() -> Dict[int, Tuple[Tuple[float, float, float]]]:
        """
        获取模糊标度参考 (三角模糊数)

        Returns:
            Dict[int, Tuple[Tuple[float, float, float]]]: 模糊标度参考
        """
        return {
            1: (1, 1, 1),  # 同等重要
            3: (2, 3, 4),  # 稍微重要
            5: (4, 5, 6),  # 明显重要
            7: (6, 7, 8),  # 强烈重要
            9: (8, 9, 10),  # 极端重要
            2: (1, 2, 3),  # 介于1和3之间
            4: (3, 4, 5),  # 介于3和5之间
            6: (5, 6, 7),  # 介于5和7之间
            8: (7, 8, 9)   # 介于7和9之间
        }

    def generate_fuzzy_comparison_matrix(self, crisp_matrix: np.ndarray) -> np.ndarray:
        """
        将普通判断矩阵转换为模糊判断矩阵 (三角模糊数)

        Args:
            crisp_matrix: 普通判断矩阵 (二维数组)

        Returns:
            np.ndarray: 模糊判断矩阵 (三维数组)
        """
        n = crisp_matrix.shape[0]
        fuzzy_matrix = np.zeros((n, n, 3))  # 三维矩阵存储三角模糊数

        for i in range(n):
            for j in range(n):
                if i == j:
                    fuzzy_matrix[i, j] = (1, 1, 1)  # 对角线元素
                elif i < j:
                    fuzzy_matrix[i, j] = self.scale_reference[int(crisp_matrix[i, j])]
                    fuzzy_matrix[j, i] = tuple(1 / x for x in reversed(fuzzy_matrix[i, j]))  # 互反性

        return fuzzy_matrix

    def calculate_fuzzy_weights(self, fuzzy_matrix: np.ndarray) -> np.ndarray:
        """
        计算模糊权重向量

        Args:
            fuzzy_matrix: 模糊判断矩阵 (三维数组)

        Returns:
            np.ndarray: 模糊权重向量 (三角模糊数)
        """
        try:
            n = fuzzy_matrix.shape[0]

            # 1. 计算模糊综合矩阵的行和
            row_sums = np.sum(fuzzy_matrix, axis=1)  # 每一行的模糊数相加

            # 2. 模糊数归一化
            total_sum = np.sum(row_sums, axis=0)  # 所有模糊数的总和 (L, M, U)
            fuzzy_weights = row_sums / total_sum

            return fuzzy_weights

        except Exception as e:
            self.logger.error(f"Error in fuzzy weight calculation: {str(e)}")
            raise

    def defuzzify_weights(self, fuzzy_weights: np.ndarray) -> np.ndarray:
        """
        模糊权重去模糊化 (Defuzzification)

        Args:
            fuzzy_weights: 模糊权重向量 (三角模糊数)

        Returns:
            np.ndarray: 去模糊化后的权重向量
        """
        try:
            # 使用重心法去模糊化： (L + M + U) / 3
            crisp_weights = np.mean(fuzzy_weights, axis=1)
            return crisp_weights / np.sum(crisp_weights)  # 归一化

        except Exception as e:
            self.logger.error(f"Error in defuzzification: {str(e)}")
            raise

    def fuzzy_ahp(self, crisp_matrix: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        完整的模糊AHP流程：从普通判断矩阵到权重向量

        Args:
            crisp_matrix: 普通判断矩阵

        Returns:
            Tuple[np.ndarray, np.ndarray]: 模糊权重向量、去模糊化后的权重向量
        """
        try:
            # 1. 转换为模糊判断矩阵
            fuzzy_matrix = self.generate_fuzzy_comparison_matrix(crisp_matrix)

            # 2. 计算模糊权重向量
            fuzzy_weights = self.calculate_fuzzy_weights(fuzzy_matrix)

            # 3. 去模糊化 (Defuzzification)
            crisp_weights = self.defuzzify_weights(fuzzy_weights)

            return fuzzy_weights, crisp_weights

        except Exception as e:
            self.logger.error(f"Error in fuzzy AHP process: {str(e)}")
            raise


def main():
    """主函数：演示模糊AHP的使用"""
    # 示例：普通判断矩阵
    crisp_matrix = np.array([
        [1, 3, 5],
        [1/3, 1, 2],
        [1/5, 1/2, 1]
    ])

    # 创建模糊AHP实例
    fuzzy_ahp = FuzzyAHP()

    # 执行模糊AHP
    fuzzy_weights, crisp_weights = fuzzy_ahp.fuzzy_ahp(crisp_matrix)

    # 输出结果
    print("普通判断矩阵:")
    print(crisp_matrix)
    print("\n模糊权重向量 (三角模糊数):")
    print(fuzzy_weights)
    print("\n去模糊化后的权重向量:")
    print(crisp_weights)


if __name__ == "__main__":
    main()
