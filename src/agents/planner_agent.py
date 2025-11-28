class PlannerAgent:
    def __init__(self, cfg):
        self.cfg = cfg
    def decompose(self, query):
        plan = {'task':query, 'steps':['summarize','hypothesize','validate','creative']}
        if '14' in query or '14 days' in query:
            plan['window_days'] = 14
        elif '7' in query:
            plan['window_days'] = 7
        else:
            plan['window_days'] = 7
        return plan