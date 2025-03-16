FROM alpine

RUN apk add --no-cache python3 py3-pip && \
[ ! -e /usr/bin/python ] && ln -s /usr/bin/python3 /usr/bin/python || true
RUN which python3 && python3 --version
# RUN python3 -m ensurepip --default-pip


WORKDIR /app

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

RUN /app/venv/bin/pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 9000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]

# USER trainee

# CMD ["python", "-V"]
