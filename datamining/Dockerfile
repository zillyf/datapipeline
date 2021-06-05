FROM jupyter/scipy-notebook

RUN pip install pymongo kafka-python

EXPOSE 8080

#USER jovyan
COPY ./notebooks /home/jovyan/notebooks

CMD ["jupyter", "notebook", "--port=8890", "--NotebookApp.token=''"]

