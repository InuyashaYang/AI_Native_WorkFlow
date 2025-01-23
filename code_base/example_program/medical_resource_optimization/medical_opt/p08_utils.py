# p08_utils.py

import logging
import os
from typing import Any, Dict
import numpy as np

def setup_logging(log_config: Dict[str, Any] = None) -> None:
    """
    配置日志系统

    Args:
        log_config (Dict[str, Any], optional): 日志配置字典。
            包含 'level', 'format', 'filename' 等键。
            如果为 None，则使用默认配置。
    """
    default_config = {
        'level': logging.INFO,
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'filename': None,  # 如果为 None，则输出到控制台
        'filemode': 'a'
    }

    if log_config is not None:
        default_config.update(log_config)

    logging.basicConfig(
        level=default_config['level'],
        format=default_config['format'],
        filename=default_config['filename'],
        filemode=default_config['filemode']
    )

def ensure_directory(path: str) -> None:
    """
    确保指定路径的目录存在，如果不存在则创建。

    Args:
        path (str): 目录路径。
    """
    os.makedirs(path, exist_ok=True)

def normalize_matrix(matrix: np.ndarray) -> np.ndarray:
    """
    对矩阵进行归一化处理。

    Args:
        matrix (np.ndarray): 输入矩阵。

    Returns:
        np.ndarray: 归一化后的矩阵。
    """
    min_vals = np.min(matrix, axis=0)
    max_vals = np.max(matrix, axis=0)
    ranges = np.maximum(max_vals - min_vals, 1e-10)  # 避免除零
    normalized = (matrix - min_vals) / ranges
    return normalized

def set_random_seeds(seed: int = 42) -> None:
    """
    设置随机种子以确保结果可复现。

    Args:
        seed (int, optional): 随机种子。默认为42。
    """
    import random
    random.seed(seed)
    np.random.seed(seed)

# 示例使用
if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger("UtilsTest")
    logger.info("日志系统配置成功。")

    # 确保目录存在
    test_dir = "./test_output"
    ensure_directory(test_dir)
    logger.info(f"确保目录存在：{test_dir}")

    # 归一化示例
    sample_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    normalized_matrix = normalize_matrix(sample_matrix)
    logger.info(f"归一化前:\n{sample_matrix}")
    logger.info(f"归一化后:\n{normalized_matrix}")

    # 设置随机种子
    set_random_seeds(123)
    logger.info("随机种子已设置为123。")
