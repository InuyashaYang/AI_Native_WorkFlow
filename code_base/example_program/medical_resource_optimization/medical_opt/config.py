"""
医疗资源优化配置系统配置模块
包含系统所需的全局参数和配置项
"""

from typing import Dict, List, Tuple
import numpy as np

# 1. 基础配置
RESOURCE_TYPES = {
    1: "医疗设备",
    2: "医护人员",
    3: "床位资源"
}

HOSPITAL_LEVELS = {
    1: "三级医院",
    2: "二级医院",
    3: "一级医院"
}

# 2. 资源约束配置
BUDGET_CONFIG = {
    # 各类资源预算上限 B_i (单位：万元)
    "BUDGET_LIMITS": {
        1: 1000,  # 医疗设备预算
        2: 800,   # 医护人员预算
        3: 500    # 床位资源预算
    },
    
    # 各级医院最低服务需求 D_j
    "DEMAND_THRESHOLDS": {
        1: 200,  # 三级医院最低需求
        2: 150,  # 二级医院最低需求
        3: 100   # 一级医院最低需求
    },
    
    # 资源单位成本 (万元/单位)
    "UNIT_COSTS": {
        1: {"equipment": 10, "maintenance": 2},
        2: {"salary": 15, "training": 3},
        3: {"construction": 5, "operation": 1}
    }
}

# 3. 权重参数配置
WEIGHT_CONFIG = {
    # 目标函数权重范围 [w1, w2, w3]
    "OBJECTIVE_WEIGHTS": {
        "efficiency": (0.3, 0.4),    # 效率权重范围
        "accessibility": (0.3, 0.4),  # 可及性权重范围
        "cost": (0.2, 0.3)           # 成本权重范围
    },
    
    # AHP判断矩阵参数
    "AHP_PARAMS": {
        "max_iterations": 100,
        "tolerance": 1e-6,
        "random_index": [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
    }
}

# 4. 模糊评价参数配置
FUZZY_CONFIG = {
    # 评价等级
    "EVALUATION_LEVELS": ["优", "良", "中", "差"],
    
    # 隶属度函数参数
    "MEMBERSHIP_PARAMS": {
        "efficiency": {"a": 0.2, "b": 0.5, "c": 0.8},
        "accessibility": {"a": 0.3, "b": 0.6, "c": 0.9},
        "cost": {"a": 0.4, "b": 0.7, "c": 1.0}
    },
    
    # 模糊关系矩阵初始值
    "INITIAL_RELATION_MATRIX": np.array([
        [0.8, 0.6, 0.4],
        [0.6, 0.8, 0.5],
        [0.4, 0.5, 0.8]
    ])
}

# 5. 优化器配置
OPTIMIZER_CONFIG = {
    "algorithm": "NSGA-II",  # 使用NSGA-II多目标优化算法
    "population_size": 100,
    "generations": 200,
    "crossover_prob": 0.8,
    "mutation_prob": 0.1,
    "convergence_threshold": 1e-5,
    "random_seed": 42
}

# 6. 可视化配置
VISUALIZATION_CONFIG = {
    # 图表样式
    "style": {
        "figure_size": (10, 6),
        "dpi": 100,
        "font_size": 12,
        "color_palette": "Set3"
    },
    
    # 输出配置
    "output": {
        "save_format": "png",
        "save_path": "./results/figures/",
        "show_plot": True
    }
}

# 7. 系统配置
SYSTEM_CONFIG = {
    # 数据路径
    "data_paths": {
        "input": "./data/input/",
        "output": "./data/output/",
        "temp": "./data/temp/"
    },
    
    # 日志配置
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "./logs/optimization.log"
    },
    
    # 并行计算配置
    "parallel": {
        "enabled": True,
        "n_jobs": -1  # 使用所有可用CPU核心
    }
}

def validate_config() -> bool:
    """
    验证配置参数的有效性
    
    Returns:
        bool: 配置是否有效
    """
    try:
        # 验证资源类型和医院等级的完整性
        assert len(RESOURCE_TYPES) == 3
        assert len(HOSPITAL_LEVELS) == 3
        
        # 验证预算和需求阈值的非负性
        for budget in BUDGET_CONFIG["BUDGET_LIMITS"].values():
            assert budget > 0
        for demand in BUDGET_CONFIG["DEMAND_THRESHOLDS"].values():
            assert demand > 0
            
        # 验证权重和为1
        weights = WEIGHT_CONFIG["OBJECTIVE_WEIGHTS"]
        for w_range in weights.values():
            assert 0 <= w_range[0] <= w_range[1] <= 1
            
        # 验证模糊矩阵的维度
        assert FUZZY_CONFIG["INITIAL_RELATION_MATRIX"].shape == (3, 3)
        
        return True
        
    except AssertionError as e:
        print(f"配置验证失败: {str(e)}")
        return False

def get_resource_params(resource_type: int) -> Dict:
    """
    获取指定资源类型的相关参数
    
    Args:
        resource_type: 资源类型编号
        
    Returns:
        Dict: 资源参数字典
    """
    return {
        "budget": BUDGET_CONFIG["BUDGET_LIMITS"][resource_type],
        "unit_cost": BUDGET_CONFIG["UNIT_COSTS"][resource_type]
    }

def get_hospital_params(hospital_level: int) -> Dict:
    """
    获取指定医院等级的相关参数
    
    Args:
        hospital_level: 医院等级编号
        
    Returns:
        Dict: 医院参数字典
    """
    return {
        "demand": BUDGET_CONFIG["DEMAND_THRESHOLDS"][hospital_level]
    }
