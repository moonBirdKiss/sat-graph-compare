# 使用官方 Python alpine 镜像作为基础镜像
FROM python:3.6-alpine

# 安装依赖
RUN pip install --no-cache-dir flask requests loguru numpy skyfield networkx

# 设置工作目录
WORKDIR /usr/src/app

# 添加你的应用代码到容器中
ADD . /usr/src/app

# 运行你的程序
CMD [ "python", "./routerServer.py" ]
