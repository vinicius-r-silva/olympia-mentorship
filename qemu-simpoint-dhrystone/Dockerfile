FROM ubuntu:22.04

RUN apt update

# TODO remove unecessary packages
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt \
  install -y \
  git-email \
  libaio-dev \
  libbluetooth-dev \
  libcapstone-dev \
  libbrlapi-dev \
  libbz2-dev \
  libcap-ng-dev \
  libcurl4-gnutls-dev \
  libgtk-3-dev \
  libibverbs-dev \
  libjpeg8-dev \
  libncurses5-dev \
  libnuma-dev \
  librbd-dev \
  librdmacm-dev \
  libsasl2-dev \
  libsdl2-dev \
  libseccomp-dev \
  libsnappy-dev \
  libssh-dev \
  libvde-dev \
  libvdeplug-dev \
  libvte-2.91-dev \
  libxen-dev \
  liblzo2-dev \
  valgrind \
  xfslibs-dev \ 
  libnfs-dev \ 
  libiscsi-dev \
  gcc binutils \
  python3-pip \
  python3-sphinx \
  python3-sphinx-rtd-theme \
  ninja-build \
  flex \
  bison \
  git \ 
  python3-tomli \ 
  autoconf \
  automake \
  autotools-dev \
  curl \
  python3 \
  libmpc-dev \
  libmpfr-dev \
  libgmp-dev \
  gawk \
  build-essential \
  texinfo \
  gperf \
  libtool \
  patchutils \
  bc \
  zlib1g-dev \
  libexpat-dev \
  cmake \
  libglib2.0-dev \
  gcc-riscv64-linux-gnu \
  libslirp-dev 

RUN git clone https://gitlab.com/qemu-project/qemu.git
RUN git clone https://github.com/sifive/benchmark-dhrystone.git
RUN git clone https://github.com/hanhwi/SimPoint.git

WORKDIR /qemu/build
RUN ../configure --target-list=riscv32-linux-user,riscv64-linux-user,riscv32-softmmu,riscv64-softmmu
RUN make -j$(nproc)
RUN make install
ENV QEMU_PLUGINS=/qemu/build/contrib/plugins

WORKDIR /SimPoint/
RUN make -j$(nproc)
ENV PATH="$PATH:/SimPoint/bin"

# TODO make repository fork with file changes
WORKDIR /benchmark-dhrystone
RUN sed -i 's/^#define DHRY_ITERS 2000$/#define DHRY_ITERS 100000/' dhry_1.c
RUN sed -i 's/^\(DHRY-CFLAGS[[:space:]]*:=.*\)/\1 -static/' Makefile
RUN make CC=riscv64-linux-gnu-gcc
ENV DHRYSTONE="/benchmark-dhrystone/dhrystone"