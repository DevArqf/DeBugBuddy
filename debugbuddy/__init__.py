def __getattr__(name):
    if name == "ErrorParser":
        from debugbuddy.core.parsers import ErrorParser
        return ErrorParser
    elif name == "ErrorExplainer":
        from debugbuddy.core.explainer import ErrorExplainer
        return ErrorExplainer
    elif name == "ErrorPredictor":
        from debugbuddy.core.predictor import ErrorPredictor
        return ErrorPredictor
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")