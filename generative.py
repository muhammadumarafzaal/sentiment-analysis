# function for simple rule-based generator to suggest improvements based on sentiment
def generate_suggestion(sentiment):
    if sentiment == 0:
        return "Consider improving product quality or customer service based on this feedback."
    elif sentiment == 1:
        return "Maintain current standards and gather more feedback for enhancement."
    elif sentiment == 2:
        return "Great feedback! Continue to leverage these strengths in marketing."
    return "No suggestion available."
