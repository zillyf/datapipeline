FROM jupyter/scipy-notebook

RUN pip install pymongo

EXPOSE 8080

COPY ./notebooks /home/jovyan/notebooks

CMD ["jupyter", "notebook", "--port=8890", "--NotebookApp.token=''"]

