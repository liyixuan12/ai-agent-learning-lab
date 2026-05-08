"""
Company Growth and Risk Analyzer — runnable entry for the Topic 1 mini project.
公司增长与风险分析器（主题 1 小项目可运行入口）
"""

import importlib.util
from pathlib import Path


def _load_topic1_project():
    path = Path(__file__).resolve().parent.parent / "topic1_final_project.py"
    spec = importlib.util.spec_from_file_location("topic1_final_project", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    m = _load_topic1_project()
    for company in m.companies:
        print(m.generate_company_summary(company))


if __name__ == "__main__":
    main()
