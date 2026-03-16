"""
主可视化脚本 - 一键生成所有可视化图表
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import subprocess

def main():
    print("=" * 70)
    print("  HiSCaM Visualization Suite")
    print("  Generating all visualizations for paper and presentation")
    print("=" * 70)
    
    scripts = [
        ('visualize_data.py', 'Data Visualization'),
        ('visualize_pipeline.py', 'Pipeline Visualization'),
        ('visualize_training.py', 'Training Visualization'),
    ]
    
    for script, name in scripts:
        print(f"\n{'='*70}")
        print(f"  Running: {name}")
        print(f"{'='*70}")
        
        script_path = os.path.join(os.path.dirname(__file__), script)
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=False, 
                              cwd=os.path.dirname(os.path.dirname(__file__)))
    
    print("\n" + "=" * 70)
    print("  All visualizations completed!")
    print("=" * 70)
    
    # 列出生成的所有文件
    print("\nGenerated files:")
    print("-" * 50)
    
    figures_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'figures')
    
    for subdir in ['data_visualization', 'pipeline', 'training']:
        subdir_path = os.path.join(figures_dir, subdir)
        if os.path.exists(subdir_path):
            print(f"\n[{subdir}]")
            for f in sorted(os.listdir(subdir_path)):
                if f.endswith(('.png', '.pdf')):
                    filepath = os.path.join(subdir_path, f)
                    size = os.path.getsize(filepath) / 1024
                    print(f"  - {f} ({size:.1f} KB)")
    
    print("\n" + "=" * 70)
    print("  Ready for paper inclusion!")
    print("=" * 70)

if __name__ == "__main__":
    main()
