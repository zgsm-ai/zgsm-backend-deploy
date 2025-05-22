FROM zgsm/chat-server:1.2.0

# Copy files into the container instead of mounting them as volumes
COPY server/ /server/
COPY supervisor/ /var/log/supervisor/
COPY custom.yml /custom.yml

# Create logs directory with proper permissions
RUN mkdir -p /server/logs && \
    chmod -R 755 /server/logs

# Command to start the service
CMD ["/sbin/entrypoint.sh", "app:start"]

# Default environment variables
ENV TZ=Asia/Shanghai \
    CACHE_DB=chatgpt \
    SERVE_THREADS=200 \
    SERVE_CONNECTION_LIMIT=512 \
    DB_NAME=chatgpt \
    CUSTOM_CONFIG_FILE=/custom.yml \
    GEVENT_SUPPORT=True \
    NO_COLOR=1 \
    DEPLOYMENT_TYPE=all

# Expose ports
EXPOSE 5000 8765 5555 