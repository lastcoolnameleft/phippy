variable "resource_group_name" {
    default = "phippy" 
}
variable "location" {
    default = "centralus"
}
variable "dns_prefix" {
    default = "phippy"
}
variable "cluster_name" {
    default = "phippy"
}
variable "admin_username" {
    default = "thfalgou"
}
variable "agent_count" {
    default = "1"
}
variable "ssh_public_key" {
    default = "~/.ssh/id_rsa.pub"
}

variable "client_id" {
    type = "string"
}
variable "client_secret" {
    type = "string"
}