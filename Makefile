build:
	pip install -e .

clean:
	rm -rf *.egg-info
	rm -rf build/

cleanup:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

venv:
	virtualenv -p python3 venv
