ARG cuda_version=10.0
ARG cudnn_version=7
FROM nvidia/cuda:${cuda_version}-cudnn${cudnn_version}-devel

# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
      bzip2 \
      g++ \
      git \
      openssh-server \
      sudo \
      nano \
      curl \
      libsm6 \
      libxext6 \
      libxrender1 \
      libgl1-mesa-glx \
      python3-dev \
      python3-pip \
      p7zip-full \
      wget && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install pip --upgrade && \
    python3 -m pip install cython && \
    python3 -m pip install numpy && \
    python3 -m pip install opencv-python && \
    python3 -m pip install matplotlib && \
    python3 -m pip install requests && \
    python3 -m pip install --upgrade nbconvert && \
    python3 -m pip install notebook && \
    python3 -m pip install tqdm && \
    python3 -m pip install scikit-image

# Install pycocotools
RUN git clone https://github.com/waleedka/coco.git
WORKDIR coco/PythonAPI/
RUN python3 setup.py build_ext install
