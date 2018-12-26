# Terraform example

## Create the Terraform plan

```shell
terraform plan -var "client_id=$SERVICE_PRINCIPAL" -var "client_secret=$SERVICE_PRINCIPAL_PASSWORD" -out run.plan
```

## Create the cluster

```shell
terraform apply "run.plan"
```

## Cleanup

```shell
terraform destroy -var "client_id=$SERVICE_PRINCIPAL" -var "client_secret=$SERVICE_PRINCIPAL_PASSWORD"
```