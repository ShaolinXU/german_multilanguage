# 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装依赖
RUN apt-get update && \
  apt-get install -y wget gnupg2 curl unzip \
  fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
  libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 \
  libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
  libgbm1 libgtk-3-0 libxshmfence1 libxss1 libxtst6 lsb-release \
  xdg-utils && \
  rm -rf /var/lib/apt/lists/*

# 安装 Chrome 浏览器
RUN wget -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
  apt-get update && \
  apt-get install -y /tmp/chrome.deb && \
  rm /tmp/chrome.deb

# 安装 ChromeDriver（自动适配 Chrome 版本）
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
  CHROMEDRIVER_VERSION=$(curl -sS "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['channels']['Stable']['version'])") && \
  wget -O /tmp/chromedriver.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" && \
  unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
  mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
  chmod +x /usr/local/bin/chromedriver && \
  rm -rf /tmp/chromedriver.zip /usr/local/bin/chromedriver-linux64

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 暴露 Streamlit 默认端口
EXPOSE 8501

# 启动 Streamlit 服务
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]