"""
优化器模块 (p06_optimizer.py)
实现医疗资源优化配置问题的求解，使用NSGA-II多目标优化算法。
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
import logging
from deap import base, creator, tools, algorithms
import random
from .config import OPTIMIZER_CONFIG, WEIGHT_CONFIG
from .p05_constraints import Constraints

class ResourceOptimizer:
    """医疗资源优化器类"""

    def __init__(self, 
                 resource_types: Dict,
                 hospital_levels: Dict,
                 budget_config: Dict,
                 constraints: Constraints):
        """
        初始化优化器

        Args:
            resource_types: 资源类型配置
            hospital_levels: 医院等级配置
            budget_config: 预算配置
            constraints: 约束条件对象
        """
        self.logger = logging.getLogger(__name__)
        self.resource_types = resource_types
        self.hospital_levels = hospital_levels
        self.budget_config = budget_config
        self.constraints = constraints
        
        # 优化器配置
        self.population_size = OPTIMIZER_CONFIG["population_size"]
        self.n_generations = OPTIMIZER_CONFIG["generations"]
        self.cx_prob = OPTIMIZER_CONFIG["crossover_prob"]
        self.mut_prob = OPTIMIZER_CONFIG["mutation_prob"]
        self.convergence_threshold = OPTIMIZER_CONFIG["convergence_threshold"]
        
        # 设置随机种子
        random.seed(OPTIMIZER_CONFIG["random_seed"])
        np.random.seed(OPTIMIZER_CONFIG["random_seed"])

        # 初始化DEAP工具箱
        self._setup_toolbox()

    def _setup_toolbox(self) -> None:
        """配置DEAP工具箱"""
        # 1. 创建最小化问题的Fitness类
        creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0, -1.0))
        
        # 2. 创建Individual类
        creator.create("Individual", np.ndarray, fitness=creator.FitnessMin)
        
        # 3. 初始化工具箱
        self.toolbox = base.Toolbox()
        
        # 4. 注册个体生成函数
        self.toolbox.register("attr_float", self._generate_random_allocation)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, 
                            self.toolbox.attr_float)
        self.toolbox.register("population", tools.initRepeat, list, 
                            self.toolbox.individual)
        
        # 5. 注册遗传算法操作
        self.toolbox.register("evaluate", self._evaluate)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
        self.toolbox.register("select", tools.selNSGA2)

    def _generate_random_allocation(self) -> np.ndarray:
        """
        生成随机的初始资源分配方案

        Returns:
            np.ndarray: 资源分配矩阵
        """
        n_resources = len(self.resource_types)
        n_hospitals = len(self.hospital_levels)
        
        # 生成满足约束的随机分配方案
        while True:
            allocation = np.random.uniform(
                low=0,
                high=[self.budget_config["BUDGET_LIMITS"][i+1] for i in range(n_resources)],
                size=(n_resources, n_hospitals)
            )
            
            if self.constraints.validate_constraints(
                allocation, 
                np.array([self.budget_config["DEMAND_THRESHOLDS"][i+1] 
                         for i in range(n_hospitals)])
            ):
                return allocation

    def _evaluate(self, individual: np.ndarray) -> Tuple[float, float, float]:
        """
        评估解的适应度

        Args:
            individual: 资源分配方案

        Returns:
            Tuple[float, float, float]: (效率损失, 可及性损失, 成本损失)
        """
        # 1. 计算效率目标
        efficiency_loss = self._calculate_efficiency_loss(individual)
        
        # 2. 计算可及性目标
        accessibility_loss = self._calculate_accessibility_loss(individual)
        
        # 3. 计算成本目标
        cost_loss = self._calculate_cost_loss(individual)
        
        return efficiency_loss, accessibility_loss, cost_loss

    def _calculate_efficiency_loss(self, allocation: np.ndarray) -> float:
        """计算效率损失"""
        # 资源利用率偏差
        utilization_rates = np.sum(allocation, axis=1) / np.array(
            [self.budget_config["BUDGET_LIMITS"][i+1] for i in range(len(self.resource_types))]
        )
        efficiency_loss = np.mean((1 - utilization_rates) ** 2)
        
        return float(efficiency_loss)

    def _calculate_accessibility_loss(self, allocation: np.ndarray) -> float:
        """计算可及性损失"""
        # 需求满足度偏差
        demand_satisfaction = np.sum(allocation, axis=0) / np.array(
            [self.budget_config["DEMAND_THRESHOLDS"][i+1] 
             for i in range(len(self.hospital_levels))]
        )
        accessibility_loss = np.mean((1 - demand_satisfaction) ** 2)
        
        return float(accessibility_loss)

    def _calculate_cost_loss(self, allocation: np.ndarray) -> float:
        """计算成本损失"""
        total_costs = np.zeros(len(self.resource_types))
        
        for resource_type, costs in self.budget_config["UNIT_COSTS"].items():
            resource_idx = resource_type - 1
            unit_cost = sum(costs.values())
            total_costs[resource_idx] = np.sum(allocation[resource_idx]) * unit_cost
            
        cost_loss = np.mean(
            (total_costs / np.array([self.budget_config["BUDGET_LIMITS"][i+1] 
                                   for i in range(len(self.resource_types))])) ** 2
        )
        
        return float(cost_loss)

    def optimize(self) -> Tuple[np.ndarray, List[float]]:
        """
        执行优化过程

        Returns:
            Tuple[np.ndarray, List[float]]: (最优解, 目标函数值)
        """
        try:
            # 1. 生成初始种群
            pop = self.toolbox.population(n=self.population_size)
            
            # 2. 评估初始种群
            fitnesses = list(map(self.toolbox.evaluate, pop))
            for ind, fit in zip(pop, fitnesses):
                ind.fitness.values = fit
            
            # 3. 开始进化
            for gen in range(self.n_generations):
                # 选择下一代个体
                offspring = algorithms.varOr(
                    pop, self.toolbox, 
                    lambda_=self.population_size, 
                    cxpb=self.cx_prob, 
                    mutpb=self.mut_prob
                )
                
                # 评估子代适应度
                fits = self.toolbox.map(self.toolbox.evaluate, offspring)
                for fit, ind in zip(fits, offspring):
                    ind.fitness.values = fit
                
                # 环境选择
                pop = self.toolbox.select(pop + offspring, self.population_size)
                
                # 检查收敛性
                if self._check_convergence(pop):
                    self.logger.info(f"Converged after {gen+1} generations")
                    break
            
            # 4. 获取最优解
            best_solution = tools.selBest(pop, 1)[0]
            return np.array(best_solution), best_solution.fitness.values
            
        except Exception as e:
            self.logger.error(f"Optimization error: {str(e)}")
            raise

    def _check_convergence(self, population: List) -> bool:
        """检查是否收敛"""
        fitness_values = [ind.fitness.values for ind in population]
        std_dev = np.std(fitness_values, axis=0)
        return np.all(std_dev < self.convergence_threshold)

# 测试代码
if __name__ == "__main__":
    from .config import RESOURCE_TYPES, HOSPITAL_LEVELS, BUDGET_CONFIG
    
    # 创建约束条件对象
    constraints = Constraints(BUDGET_CONFIG, HOSPITAL_LEVELS)
    
    # 创建优化器
    optimizer = ResourceOptimizer(
        RESOURCE_TYPES,
        HOSPITAL_LEVELS,
        BUDGET_CONFIG,
        constraints
    )
    
    # 执行优化
    best_solution, objective_values = optimizer.optimize()
    
    print("最优解:")
    print(best_solution)
    print("\n目标函数值 (效率损失, 可及性损失, 成本损失):")
    print(objective_values)
