FROM python:3.5.6-slim-jessie

RUN apt-get update \
  && apt-get install -y curl \ 
  && curl -sL https://deb.nodesource.com/setup_10.x | bash - \
  && apt-get install -y nodejs \
  && pip install plotly==3.5.0 \
  && pip install "notebook>=5.3" "ipywidgets>=7.2" \
  && pip install jupyterlab==0.35 "ipywidgets>=7.2" \
  && export NODE_OPTIONS=--max-old-space-size=4096 \
  && jupyter labextension install @jupyter-widgets/jupyterlab-manager@0.38 --no-build \
  && jupyter labextension install plotlywidget@0.6.0 --no-build \
  && jupyter labextension install @jupyterlab/plotly-extension@0.18.1 --no-build \
  && jupyter labextension install jupyterlab-chart-editor@1.0 --no-build \
  && jupyter lab build \
  && unset NODE_OPTIONS

ENTRYPOINT ["jupyter", "lab", "--port=8889", "--allow-root", "--ip=0.0.0.0" , "--no-browser"]