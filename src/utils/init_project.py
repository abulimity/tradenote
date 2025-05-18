import json
from pathlib import Path

def init_project():
    # 获取项目根目录
    project_root = Path(__file__).parent.parent.parent

    # 配置文件路径
    config_path = project_root / "config.json"

    try:
        # 读取配置文件
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 检查 root_path 是否为空
        if not config.get('root_path'):
            config['root_path'] = str(project_root)

            # 将更新后的配置写回文件
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)

            print(f"已将 root_path 设置为 {project_root}")
        else:
            print(f"root_path 已存在，值为 {config['root_path']}")

    except FileNotFoundError:
        print("未找到配置文件 config.json")
    except Exception as e:
        print(f"初始化过程中出现错误: {e}")

if __name__ == "__main__":
    init_project()