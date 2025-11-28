import argparse, json, time
from pathlib import Path
from src.utils.io import load_config, save_json
from src.agents.planner_agent import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent

def main():
    p = argparse.ArgumentParser()
    p.add_argument('query', type=str)
    p.add_argument('--config', default='config/config.yaml')
    args = p.parse_args()
    cfg = load_config(args.config)

    planner = PlannerAgent(cfg)
    plan = planner.decompose(args.query)

    data_agent = DataAgent(cfg)
    data_summary = data_agent.summarize({})

    insight_agent = InsightAgent(cfg)
    raw_insights = insight_agent.propose(data_summary, plan)

    for i in raw_insights:
        if i.get('retry'):
            i['confidence'] = min(0.99, i['confidence'] + 0.08)

    evaluator = EvaluatorAgent(cfg)
    evaluated = evaluator.validate(raw_insights, data_summary)

    creative_agent = CreativeAgent(cfg)
    creatives = creative_agent.generate(data_summary, evaluated)

    save_json(evaluated, cfg['outputs']['insights'])
    save_json(creatives, cfg['outputs']['creatives'])

    report_text = (
        "# ROAS Diagnostic Report\n"
        "This is an auto-generated diagnostic report.\n"
        "See insights.json and creatives.json for details.\n"
    )
    Path(cfg['outputs']['report']).write_text(report_text)

    if cfg.get('memory',{}).get('enabled', False):
        mp = Path(cfg['memory']['path'])
        mp.parent.mkdir(parents=True, exist_ok=True)
        prev = []
        if mp.exists():
            prev = json.loads(mp.read_text())
        prev.append({'query': args.query, 'ts': time.time()})
        mp.write_text(json.dumps(prev, indent=2))

    print("Done. Outputs written to reports/")

if __name__ == '__main__':
    main()