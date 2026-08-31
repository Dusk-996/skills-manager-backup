# Nginx 前端托管模板

## nginx.conf

```nginx
server {
    listen 80;
    server_name ops.example.com;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|svg|ico|woff2?)$ {
        expires 7d;
        add_header Cache-Control "public";
    }
}
```

## 验证

```bash
npm run build
nginx -t
systemctl reload nginx
curl -I http://ops.example.com/
```

## 回滚

保留上一版 `dist` 目录，例如 `/data/www/app/releases/<version>`，通过 `current` 软链接切换：

```bash
ln -sfn /data/www/app/releases/previous /data/www/app/current
nginx -t && systemctl reload nginx
```
