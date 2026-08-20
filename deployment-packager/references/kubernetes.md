# Kubernetes 交付模板

## Deployment / Service / ConfigMap / Secret

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: "production"
---
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  TOKEN: "replace-me"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
        - name: app
          image: registry.example.com/app:20260531-1
          ports:
            - containerPort: 8080
          envFrom:
            - configMapRef:
                name: app-config
            - secretRef:
                name: app-secret
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 20
---
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  selector:
    app: app
  ports:
    - port: 80
      targetPort: 8080
```

## 验证

```bash
kubectl apply --dry-run=server -f k8s.yaml
kubectl apply -f k8s.yaml
kubectl rollout status deployment/app
kubectl get pod -l app=app -o wide
kubectl logs -l app=app --tail=100
```

## 回滚

```bash
kubectl rollout history deployment/app
kubectl rollout undo deployment/app
kubectl rollout status deployment/app
```

生产注意：执行 `kubectl delete` 前必须说明影响范围、备份、验证和回滚。
