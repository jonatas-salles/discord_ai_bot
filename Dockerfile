FROM public.ecr.aws/lambda/python:3.12

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

COPY discord.py ${LAMBDA_TASK_ROOT}

CMD [ "discord.lambda_handler" ]