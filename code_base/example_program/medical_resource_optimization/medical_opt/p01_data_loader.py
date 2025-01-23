"""
数据加载与预处理模块
负责原始数据的读取、验证、清洗和标准化处理
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import logging
from .config import (
    RESOURCE_TYPES, 
    HOSPITAL_LEVELS,
    BUDGET_CONFIG
)

class DataLoader:
    """医疗资源数据加载与预处理类"""
    
    def __init__(self, data_path: str = None):
        """
        初始化数据加载器
        
        Args:
            data_path: 数据文件路径
        """
        self.data_path = Path(data_path) if data_path else None
        self.logger = logging.getLogger(__name__)
        
        # 存储处理后的数据
        self.resource_data = None  # 资源数据
        self.demand_data = None    # 需求数据
        self.cost_data = None      # 成本数据
        
    def load_resource_data(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """
        加载资源数据
        
        Args:
            file_path: 资源数据文件路径
            
        Returns:
            pd.DataFrame: 资源数据框
        """
        try:
            path = Path(file_path) if file_path else self.data_path
            if path.suffix == '.csv':
                data = pd.read_csv(path)
            elif path.suffix in ['.xlsx', '.xls']:
                data = pd.read_excel(path)
            else:
                raise ValueError(f"Unsupported file format: {path.suffix}")
                
            # 验证数据结构
            required_columns = ['resource_type', 'hospital_level', 'quantity', 'unit_cost']
            if not all(col in data.columns for col in required_columns):
                raise ValueError(f"Missing required columns: {required_columns}")
                
            self.resource_data = data
            return data
            
        except Exception as e:
            self.logger.error(f"Error loading resource data: {str(e)}")
            raise
            
    def load_demand_data(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """
        加载需求数据
        
        Args:
            file_path: 需求数据文件路径
            
        Returns:
            pd.DataFrame: 需求数据框
        """
        try:
            path = Path(file_path) if file_path else self.data_path
            data = pd.read_csv(path) if path.suffix == '.csv' else pd.read_excel(path)
            
            # 验证数据结构
            required_columns = ['hospital_level', 'demand_value', 'population']
            if not all(col in data.columns for col in required_columns):
                raise ValueError(f"Missing required columns: {required_columns}")
                
            self.demand_data = data
            return data
            
        except Exception as e:
            self.logger.error(f"Error loading demand data: {str(e)}")
            raise
            
    def preprocess_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        数据预处理：清洗、标准化
        
        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray]: 
                处理后的资源矩阵、需求矩阵和成本矩阵
        """
        if self.resource_data is None or self.demand_data is None:
            raise ValueError("Please load data first")
            
        try:
            # 1. 数据清洗
            self._clean_data()
            
            # 2. 构建资源矩阵 (resource_type × hospital_level)
            resource_matrix = self._build_resource_matrix()
            
            # 3. 构建需求矩阵 (hospital_level × 1)
            demand_matrix = self._build_demand_matrix()
            
            # 4. 构建成本矩阵 (resource_type × hospital_level)
            cost_matrix = self._build_cost_matrix()
            
            return resource_matrix, demand_matrix, cost_matrix
            
        except Exception as e:
            self.logger.error(f"Error in data preprocessing: {str(e)}")
            raise
            
    def _clean_data(self) -> None:
        """数据清洗"""
        # 1. 删除空值
        self.resource_data = self.resource_data.dropna()
        self.demand_data = self.demand_data.dropna()
        
        # 2. 删除重复值
        self.resource_data = self.resource_data.drop_duplicates()
        self.demand_data = self.demand_data.drop_duplicates()
        
        # 3. 类型转换
        self.resource_data['quantity'] = pd.to_numeric(self.resource_data['quantity'])
        self.resource_data['unit_cost'] = pd.to_numeric(self.resource_data['unit_cost'])
        self.demand_data['demand_value'] = pd.to_numeric(self.demand_data['demand_value'])
        
        # 4. 范围检查
        self._validate_data_ranges()
        
    def _validate_data_ranges(self) -> None:
        """验证数据范围"""
        # 验证资源类型
        valid_resource_types = set(RESOURCE_TYPES.keys())
        if not set(self.resource_data['resource_type']).issubset(valid_resource_types):
            raise ValueError(f"Invalid resource types found. Valid types: {valid_resource_types}")
            
        # 验证医院等级
        valid_hospital_levels = set(HOSPITAL_LEVELS.keys())
        if not set(self.resource_data['hospital_level']).issubset(valid_hospital_levels):
            raise ValueError(f"Invalid hospital levels found. Valid levels: {valid_hospital_levels}")
            
        # 验证数值范围
        if (self.resource_data['quantity'] < 0).any():
            raise ValueError("Negative quantity values found")
        if (self.resource_data['unit_cost'] < 0).any():
            raise ValueError("Negative unit cost values found")
        if (self.demand_data['demand_value'] < 0).any():
            raise ValueError("Negative demand values found")
            
    def _build_resource_matrix(self) -> np.ndarray:
        """构建资源矩阵"""
        matrix = np.zeros((len(RESOURCE_TYPES), len(HOSPITAL_LEVELS)))
        
        for _, row in self.resource_data.iterrows():
            i = row['resource_type'] - 1
            j = row['hospital_level'] - 1
            matrix[i, j] = row['quantity']
            
        return matrix
        
    def _build_demand_matrix(self) -> np.ndarray:
        """构建需求矩阵"""
        matrix = np.zeros(len(HOSPITAL_LEVELS))
        
        for _, row in self.demand_data.iterrows():
            j = row['hospital_level'] - 1
            matrix[j] = row['demand_value']
            
        return matrix
        
    def _build_cost_matrix(self) -> np.ndarray:
        """构建成本矩阵"""
        matrix = np.zeros((len(RESOURCE_TYPES), len(HOSPITAL_LEVELS)))
        
        for _, row in self.resource_data.iterrows():
            i = row['resource_type'] - 1
            j = row['hospital_level'] - 1
            matrix[i, j] = row['unit_cost']
            
        return matrix
        
    def generate_test_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        生成测试数据
        
        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray]: 
                测试用的资源矩阵、需求矩阵和成本矩阵
        """
        # 1. 生成资源矩阵
        resource_matrix = np.random.randint(10, 100, size=(3, 3))
        
        # 2. 生成需求矩阵
        demand_matrix = np.array([
            BUDGET_CONFIG["DEMAND_THRESHOLDS"][1],
            BUDGET_CONFIG["DEMAND_THRESHOLDS"][2],
            BUDGET_CONFIG["DEMAND_THRESHOLDS"][3]
        ])
        
        # 3. 生成成本矩阵
        cost_matrix = np.random.uniform(1, 10, size=(3, 3))
        
        return resource_matrix, demand_matrix, cost_matrix
        
    def export_processed_data(self, output_path: str) -> None:
        """
        导出处理后的数据
        
        Args:
            output_path: 输出路径
        """
        if any(data is None for data in [self.resource_data, self.demand_data]):
            raise ValueError("No processed data available")
            
        try:
            output_path = Path(output_path)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # 导出资源数据
            self.resource_data.to_csv(output_path / 'processed_resource_data.csv', index=False)
            
            # 导出需求数据
            self.demand_data.to_csv(output_path / 'processed_demand_data.csv', index=False)
            
            self.logger.info(f"Data exported successfully to {output_path}")
            
        except Exception as e:
            self.logger.error(f"Error exporting data: {str(e)}")
            raise
