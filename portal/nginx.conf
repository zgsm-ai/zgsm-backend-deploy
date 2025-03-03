worker_processes 1;
error_log stderr notice;
events {
    worker_connections 1024;
}

http {
    variables_hash_max_size 1024;
    access_log off;
    real_ip_header X-Real-IP;
    charset utf-8;
    include /etc/nginx/mime.types;
    default_type  application/octet-stream;

    server {
        listen 80;

        root /var/www;
        index index.html;

        location / {
            try_files $uri $uri/ =404;
        }

        location /static/ {
            alias static/;
        }

        location /login/ {
            alias login/;
        }
        # 配置对 CSS、JS、PNG、SVG 文件的访问
        location ~* \.(css|js|png|svg)$ {
            expires 1d;  # 设置缓存过期时间
            add_header Access-Control-Allow-Origin *;  # 允许所有域访问
            add_header Access-Control-Allow-Methods 'GET, OPTIONS';  # 允许的请求方法
            add_header Access-Control-Allow-Headers 'Content-Type';  # 允许的请求头
        }

        # 其他文件类型的配置（可选）
        location ~* \.(jpg|jpeg|gif|ico|woff|woff2|ttf|eot)$ {
            expires 1d;  # 设置缓存过期时间
            add_header Access-Control-Allow-Origin *;  # 允许所有域访问
        }
    }
}
