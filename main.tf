terraform {
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = ">= 2.49"
        }
    }
    backend "azurerm" {
        resource_group_name  = "McLaren1_GeorgeAnker_ProjectExercise"
        storage_account_name = "tfstate1099930277"
        container_name       = "tfstate"
        key                  = "terraform.tfstate"
    }
}
provider "azurerm" {
    skip_provider_registration = "true"
    features {}
}
data "azurerm_resource_group" "main" {
    name = "McLaren1_GeorgeAnker_ProjectExercise"
}
resource "azurerm_cosmosdb_account" "main" {
    name = "${var.prefix}-terraformed-cdb-a"
    location = data.azurerm_resource_group.main.location
    resource_group_name = data.azurerm_resource_group.main.name
    offer_type = "Standard"
    kind = "MongoDB"
    capabilities {
        name = "EnableServerless"
    } 
    capabilities {
        name = "EnableMongo"
    }
    consistency_policy {
        consistency_level = "BoundedStaleness"
        max_interval_in_seconds = 10
        max_staleness_prefix = 200
    }
    geo_location {
        location = data.azurerm_resource_group.main.location
        failover_priority = 0
    }
}
resource "azurerm_cosmosdb_mongo_database" "main" {
    name = "${var.prefix}-terraformed-cdb-m-db"
    resource_group_name = data.azurerm_resource_group.main.name
    account_name = azurerm_cosmosdb_account.main.name
    lifecycle {
        prevent_destroy = true
    }
}
resource "azurerm_app_service_plan" "main" {
    name = "${var.prefix}-terraformed-asp"
    location = data.azurerm_resource_group.main.location
    resource_group_name = data.azurerm_resource_group.main.name
    kind = "Linux"
    reserved = true
    sku {
        tier = "Basic"
        size = "B1"
    }
}
resource "azurerm_app_service" "main" {
    name = "${var.prefix}-terraformed-as"
    location = data.azurerm_resource_group.main.location
    resource_group_name = data.azurerm_resource_group.main.name
    app_service_plan_id = azurerm_app_service_plan.main.id
    site_config {
        app_command_line = ""
        linux_fx_version = "DOCKER|mrlganker/todo-app:latest"
    }
        app_settings = {
        "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
        "FLASK_APP" = "todo_app/app"
        "FLASK_ENV" = "development"
        "MONGO_USERNAME" = "${azurerm_cosmosdb_account.main.name}"
        "MONGO_PASSWORD" = "${azurerm_cosmosdb_account.main.primary_key}"
        "MONGO_URL" = "${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255"
        "MONGO_PROTOCOL" = "mongodb"
        "MONGO_DATABASE" = "ToDo"
        "OAUTH_CLIENT_ID"="${var.OAUTH_CLIENT_ID}"
        "OAUTH_CLIENT_SECRET"="${var.OAUTH_CLIENT_SECRET}"
    }
}