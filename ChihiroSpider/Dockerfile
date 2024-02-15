FROM python:3.8


COPY . ./workspace
WORKDIR ./workspace


# COPY pyproject.toml ./

# RUN apt-get update
# RUN apt-get install -y build-essential libssl-dev libffi-dev python3-dev 

RUN python -m ensurepip --upgrade

RUN pip install --upgrade setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
# RUN python3 -m ensurepip --upgrade

RUN pip install poetry  -i https://pypi.tuna.tsinghua.edu.cn/simple
# RUN pip install cffi -i https://pypi.tuna.tsinghua.edu.cn/simple
# RUN pip wheel --no-cache-dir --use-pep517 "cffi (==1.14.0)"  -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi


# run the app server in production with gunicorn
CMD ["poetry", "run", "scrapy", "crawl", "QuotesSpider"]


