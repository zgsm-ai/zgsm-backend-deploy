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
        # Configure access to CSS, JS, PNG, SVG files
        location ~* \.(css|js|png|svg)$ {
            expires 1d;  # Set cache expiration time
            add_header Access-Control-Allow-Origin *;  # Allow access from all domains
            add_header Access-Control-Allow-Methods 'GET, OPTIONS';  # Allowed request methods
            add_header Access-Control-Allow-Headers 'Content-Type';  # Allowed request headers
        }

        # Configuration for other file types (optional)
        location ~* \.(jpg|jpeg|gif|ico|woff|woff2|ttf|eot)$ {
            expires 1d;  # Set cache expiration time
            add_header Access-Control-Allow-Origin *;  # Allow access from all domains
        }
    }
}
