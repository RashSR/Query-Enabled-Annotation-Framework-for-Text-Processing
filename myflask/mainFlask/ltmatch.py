class LTMatch:
    def __init__(self, startPos, endPos, text, category, ruleId):
        self.startPos = startPos
        self.endPos = endPos
        self.text = text
        self.category = category
        self.ruleId = ruleId

    def __str__(self):
        toString = f"""Category: {self.category}
        RuleId: {self.ruleId}
        text: {self.text}
        startPos: {self.startPos}
        endPos: {self.endPos}
        """

        return toString