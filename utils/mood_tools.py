# utils/mood_tools.py

def detect_macro_mood_label(mood_text: str) -> str:
    """
    Classifies the market mood string into a label: Risk-On, Risk-Off, or Unknown.
    """
    if "Risk-On" in mood_text:
        return "Risk-On"
    elif "Risk-Off" in mood_text:
        return "Risk-Off"
    else:
        return "Unknown"