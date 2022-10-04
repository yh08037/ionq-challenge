FROM ubuntu:22.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
libglib2.0-0 libxext6 libsm6 libxrender1 git mercurial subversion vim python3 python3-pip && \
	pip install --no-cache-dir --upgrade pip

RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-5.3.0-Linux-x86_64.sh -O ~/anaconda.sh && /bin/bash ~/anaconda.sh -b -p /opt/conda && \
rm ~/anaconda.sh && ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate ionq" >> ~/.bashrc

RUN conda create -n ionq python=3

RUN /bin/bash -c "source activate ionq && pip install --upgrade pip && \
    pip install notebook ipykernel tqdm numpy pandas matplotlib seaborn pylatexenc \
    qiskit qiskit-ionq qiskit[machine-learning] qiskit-machine-learning[sparse] \
    qiskit[optimization] qiskit[finance] qiskit[nature] \
    torch torchvision \
    pennylane pennylane-lightning pennylane-lightning[gpu] pennylane-qiskit" 

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \
    apt install git-lfs

RUN git clone -b submit --single-branch https://github.com/yh08037/ionq-challenge.git /home/dohunkim && \
    cd /home/dohunkim/ && git lfs pull

RUN echo "cd /home/dohunkim" >> ~/.bashrc

CMD [ "/bin/bash" ]
