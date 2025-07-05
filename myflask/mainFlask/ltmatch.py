class LTMatch:
    def __init__(self, startPos: int, endPos: int, text: str, category: str, ruleId: str):
        self.startPos = startPos
        self.endPos = endPos
        self.text = text
        self.category = category
        self.ruleId = ruleId

    def __str__(self):
        toString = f"""text: {self.text}
        Category: {self.category}
        RuleId: {self.ruleId}
        text: {self.text}
        startPos: {self.startPos}
        endPos: {self.endPos}
        """

        return toString