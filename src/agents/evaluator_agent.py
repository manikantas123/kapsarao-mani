class EvaluatorAgent:
    def __init__(self,cfg):
        self.cfg = cfg
    def validate(self,insights,data):
        camp_map = {c['campaign_name']:c for c in data['by_campaign']}
        out=[]
        for ins in insights:
            c = camp_map.get(ins['campaign'])
            evidence = {'ctr': round(c.get('ctr',0),4), 'roas': round(c.get('roas',0),2), 'impressions': int(c.get('impressions',0))}
            conf = ins.get('confidence',0)
            if evidence['impressions'] > 200000:
                conf = min(0.99, conf + 0.05)
            out.append({**ins, 'evidence': evidence, 'confidence_final': round(conf,2)})
        return out