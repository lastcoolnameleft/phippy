provider "azurerm" {
  version = "=1.20.0"
}

resource "azurerm_resource_group" "phippy_k8s" {
  name     = "${var.resource_group_name}"
  location = "${var.location}"
}

resource "azurerm_kubernetes_cluster" "phippy_k8s" {
  name                = "${var.cluster_name}"
  location            = "${azurerm_resource_group.phippy_k8s.location}"
  resource_group_name = "${azurerm_resource_group.phippy_k8s.name}"
  dns_prefix          = "${var.dns_prefix}"
  kubernetes_version  = "${var.kubernetes_version}"
  
  linux_profile {
    admin_username = "${var.admin_username}"

    ssh_key {
      key_data = "${file("${var.ssh_public_key}")}"
    }
  }

  agent_pool_profile {
    name            = "default"
    count           = "${var.agent_count}"
    vm_size         = "Standard_DS2_v2"
    os_type         = "Linux"
    os_disk_size_gb = 30
  }

  service_principal {
    client_id     = "${var.client_id}"
    client_secret = "${var.client_secret}"
  }

  tags {
    Environment = "Production"
  }
}

resource "azurerm_storage_account" "phippy_k8s" {
  name                     = "phippy"
  resource_group_name      = "${azurerm_resource_group.phippy_k8s.name}"
  location                 = "${azurerm_resource_group.phippy_k8s.location}"
  account_tier             = "Standard"
  account_replication_type = "GRS"
}

resource "azurerm_container_registry" "test" {
  name                = "phippy"
  resource_group_name = "${azurerm_resource_group.phippy_k8s.name}"
  location            = "${azurerm_resource_group.phippy_k8s.location}"
  admin_enabled       = true
  sku                 = "Classic"
  storage_account_id  = "${azurerm_storage_account.phippy_k8s.id}"
}

