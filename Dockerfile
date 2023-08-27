FROM python

WORKDIR .

COPY . .

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY . .

CMD ["streamlit", "run", "front.py"]