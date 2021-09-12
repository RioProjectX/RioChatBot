FROM archlinux:base-devel
RUN curl -fsSL "https://repo.archlinuxcn.org/x86_64/glibc-linux4-2.33-4-x86_64.pkg.tar.zst" | bsdtar -C / -xvf -
RUN pacman -Syy && \
    pacman --noconfirm --needed -Syu python3 \
    python-pip
RUN pip3 install -U pip
COPY . .
RUN pip3 install -U -r requirements.txt
CMD ["python3","Rio.py"]
