.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: run
run:
	python3 a_maze_ing.py config.txt

.PHONY: clean
clean:
	find . -type d - name "__pycache__" -exec rm -rf {} +
	rm -rf . .mypy_cache

.PHONY: debug
debug:
	python3 pdb a_maze_ing.py config.txt

.PHONY: lint
lint:
	flake8.
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-def --check-untyped-defs