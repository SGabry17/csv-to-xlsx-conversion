FROM public.ecr.aws/lambda/python:3.12

RUN pip3 install pandas xlsxwriter boto3

COPY convert.py ${LAMBDA_TASK_ROOT}/

CMD [ "convert.lambda_handler" ]
