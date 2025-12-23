import click
from rich.console import Console
from rich.prompt import Prompt
from debugbuddy.core.trainer import PatternTrainer
from debugbuddy.storage.config import ConfigManager
from debugbuddy.models.training import TrainingData

console = Console()

@click.command()
@click.option('--interactive', '-i', is_flag=True, help='Interactive training mode')
@click.option('--language', '-l', type=str, help='Programming language')
def train(interactive, language):
    
    config = ConfigManager()
    trainer = PatternTrainer(config)
    
    if interactive:
        console.print("\n[bold cyan]📚 Interactive Pattern Training[/bold cyan]\n")
        console.print("[dim]Enter error examples to create a custom pattern[/dim]\n")
        
        examples = []
        
        while True:
            error_text = Prompt.ask("Error text (or 'done' to finish)")
            
            if error_text.lower() == 'done':
                if len(examples) < 2:
                    console.print("[yellow]⚠ Need at least 2 examples[/yellow]")
                    continue
                break
            
            explanation = Prompt.ask("Simple explanation")
            fix = Prompt.ask("How to fix")
            lang = language or Prompt.ask("Language")
            
            examples.append(TrainingData(
                error_text=error_text,
                explanation=explanation,
                fix=fix,
                language=lang
            ))
            
            console.print(f"[green]✓ Added example {len(examples)}[/green]\n")
        
        pattern = trainer.train_pattern(examples)
        
        console.print(f"\n[green]✨ Custom pattern created![/green]")
        console.print(f"[dim]Type: {pattern.type}[/dim]")
        console.print(f"[dim]Keywords: {', '.join(pattern.keywords)}[/dim]")
    
    else:
        patterns = trainer.list_custom_patterns()
        
        if not patterns:
            console.print("[yellow]No custom patterns yet[/yellow]")
            console.print("[dim]Use --interactive to create one[/dim]")
            return
        
        console.print("\n[bold cyan]📚 Custom Patterns[/bold cyan]\n")
        for i, pattern in enumerate(patterns, 1):
            console.print(f"{i}. [cyan]{pattern.type}[/cyan] [{pattern.language}]")