test:
	# linting warnings should not prevent us from moving forward.
	# also, line length of 80 is too restrictive.
	flake8 \
	--exclude docs \
	--max-line-length 160 \
	--statistics \
	./
	
	# cov requires pytest-cov library
	py.test \
	--cov=sudoku_objects \
	--cov-report term-missing \
	--cov-config=.coveragerc \
	--verbose
