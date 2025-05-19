FROM zgsm/copilot_proxy:1.5.15

# Copy custom files into the image
COPY common-v1.5.15.py /python-docker/utils/common.py
COPY tgi_proxy_v2.py /python-docker/instances/tgi_proxy_v2.py
COPY api_manager.py /python-docker/thrid_platform/openai_server/api_manager.py
COPY model_client_service.py /python-docker/services/model_client_service.py
COPY log_config.py /python-docker/config/log_config.py

# Set default environment variables for logging
ENV LOG_LEVEL=INFO
ENV LOG_FORMAT=standard

# Set working directory
WORKDIR /python-docker

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"] 