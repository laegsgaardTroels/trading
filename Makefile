SHELL := /bin/bash

da_weather_trading.html: da_weather_trading.ipynb
	jupyter nbconvert --to html da_weather_trading.ipynb

.PHONY: case
case: environment.yml
	conda env create --prefix envs/case --file environment.yml
