# CostOptimizer

## Usage
For selecting default config path `config`, from src directory
```py
from cost_optimizer import CostOptimizer
co = CostOptimizer()
print(co.optimize(<capacity>,<hours>)
```
For selecting cutom config path
```py
from src.cost_optimizer import CostOptimizer
co = CostOptimizer('<path_to_config_directory>')
print(co.optimize(<capacity>,<hours>)
```

## Test
Get into tests directory and run
```
pytest cost_optimizer_test.py
```
