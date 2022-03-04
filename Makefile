# ----------------------------------
#          INSTALL & TEST
# ----------------------------------

check_code:
	@flake8 scripts/* smackbang/*.py

black:
	@black scripts/* smackbang/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr smackbang-*.dist-info
	@rm -fr smackbang.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)



# ----------------------------------
#         LOCAL SET UP
# ----------------------------------

install_requirements:
	@pip install -r requirements.txt

# ----------------------------------
#         HEROKU COMMANDS
# ----------------------------------

APP_NAME=smackbang

env:
	API_KEY: ${{secrets.FLIGHT_DATA_TOKEN}}

streamlit:
	-@streamlit run app.py

heroku_login:
	-@heroku login

heroku_keys:
	-@heroku keys:add ~/.ssh/id_ed25519.pub

heroku_create_app:
	-@heroku create --ssh-git ${APP_NAME} --region eu

deploy_heroku:
	-@git push heroku master
	-@heroku ps:scale web=1

# ----------------------------------
#         FAST API COMMANDS
# ----------------------------------

run_api:
	uvicorn api.fast:app --reload  # load web server with code autoreload


# ----------------------------------
#         FAST API COMMANDS
# ----------------------------------

docker_build:
	-@docker build --tag=smackbang_api .

docker_run_it:
	-@docker run -it -e PORT=8000 -p 8000:8000 smackbang_api sh

docker_run_production:
	-@docker run -e PORT=8000 -p 8000:8000 smackbang_api
