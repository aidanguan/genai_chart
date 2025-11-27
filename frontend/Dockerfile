FROM node:20-alpine

# 设置工作目录
WORKDIR /app

# 复制 package 文件
COPY frontend/package*.json ./

# 安装依赖
RUN npm install

# 复制 antv_infographic 依赖
COPY antv_infographic/infographic /antv_infographic/infographic

# 复制应用代码
COPY frontend/. .

# 构建应用
RUN npm run build

# 使用 nginx 提供静态文件服务
FROM nginx:alpine

# 复制构建产物到 nginx
COPY --from=0 /app/dist /usr/share/nginx/html

# 复制 nginx 配置
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
