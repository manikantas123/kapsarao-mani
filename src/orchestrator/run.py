import argparse
import json
import time
from pathlib import Path

from src.utils.io import load_config, save_json
from src.agents.planner_agent import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent


def main():
    # Parse input query
    p = argparse.ArgumentParser()
    p.add_argument("query", type=str)
    p.add_argument("--config", default="config/config.yaml")
    args = p.parse_args()

    # Load config
    cfg = load_config(args.config)

    # ----- AGENT PIPELINE -----

    # 1. Planner Agent
    planner = PlannerAgent(cfg)
    plan = planner.decompose(args.query)

    # 2. Data Agent
    data_agent = DataAgent(cfg)
    data_summary = data_agent.summarize({})

    # 3. Insight Agent
    insight_agent = InsightAgent(cfg)
    raw_insights = insight_agent.propose(data_summary, plan)

    # Improve confidence on retry items
    for i in raw_insights:
        if i.get("retry"):
            i["confidence"] = min(0.99, i["confidence"] + 0.08)

    # 4. Evaluator Agent
    evaluator = EvaluatorAgent(cfg)
    evaluated = evaluator.validate(raw_insights, data_summary)

    # 5. Creative Agent
    creative_agent = CreativeAgent(cfg)
    creatives = creative_agent.generate(data_summary, evaluated)

    # ----- SAVE OUTPUTS -----
    save_json(evaluated, cfg["outputs"]["insights"])
    save_json(creatives, cfg["outputs"]["creatives"])

    # DO NOT overwrite report.md
    # The report is written manually by the user

    # ----- MEMORY LOGGING -----
    if cfg.get("memory", {}).get("enabled", False):
        mp = Path(cfg["memory"]["path"])
        mp.parent.mkdir(parents=True, exist_ok=True)
        prev = []

        if mp.exists():
            prev = json.loads(mp.read_text())

        prev.append({"query": args.query, "ts": time.time()})
        mp.write_text(json.dumps(prev, indent=2))

    print("Done. Outputs written to reports/")


if __name__ == "__main__":
    main()
