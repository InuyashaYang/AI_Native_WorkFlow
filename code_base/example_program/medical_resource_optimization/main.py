# main.py

"""
医疗资源优化配置系统主程序
整合数据加载、预处理、权重计算、约束设置、优化求解和结果可视化的完整流程
"""

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# 从项目模块中导入所需的类和函数
from medical_opt.p01_data_loader import DataLoader
from medical_opt.p02_ahp import AHPCalculator
from medical_opt.p03_fuzzy import FuzzyAHP
from medical_opt.p04_objective import ObjectiveFunction
from medical_opt.p05_constraints import Constraints
from medical_opt.p06_optimizer import ResourceOptimizer
from medical_opt.p07_visualizer import Visualizer
from medical_opt.p08_utils import setup_logging, ensure_directory, set_random_seeds

def main():
    """主函数：执行医疗资源优化配置的完整流程"""
    # 1. 设置日志系统
    setup_logging({
        'level': logging.INFO,
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'filename': './logs/main.log',
        'filemode': 'a'
    })
    logger = logging.getLogger("Main")
    logger.info("医疗资源优化配置系统启动。")

    try:
        # 2. 数据加载与预处理
        data_loader = DataLoader(data_path="./data/input/")
        logger.info("开始加载资源数据。")
        resource_data = data_loader.load_resource_data("resource_data.csv")
        logger.info("资源数据加载完成。")
        
        logger.info("开始加载需求数据。")
        demand_data = data_loader.load_demand_data("demand_data.csv")
        logger.info("需求数据加载完成。")
        
        logger.info("开始预处理数据。")
        resource_matrix, demand_matrix, cost_matrix = data_loader.preprocess_data()
        logger.info("数据预处理完成。")
        
        # 可选：生成测试数据
        # resource_matrix, demand_matrix, cost_matrix = data_loader.generate_test_data()
        # logger.info("生成测试数据。")
        
        # 3. 权重计算（选择 AHP 或 模糊 AHP）
        # 3.1 使用 AHP 计算权重
        ahp_calculator = AHPCalculator()
        logger.info("开始进行 AHP 权重计算。")
        criteria = ["efficiency", "accessibility", "cost"]
        ahp_matrix = np.array([
            [1, 2, 4],
            [1/2, 1, 2],
            [1/4, 1/2, 1]
        ])  # 这里您可以根据实际情况修改判断矩阵
        weights, cr, is_consistent = ahp_calculator.calculate_weights(ahp_matrix)
        
        if not is_consistent:
            logger.warning("AHP 判断矩阵一致性检验未通过。请检查判断矩阵。")
        
        logger.info(f"AHP 权重计算完成。权重向量: {weights}，一致性比率: {cr:.4f}")
        
        # 3.2 或者，使用模糊 AHP 计算权重
        # fuzzy_ahp = FuzzyAHP()
        # logger.info("开始进行模糊 AHP 权重计算。")
        # fuzzy_weights, crisp_weights = fuzzy_ahp.fuzzy_ahp(ahp_matrix)
        # logger.info(f"模糊 AHP 权重计算完成。去模糊化后的权重向量: {crisp_weights}")
        # weights = crisp_weights  # 使用去模糊化后的权重
        
        # 4. 设置约束条件
        logger.info("开始设置约束条件。")
        from medical_opt.config import BUDGET_CONFIG, HOSPITAL_LEVELS, RESOURCE_TYPES
        constraints = Constraints(BUDGET_CONFIG, HOSPITAL_LEVELS)
        logger.info("约束条件设置完成。")
        
        # 5. 初始化优化器
        logger.info("开始初始化优化器。")
        optimizer = ResourceOptimizer(
            resource_types=RESOURCE_TYPES,
            hospital_levels=HOSPITAL_LEVELS,
            budget_config=BUDGET_CONFIG,
            constraints=constraints
        )
        logger.info("优化器初始化完成。")
        
        # 6. 执行优化
        logger.info("开始执行优化过程。")
        best_solution, objective_values = optimizer.optimize()
        logger.info("优化过程完成。")
        logger.info(f"最优解: {best_solution}")
        logger.info(f"目标函数值 (效率损失, 可及性损失, 成本损失): {objective_values}")
        
        # 7. 结果可视化
        logger.info("开始进行结果可视化。")
        visualizer = Visualizer()
        ensure_directory("./results/figures/")
        
        # 绘制帕累托前沿
        # 假设我们保存了优化过程中的所有目标函数值，需在优化器中进行记录
        # 这里为了示例，使用随机数据
        # 请根据实际优化器实现调整
        # pareto_objectives = np.random.rand(50, 2)  # 示例数据
        # visualizer.plot_pareto_front(pareto_objectives, save_path="./results/figures/pareto_front.png")
        
        # 绘制资源分配热图
        visualizer.plot_resource_allocation(
            allocation_matrix=best_solution,
            hospital_levels=HOSPITAL_LEVELS,
            resource_types=RESOURCE_TYPES,
            save_path="./results/figures/resource_allocation.png"
        )
        
        # 保存优化结果
        np.savetxt("./results/optimzation_result.csv", best_solution, delimiter=",")
        logger.info("优化结果已保存至 ./results/optimzation_result.csv")
        
        # 可视化其他内容，如目标函数趋势（需要在优化器中记录）
        # history = optimizer.get_objective_history()  # 假设有此方法
        # visualizer.plot_objective_trends(history, save_path="./results/figures/objective_trends.png")
        
        logger.info("结果可视化完成。")
        
        logger.info("医疗资源优化配置系统运行结束。")
        
    except Exception as e:
        logger.error(f"程序运行中发生错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
