import random
class InsightAgent:
    def __init__(self,cfg):
        self.cfg = cfg
        random.seed(self.cfg.get('seed',42))
    def propose(self,data,plan):
        insights=[]
        min_ctr=self.cfg.get('min_ctr_alert',0.012)
        for c in data['by_campaign']:
            reasons=[]
            conf=0.5
            if c.get('roas',0) < 3:
                reasons.append('roas_decline')
                conf += 0.2
            if c.get('ctr',0) < min_ctr:
                reasons.append('creative_fatigue_or_low_hook_strength')
                conf += 0.15
            if random.random() < 0.3:
                reasons.append('repetitive_creative_angles')
                conf += 0.05
            if not reasons:
                reasons.append('stable_but_opportunity_for_scale')
            insights.append({
                'campaign': c['campaign_name'],
                'hypothesis': ' & '.join(reasons),
                'reasoning': f"CTR={c.get('ctr',0):.4f} ROAS={c.get('roas',0):.2f}",
                'confidence': round(min(conf,0.99),2),
                'retry': conf < self.cfg.get('confidence_threshold',0.6)
            })
        return insights