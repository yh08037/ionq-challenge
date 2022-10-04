FROM ubuntu:22.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
libglib2.0-0 libxext6 libsm6 libxrender1 git mercurial subversion vim python3 python3-pip && \
	pip install --no-cache-dir --upgrade pip

RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-5.3.0-Linux-x86_64.sh -O ~/anaconda.sh && /bin/bash ~/anaconda.sh -b -p /opt/conda && \
rm ~/anaconda.sh && ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

#RUN apt-get install -y curl grep sed dpkg && \
#	TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
#	curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
#	dpkg -i tini.deb && \
#	rm tini.deb && \
#	apt-get clean

RUN pip install ipykernel qiskit qiskit-ionq qiskit[machine-learning] qiskit-machine-learning[sparse] qiskit[optimization] qiskit[finance] qiskit[nature] matplotlib pylatexenc tensorflow torch torchvision torchaudio pennylane pennylane-lightning pennylane-lightning[gpu] pennylane-qiskit seaborn
	
ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]

