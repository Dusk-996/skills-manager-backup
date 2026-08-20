# systemd 交付模板

## service

```ini
[Unit]
Description=DevOps App
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=app
Group=app
WorkingDirectory=/opt/app/current
EnvironmentFile=/etc/app/app.env
ExecStart=/opt/app/current/app
Restart=always
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=true

[Install]
WantedBy=multi-user.target
```

## 部署

```bash
install -d /opt/app/releases/20260531-1 /etc/app
cp app /opt/app/releases/20260531-1/app
ln -sfn /opt/app/releases/20260531-1 /opt/app/current
cp app.service /etc/systemd/system/app.service
systemctl daemon-reload
systemctl enable --now app
systemctl status app
```

## 验证与回滚

```bash
journalctl -u app -n 100 --no-pager
curl -f http://127.0.0.1:8080/health

ln -sfn /opt/app/releases/previous /opt/app/current
systemctl restart app
```
