FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（包括 Cairo 图形库、中文字体和lxml依赖）
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-noto-cjk \
    fonts-noto-cjk-extra \
    fontconfig \
    libxml2-dev \
    libxslt-dev \
    && fc-cache -fv \
    && rm -rf /var/lib/apt/lists/*

# 复制字体配置文件
COPY backend/fonts.conf /etc/fonts/local.conf
RUN fc-cache -fv

# 复制依赖文件
COPY backend/requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY backend/. .

# 创建必要的目录
RUN mkdir -p temp/exports data

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
