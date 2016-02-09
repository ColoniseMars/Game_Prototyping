class fps:
    """Records time of renders and saves fps"""
    def __init__(self):
        self.rendertimelist = [0]
        self.differencelist = []
        self.fps = 1

    def addvalue(self, value):
        self.rendertimelist.append(value)
        self.differencelist.append(self.rendertimelist[-1]-self.rendertimelist[-2])
        self.fps = int(1000/(sum(self.differencelist)/len(self.differencelist)))
        if len(self.rendertimelist) >20:
            self.rendertimelist.pop(0)
            self.differencelist.pop(0)
        if self.fps <1:
            self.fps = 1

    def give_fps(self):
        return self.fps