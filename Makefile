format:
	PYTHONPATH=. python3 -m black .

test:
	PYTHONPATH=converter pytest
