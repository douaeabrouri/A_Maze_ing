install:
	@pip install -r requirements.txt

run:
	@python3 a_maze_ing.py config.txt

clean:
	@find . -type d - name "__pycache__" -exec rm -rf {} +
	@rm -rf . .mypy_cache

debug:
	@python3 pdb a_maze_ing.py config.txt

lint:
	@flake8.
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-def --check-untyped-defs