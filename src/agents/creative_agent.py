class CreativeAgent:
    def __init__(self,cfg):
        self.cfg = cfg
    def generate(self,data,evaluated):
        tokens=set()
        for r in data.get('raw_head',[]):
            for t in str(r.get('creative_message','')).split():
                tokens.add(t.strip('.,!?').capitalize())
        if not tokens:
            tokens={'Comfort','Breathable','Soft'}
        tok_list=list(tokens)
        out={}
        for e in evaluated:
            camp=e['campaign']
            out[camp]=[
                {'headline':f"{camp}: Premium Comfort", 'message': ' '.join(tok_list[:6]), 'cta':'Shop Now'},
                {'headline':f"{camp}: Customer Favorite", 'message':'Social proof: loved by customers', 'cta':'Buy Today'},
                {'headline':f"{camp}: Bundle & Save", 'message':'Offer-led messaging: 3 for 2 bundle', 'cta':'View Offer'}
            ]
        return out