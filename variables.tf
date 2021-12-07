variable "prefix" {
    description = "The prefix used for all resources in this environment"
}
variable "location" {
    description = "The Azure location where all resources in this deployment should be created"
    default     = "uksouth"
}
variable "OAUTH_CLIENT_ID" {
    description = "OAuth ClientID"
    sensitive   = true
}
variable "OAUTH_CLIENT_SECRET" {
    description = "OAuth Secret"
    sensitive   = true
}