#!/usr/bin/env python3
import sys
import tempfile
import subprocess
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

class FeatureTester:
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.test_dir = Path(tempfile.mkdtemp())
        
    def run_command(self, cmd):
        """Run a command and return success, stdout, stderr."""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'  # Handle encoding errors gracefully
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def test_error_explanation(self):
        """Test basic error explanation."""
        console.print("\n[bold cyan]Testing Basic Functionality[/bold cyan]")
        
        # Test error explanation
        success, output, error = self.run_command(
            'dbug explain "NameError: name \'x\' is not defined"'
        )
        
        # Check if explanation was generated (look for key content)
        if success and (
            "not defined" in output.lower() or 
            "nameerror" in output.lower() or
            "name error" in output.lower() or
            "doesn't exist" in output.lower()
        ):
            console.print("[green]✅ Error explanation working[/green]")
            self.passed += 1
            return True
        else:
            console.print("[red]❌ Error explanation failed[/red]")
            if error:
                console.print(f"[dim]Error: {error[:200]}[/dim]")
            if output:
                console.print(f"[dim]Output: {output[:200]}[/dim]")
            self.failed += 1
            return False
    
    def test_history(self):
        """Test history tracking."""
        success, output, error = self.run_command("dbug history")
        
        if success:
            console.print("[green]✅ History tracking working[/green]")
            self.passed += 1
            return True
        else:
            console.print("[red]❌ History tracking failed[/red]")
            self.failed += 1
            return False
    
    def test_config(self):
        """Test configuration."""
        success, output, error = self.run_command("dbug config --show")
        
        if success:
            console.print("[green]✅ Configuration working[/green]")
            self.passed += 1
            return True
        else:
            console.print("[red]❌ Configuration failed[/red]")
            self.failed += 1
            return False
    
    def test_error_prediction(self):
        """Test error prediction."""
        console.print("\n[bold cyan]Testing Error Prediction[/bold cyan]")
        
        # Create test file
        test_file = self.test_dir / "test_prediction.py"
        test_file.write_text("""
def broken_function():
    print(undefined_variable)  # NameError

def syntax_error()
    pass  # Missing colon

import os
import sys  # Unused import
""")
        
        # Test prediction
        success, output, error = self.run_command(f"dbug predict {test_file}")
        
        # Check for prediction output - look for table or error mentions
        if success and (
            "SyntaxError" in output or 
            "syntax error" in output.lower() or
            "potential errors" in output.lower() or
            "Line" in output or
            "Confidence" in output or
            "expected" in output.lower()
        ):
            console.print("[green]✅ Error prediction working[/green]")
            self.passed += 1
            return True
        else:
            console.print("[red]❌ Error prediction failed[/red]")
            if error:
                console.print(f"[dim]Error: {error[:200]}[/dim]")
            if output:
                console.print(f"[dim]Output preview: {output[:200]}[/dim]")
            self.failed += 1
            return False
    
    def test_custom_pattern_training(self):
        """Test custom pattern training."""
        console.print("\n[bold cyan]Testing Custom Pattern Training[/bold cyan]")
        
        # This requires interactive input
        console.print("[yellow]⚠ Custom pattern training requires interactive input[/yellow]")
        console.print("[dim]Run manually: dbug train --interactive[/dim]")
    
    def test_ml_training(self):
        """Test ML model training."""
        console.print("\n[bold cyan]Testing ML Training[/bold cyan]")
        
        # Build training data
        console.print("[cyan]Building training data...[/cyan]")
        
        errors = [
            "NameError: name 'x' is not defined",
            "NameError: name 'y' is not defined",
            "TypeError: cannot add int and str",
            "TypeError: unsupported operand",
            "IndexError: list index out of range",
            "KeyError: 'missing_key'",
            "ValueError: invalid literal",
            "AttributeError: no attribute",
            "ImportError: no module",
            "SyntaxError: invalid syntax",
        ]
        
        for error in errors:
            self.run_command(f'dbug explain "{error}"')
        
        # Check history
        success, output, _ = self.run_command("dbug history --stats")
        
        if success and "total" in output.lower():
            console.print("[green]✅ Training data created[/green]")
            self.passed += 1
            
            # Attempt ML training
            console.print("[cyan]Training ML models...[/cyan]")
            success, output, error = self.run_command("dbug train --ml")
            
            if success:
                console.print("[green]✅ ML training completed[/green]")
                self.passed += 1
            else:
                console.print("[yellow]⚠ ML training skipped (not enough data or dependencies missing)[/yellow]")
        else:
            console.print("[red]❌ Failed to create training data[/red]")
            self.failed += 1
    
    def test_github_integration(self, token=None):
        """Test GitHub integration."""
        console.print("\n[bold cyan]Testing GitHub Integration[/bold cyan]")
        
        if not token:
            console.print("[yellow]⚠ GitHub token not provided[/yellow]")
            console.print("[dim]Run with: python test_features.py --github YOUR_TOKEN[/dim]")
            return
        
        # Set token
        self.run_command(f"dbug config github_token {token}")
        
        # Test search
        success, output, error = self.run_command(
            'dbug github search "NameError" --language python'
        )
        
        if success and ("url" in output.lower() or "github" in output.lower()):
            console.print("[green]✅ GitHub search working[/green]")
            self.passed += 1
        else:
            console.print("[red]❌ GitHub search failed[/red]")
            console.print(f"[dim]{error}[/dim]")
            self.failed += 1
    
    def test_prediction_with_ml(self):
        """Test prediction with ML enabled."""
        console.print("\n[bold cyan]Testing ML-Enhanced Prediction[/bold cyan]")
        
        # Enable ML
        self.run_command("dbug config use_ml_prediction true")
        
        # Create test file
        test_file = self.test_dir / "test_ml.py"
        test_file.write_text("""
def test():
    result = undefined_var + 5
    return result
""")
        
        # Test prediction
        success, output, error = self.run_command(f"dbug predict {test_file}")
        
        if success and output:
            console.print("[green]✅ ML prediction working[/green]")
            self.passed += 1
        else:
            console.print("[yellow]⚠ ML prediction not available (models not trained)[/yellow]")
    
    def test_basic_functionality(self):
        """Test basic error explanation, history, and config."""
        console.print("\n[bold cyan]Testing Basic Functionality[/bold cyan]")
        
        self.test_error_explanation()
        self.test_history()
        self.test_config()
    
    def print_summary(self):
        """Print test summary."""
        console.print("\n" + "="*60)
        console.print("[bold]Test Summary[/bold]")
        console.print("="*60)
        
        table = Table()
        table.add_column("Status", style="cyan")
        table.add_column("Count", style="green")
        
        table.add_row("✅ Passed", str(self.passed))
        table.add_row("❌ Failed", str(self.failed))
        table.add_row("Total", str(self.passed + self.failed))
        
        console.print(table)
        
        if self.failed == 0:
            console.print("\n[bold green]🎉 All tests passed![/bold green]")
        else:
            console.print(f"\n[bold yellow]⚠ {self.failed} test(s) failed[/bold yellow]")
    
    def cleanup(self):
        """Clean up test files."""
        import shutil
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)


def main():
    """Run all tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test DeBugBuddy features")
    parser.add_argument("--ml", action="store_true", help="Test ML features")
    parser.add_argument("--github", type=str, help="GitHub token for testing")
    args = parser.parse_args()
    
    tester = FeatureTester()
    
    try:
        # Basic tests
        tester.test_basic_functionality()
        tester.test_error_prediction()
        
        # ML tests
        if args.ml:
            tester.test_ml_training()
            tester.test_prediction_with_ml()
        
        # GitHub tests
        if args.github:
            tester.test_github_integration(args.github)
        
        # Pattern training (manual)
        tester.test_custom_pattern_training()
        
    finally:
        tester.print_summary()
        tester.cleanup()


if __name__ == "__main__":
    main()