format:
	PYTHONPATH=. python3 -m black .

test:
	PYTHONPATH=. python3 -m pytest
