from typing import List
import ast
from pathlib import Path
from ..models.prediction import Prediction
from ..storage.patterns import PatternManager
from ..monitoring.checker import SimpleChecker

class ErrorPredictor:
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.pattern_mgr = PatternManager()
        
    def predict_file(self, file_path: Path) -> List[Prediction]:
        predictions = []
        
        # Static analysis
        predictions.extend(self._analyze_static(file_path))
        
        # Pattern matching
        predictions.extend(self._analyze_patterns(file_path))
        
        # ML-based prediction
        predictions.extend(self._analyze_ml(file_path))
        
        return sorted(predictions, key=lambda x: x.confidence, reverse=True)
    
    def _analyze_static(self, file_path: Path) -> List[Prediction]:
        predictions = []
        if file_path.suffix == '.py':
            try:
                with open(file_path, 'r') as f:
                    tree = ast.parse(f.read())
                checker = SimpleChecker(str(file_path))
                checker.visit(tree)
                for name, lines in checker.undefined_locations.items():
                    for line in lines:
                        predictions.append(Prediction(
                            file=str(file_path),
                            line=line,
                            column=None,
                            error_type='NameError',
                            message=f"name '{name}' is not defined",
                            confidence=0.8,
                            suggestion="Define the variable or import it",
                            severity='high'
                        ))
            except SyntaxError as e:
                predictions.append(Prediction(
                    file=str(file_path),
                    line=e.lineno,
                    column=e.offset,
                    error_type='SyntaxError',
                    message=e.msg,
                    confidence=1.0,
                    suggestion="Fix the syntax",
                    severity='critical'
                ))
        # For other languages, could add linters if dependencies allow, but since no install, skip
        return predictions
    
    def _analyze_patterns(self, file_path: Path) -> List[Prediction]:
        lang = file_path.suffix[1:]
        patterns = self.pattern_mgr.load_patterns(lang)
        predictions = []
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                for pattern in patterns:
                    if any(kw in line.lower() for kw in pattern.keywords):
                        predictions.append(Prediction(
                            file=str(file_path),
                            line=i,
                            column=None,
                            error_type=pattern.type,
                            message=pattern.simple,
                            confidence=0.5,
                            suggestion=pattern.fix,
                            severity='medium'
                        ))
        return predictions
    
    def _analyze_ml(self, file_path: Path) -> List[Prediction]:
        """Use trained ML models for prediction."""
        # Placeholder for future ML integration. Might use torch :)
        return []