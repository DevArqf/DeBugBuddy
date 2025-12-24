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
        
        static_preds = self._analyze_static(file_path)
        predictions.extend(static_preds)
        
        pattern_preds = self._analyze_patterns(file_path)
        predictions.extend(pattern_preds)
        
        ml_preds = self._analyze_ml(file_path)
        predictions.extend(ml_preds)
        
        predictions.sort(key=lambda p: p.confidence, reverse=True)
        
        return predictions

    def _analyze_static(self, file_path: Path) -> List[Prediction]:
        predictions = []
        
        if file_path.suffix != '.py':
            return predictions
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                return predictions
            
            try:
                tree = ast.parse(content, filename=str(file_path))
                
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
                        
            except (SyntaxError, IndentationError) as e:
                predictions.append(Prediction(
                    file=str(file_path),
                    line=e.lineno or 1,
                    column=e.offset,
                    error_type='SyntaxError',
                    message=e.msg or 'invalid syntax',
                    confidence=1.0,
                    suggestion="Fix the syntax error",
                    severity='critical'
                ))
                
        except Exception as e:
            # file read error or other issues - don't crash, just return empty
            pass
            
        return predictions

    def _analyze_patterns(self, file_path: Path) -> List[Prediction]:
        lang = file_path.suffix[1:]
        patterns = self.pattern_mgr.load_patterns(lang)
        predictions = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines, 1):
                    for pattern in patterns:
                        if any(kw in line.lower() for kw in pattern.get('keywords', [])):
                            predictions.append(Prediction(
                                file=str(file_path),
                                line=i,
                                column=None,
                                error_type=pattern.get('type', 'Unknown'),
                                message=pattern.get('simple', 'Potential issue'),
                                confidence=0.5,
                                suggestion=pattern.get('fix', 'Review this line'),
                                severity='medium'
                            ))
        except Exception:
            pass
            
        return predictions

    def _analyze_ml(self, file_path: Path) -> List[Prediction]:
        """Analyze using machine learning (placeholder)."""
        return []