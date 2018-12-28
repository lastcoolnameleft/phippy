# Deployment

## Bootstrap database

```shell
kubectl port-forward svc/mysql 3308:3306
# Make temp changes to setting.py (port=3308, host, passwd, etc)
python manage.py migrate
```

# Deployment

## Deploy helm + mysql

```shell
# https://stackoverflow.com/questions/50309012/deploy-nginx-ingress-in-aks-without-rbac-issue
# https://github.com/Azure/kubernetes-volume-drivers/tree/master/flexvolume/blobfuse
kubectl create -f https://raw.githubusercontent.com/Azure/kubernetes-volume-drivers/master/flexvolume/blobfuse/deployment/blobfuse-flexvol-installer-1.9.yaml
```

## MySQL

```shell
helm install stable/mysql --name mysql --namespace mysql
MYSQL_ROOT_PASSWORD=$(kubectl get secret --namespace mysql mysql -o jsonpath="{.data.mysql-root-password}" | base64 --decode; echo)

# In separate window
kubens mysql
kubectl port-forward svc/mysql 3308:3306

mysql -u root -h 127.0.0.1 -P 3308 -p$MYSQL_ROOT_PASSWORD
CREATE DATABASE phippy_dev;
CREATE USER 'phippy_dev'@'10.244.%.%' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON phippy_dev.* to 'phippy_dev'@'10.244.%.%';
```

## Other services

```shell
helm install stable/nginx-ingress --namespace kube-system --name nginx-ingress

```

## Create Blob Fuse Secret

```shell
ACCOUNT_KEY=$(az storage account keys list -n phippy -g phippy -o json | jq '.[0].value' -r)
az storage container create -n dev --account-name phippy
az storage container create -n prod --account-name phippy
kubectl create secret generic blobfusecreds --from-literal accountname=phippy --from-literal accountkey="$ACCOUNT_KEY" --type="azure/blobfuse"
```

## Dev K8S Env

```shell
kubectl create ns dev
kubens dev
kubectl create secret generic phippy-django --from-file=config/aks-dev-django/settings.py
az acr login -n phippy
draft up
```

## Prod K8S env

```shell
kubectl create ns prod
kubens prod
kubectl create secret generic phippy-django --from-file=config/aks-prod-django/settings.py
helm install ../charts/phippy --name phippy-prod --namespace prod --values charts/php/values-prod.yaml
```
