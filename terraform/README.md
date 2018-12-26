# Terraform example

## Plan

```shell
terraform plan -var "client_id=$SERVICE_PRINCIPAL" -var "client_secret=$SERVICE_PRINCIPAL_PASSWORD" -out run.plan
```

## Apply the cluster

```shell
terraform apply "run.plan"
```