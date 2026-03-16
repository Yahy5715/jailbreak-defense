"""
操作流程可视化
生成系统架构和处理流程图
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np
import os

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def create_system_architecture():
    """创建系统架构图"""
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # 颜色定义
    colors = {
        'input': '#3498db',
        'llm': '#9b59b6',
        'safety_prober': '#e74c3c',
        'steering': '#f39c12',
        'risk_encoder': '#1abc9c',
        'output': '#2ecc71',
        'decision': '#34495e'
    }
    
    # 绘制组件框
    def draw_box(x, y, w, h, color, label, sublabel=None):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.2",
                             facecolor=color, edgecolor='white', linewidth=2, alpha=0.9)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2 + (0.15 if sublabel else 0), label, 
               ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        if sublabel:
            ax.text(x + w/2, y + h/2 - 0.2, sublabel, 
                   ha='center', va='center', fontsize=9, color='white', alpha=0.9)
    
    # 绘制箭头
    def draw_arrow(start, end, color='gray', style='->'):
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle=style, color=color, lw=2))
    
    # 输入
    draw_box(0.5, 4, 2, 2, colors['input'], 'Input', 'User Query')
    
    # LLM
    draw_box(4, 3.5, 3, 3, colors['llm'], 'LLM', 'Extract Hidden States')
    
    # 隐藏状态
    ax.text(8.5, 5.5, 'Hidden States', ha='center', fontsize=10, fontweight='bold')
    ax.text(8.5, 5.1, 'h ∈ ℝ^896', ha='center', fontsize=9, style='italic')
    
    # Safety Prober
    draw_box(10, 7, 3, 1.5, colors['safety_prober'], 'Safety Prober', 'Risk Detection')
    
    # Steering Matrix
    draw_box(10, 4.5, 3, 1.5, colors['steering'], 'Steering Matrix', 'Activation Intervention')
    
    # Risk Encoder
    draw_box(10, 2, 3, 1.5, colors['risk_encoder'], 'Risk Encoder', 'Multi-turn Memory')
    
    # Decision
    draw_box(14, 4, 1.5, 2, colors['decision'], 'Decision', '')
    
    # 输出分支
    ax.text(15.7, 7.5, 'BLOCK', ha='center', fontsize=10, fontweight='bold', color='#e74c3c')
    ax.text(15.7, 5, 'STEER', ha='center', fontsize=10, fontweight='bold', color='#f39c12')
    ax.text(15.7, 2.5, 'PASS', ha='center', fontsize=10, fontweight='bold', color='#2ecc71')
    
    # 绘制连接箭头
    draw_arrow((2.5, 5), (4, 5), colors['input'])
    draw_arrow((7, 5), (8, 5), colors['llm'])
    
    # 从隐藏状态到三个模块
    draw_arrow((9, 5.5), (10, 7.5), colors['safety_prober'])
    draw_arrow((9, 5), (10, 5.25), colors['steering'])
    draw_arrow((9, 4.5), (10, 2.75), colors['risk_encoder'])
    
    # 从三个模块到决策
    draw_arrow((13, 7.75), (14, 5.5), colors['safety_prober'])
    draw_arrow((13, 5.25), (14, 5), colors['steering'])
    draw_arrow((13, 2.75), (14, 4.5), colors['risk_encoder'])
    
    # 从决策到输出
    draw_arrow((15.5, 5.8), (15.5, 7), '#e74c3c')
    draw_arrow((15.5, 5), (15.7, 5), '#f39c12')
    draw_arrow((15.5, 4.2), (15.5, 3), '#2ecc71')
    
    # 标题
    ax.set_title('HiSCaM System Architecture', fontsize=16, fontweight='bold', pad=20)
    
    # 图例
    legend_elements = [
        mpatches.Patch(color=colors['safety_prober'], label='Safety Prober (Detection)'),
        mpatches.Patch(color=colors['steering'], label='Steering Matrix (Intervention)'),
        mpatches.Patch(color=colors['risk_encoder'], label='Risk Encoder (Memory)'),
    ]
    ax.legend(handles=legend_elements, loc='lower center', ncol=3, fontsize=10, framealpha=0.9)
    
    plt.tight_layout()
    os.makedirs('figures/pipeline', exist_ok=True)
    plt.savefig('figures/pipeline/system_architecture_detailed.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.savefig('figures/pipeline/system_architecture_detailed.pdf', bbox_inches='tight', facecolor='white')
    print("Saved: figures/pipeline/system_architecture_detailed.png")
    plt.close()

def create_training_pipeline():
    """创建训练流程图"""
    fig, ax = plt.subplots(figsize=(18, 8))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # 颜色
    colors = {
        'data': '#3498db',
        'process': '#9b59b6',
        'train': '#e74c3c',
        'eval': '#2ecc71',
        'output': '#f39c12'
    }
    
    def draw_step(x, y, w, h, color, label, step_num=None):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.15",
                             facecolor=color, edgecolor='white', linewidth=2, alpha=0.85)
        ax.add_patch(box)
        
        if step_num:
            circle = Circle((x + 0.3, y + h - 0.3), 0.25, facecolor='white', edgecolor=color, linewidth=2)
            ax.add_patch(circle)
            ax.text(x + 0.3, y + h - 0.3, str(step_num), ha='center', va='center', 
                   fontsize=10, fontweight='bold', color=color)
        
        ax.text(x + w/2, y + h/2, label, ha='center', va='center', 
               fontsize=10, fontweight='bold', color='white', wrap=True)
    
    def draw_arrow(start, end):
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', color='gray', lw=2))
    
    # 第一行：数据准备
    y1 = 6
    draw_step(0.5, y1, 2.5, 1.5, colors['data'], 'Download\nDatasets', 1)
    draw_step(3.5, y1, 2.5, 1.5, colors['process'], 'Preprocess\nData', 2)
    draw_step(6.5, y1, 2.5, 1.5, colors['process'], 'Generate\nHidden States', 3)
    draw_step(9.5, y1, 2.5, 1.5, colors['process'], 'Compute Refusal\nDirection', 4)
    
    # 箭头
    draw_arrow((3, 6.75), (3.5, 6.75))
    draw_arrow((6, 6.75), (6.5, 6.75))
    draw_arrow((9, 6.75), (9.5, 6.75))
    
    # 第二行：模型训练
    y2 = 3.5
    draw_step(0.5, y2, 2.5, 1.5, colors['train'], 'Train Safety\nProber', 5)
    draw_step(3.5, y2, 2.5, 1.5, colors['train'], 'Train Steering\nMatrix', 6)
    draw_step(6.5, y2, 2.5, 1.5, colors['train'], 'Train Risk\nEncoder', 7)
    draw_step(9.5, y2, 2.5, 1.5, colors['process'], 'System\nIntegration', 8)
    
    # 箭头
    draw_arrow((3, 4.25), (3.5, 4.25))
    draw_arrow((6, 4.25), (6.5, 4.25))
    draw_arrow((9, 4.25), (9.5, 4.25))
    
    # 垂直箭头（从数据准备到训练）
    draw_arrow((1.75, 6), (1.75, 5))
    draw_arrow((4.75, 6), (4.75, 5))
    draw_arrow((7.75, 6), (7.75, 5))
    draw_arrow((10.75, 6), (10.75, 5))
    
    # 第三行：评估输出
    y3 = 1
    draw_step(9.5, y3, 2.5, 1.5, colors['eval'], 'Evaluate\nBenchmark', 9)
    draw_step(12.5, y3, 2.5, 1.5, colors['output'], 'Generate\nFigures', 10)
    draw_step(15.5, y3, 2, 1.5, colors['output'], 'Release!', 11)
    
    # 箭头
    draw_arrow((10.75, 3.5), (10.75, 2.5))
    draw_arrow((12, 1.75), (12.5, 1.75))
    draw_arrow((15, 1.75), (15.5, 1.75))
    
    # 阶段标签
    ax.text(0.2, 7.8, 'Stage 1: Data Preparation', fontsize=12, fontweight='bold', color=colors['data'])
    ax.text(0.2, 5.3, 'Stage 2: Model Training', fontsize=12, fontweight='bold', color=colors['train'])
    ax.text(9.3, 2.8, 'Stage 3: Evaluation & Release', fontsize=12, fontweight='bold', color=colors['eval'])
    
    # 标题
    ax.set_title('Training Pipeline Overview', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('figures/pipeline/training_pipeline.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.savefig('figures/pipeline/training_pipeline.pdf', bbox_inches='tight', facecolor='white')
    print("Saved: figures/pipeline/training_pipeline.png")
    plt.close()

def create_inference_flowchart():
    """创建推理流程图"""
    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    colors = {
        'start': '#3498db',
        'process': '#9b59b6',
        'decision': '#f39c12',
        'action': '#e74c3c',
        'end': '#2ecc71'
    }
    
    def draw_rect(x, y, w, h, color, label):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.2",
                             facecolor=color, edgecolor='white', linewidth=2, alpha=0.9)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, label, ha='center', va='center', 
               fontsize=10, fontweight='bold', color='white')
    
    def draw_diamond(x, y, size, color, label):
        diamond = plt.Polygon([(x, y + size/2), (x + size/2, y + size), 
                               (x + size, y + size/2), (x + size/2, y)],
                             facecolor=color, edgecolor='white', linewidth=2, alpha=0.9)
        ax.add_patch(diamond)
        ax.text(x + size/2, y + size/2, label, ha='center', va='center', 
               fontsize=9, fontweight='bold', color='white')
    
    def draw_arrow(start, end, label=None, color='gray'):
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', color=color, lw=2))
        if label:
            mid = ((start[0] + end[0])/2, (start[1] + end[1])/2)
            ax.text(mid[0] + 0.3, mid[1], label, fontsize=9, color=color)
    
    # 节点
    draw_rect(4.5, 12.5, 3, 1, colors['start'], 'Input Query')
    draw_rect(4.5, 10.5, 3, 1, colors['process'], 'Extract Hidden States')
    draw_rect(4.5, 8.5, 3, 1, colors['process'], 'Safety Prober Analysis')
    draw_diamond(4.5, 6, 3, colors['decision'], 'Risk > 0.5?')
    draw_rect(0.5, 6.25, 3, 1, colors['end'], 'PASS (No Action)')
    draw_rect(4.5, 4, 3, 1, colors['process'], 'Risk Encoder Update')
    draw_diamond(4.5, 1.5, 3, colors['decision'], 'Risk > 0.85?')
    draw_rect(0.5, 1.75, 3, 1, colors['action'], 'BLOCK')
    draw_rect(8.5, 1.75, 3, 1, colors['process'], 'Apply Steering')
    draw_rect(8.5, 4.5, 3, 1, colors['end'], 'STEER + Output')
    
    # 箭头
    draw_arrow((6, 12.5), (6, 11.5))
    draw_arrow((6, 10.5), (6, 9.5))
    draw_arrow((6, 8.5), (6, 7.5))
    draw_arrow((4.5, 7), (3.5, 7), 'No', colors['end'])
    draw_arrow((6, 6), (6, 5))
    draw_arrow((6, 4), (6, 3))
    draw_arrow((4.5, 2.5), (3.5, 2.5), 'Yes', colors['action'])
    draw_arrow((7.5, 2.5), (8.5, 2.5), 'No')
    draw_arrow((10, 2.75), (10, 4.5))
    
    # 标题
    ax.set_title('Inference Flowchart', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('figures/pipeline/inference_flowchart.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.savefig('figures/pipeline/inference_flowchart.pdf', bbox_inches='tight', facecolor='white')
    print("Saved: figures/pipeline/inference_flowchart.png")
    plt.close()

def create_module_details():
    """创建模块详细架构图"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 8))
    
    for ax in axes:
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 8)
        ax.axis('off')
    
    colors = ['#e74c3c', '#f39c12', '#1abc9c']
    titles = ['Safety Prober', 'Steering Matrix', 'Risk Encoder']
    
    # Safety Prober
    ax = axes[0]
    layers = [
        ('Input: h ∈ ℝ^896', 7, '#3498db'),
        ('Linear(896, 224)', 6, '#e74c3c'),
        ('ReLU + Dropout', 5, '#e74c3c'),
        ('Linear(224, 2)', 4, '#e74c3c'),
        ('Softmax', 3, '#e74c3c'),
        ('Output: Risk Score', 2, '#2ecc71')
    ]
    
    for label, y, color in layers:
        box = FancyBboxPatch((0.5, y - 0.4), 5, 0.8, boxstyle="round,pad=0.02",
                             facecolor=color, edgecolor='white', linewidth=2, alpha=0.8)
        ax.add_patch(box)
        ax.text(3, y, label, ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    
    ax.set_title('Safety Prober Architecture', fontsize=14, fontweight='bold')
    
    # Steering Matrix
    ax = axes[1]
    layers = [
        ('Input: h ∈ ℝ^896', 7, '#3498db'),
        ('Refusal Direction r', 6, '#f39c12'),
        ('Null-space Projection', 5, '#f39c12'),
        ('S = (I - VᵀV) · r·rᵀ', 4, '#f39c12'),
        ('h\' = h + α·S·h', 3, '#f39c12'),
        ('Output: Steered h\'', 2, '#2ecc71')
    ]
    
    for label, y, color in layers:
        box = FancyBboxPatch((0.5, y - 0.4), 5, 0.8, boxstyle="round,pad=0.02",
                             facecolor=color, edgecolor='white', linewidth=2, alpha=0.8)
        ax.add_patch(box)
        ax.text(3, y, label, ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    
    ax.set_title('Steering Matrix Architecture', fontsize=14, fontweight='bold')
    
    # Risk Encoder
    ax = axes[2]
    layers = [
        ('Input: {h₁, h₂, ..., hₜ}', 7, '#3498db'),
        ('GRU Encoder', 6, '#1abc9c'),
        ('VAE: μ, log σ²', 5, '#1abc9c'),
        ('Risk Classifier', 4, '#1abc9c'),
        ('Rₜ = γ·Rₜ₋₁ + (1-γ)·risk', 3, '#1abc9c'),
        ('Output: Cumulative Risk', 2, '#2ecc71')
    ]
    
    for label, y, color in layers:
        box = FancyBboxPatch((0.5, y - 0.4), 5, 0.8, boxstyle="round,pad=0.02",
                             facecolor=color, edgecolor='white', linewidth=2, alpha=0.8)
        ax.add_patch(box)
        ax.text(3, y, label, ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    
    ax.set_title('Risk Encoder Architecture', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/pipeline/module_architectures.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.savefig('figures/pipeline/module_architectures.pdf', bbox_inches='tight', facecolor='white')
    print("Saved: figures/pipeline/module_architectures.png")
    plt.close()

def main():
    print("=" * 60)
    print("Pipeline Visualization")
    print("=" * 60)
    
    os.makedirs('figures/pipeline', exist_ok=True)
    
    print("\n[1/4] Creating system architecture...")
    create_system_architecture()
    
    print("\n[2/4] Creating training pipeline...")
    create_training_pipeline()
    
    print("\n[3/4] Creating inference flowchart...")
    create_inference_flowchart()
    
    print("\n[4/4] Creating module details...")
    create_module_details()
    
    print("\n" + "=" * 60)
    print("All pipeline visualizations saved to figures/pipeline/")
    print("=" * 60)

if __name__ == "__main__":
    main()
