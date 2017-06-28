

b: benchmark
benchmark:
	python benchmark.py


t: tests
tests:
	python -m pytest test_methods.py -v


d: draw
draw:
	python draw_in_2d.py
