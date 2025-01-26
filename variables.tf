# Atlas Organization ID
variable "atlas_org_id" {
  type        = string
  description = "Atlas Organization ID"
  sensitive   = true  # Marking this as sensitive
}

# Atlas Project Name
variable "atlas_project_name" {
  type        = string
  description = "Atlas Project Name"
}

# Atlas Project Environment
variable "environment" {
  type        = string
  description = "The environment to be built"
}

# Cluster Instance Size Name
variable "cluster_instance_size_name" {
  type        = string
  description = "Cluster instance size name"
}

# Atlas Region
variable "atlas_region" {
  type        = string
  description = "Atlas region where resources will be created"
}

# MongoDB Version
variable "mongodb_version" {
  type        = string
  description = "MongoDB Version"
}

# IP Address Access
variable "ip_address" {
  type        = string
  description = "IP address used to access Atlas cluster"
}

# MongoDB Atlas API Key
variable "atlas_api_key" {
  type        = string
  description = "MongoDB Atlas API key to manage resources"
  sensitive   = true  # Marking as sensitive
}

# MongoDB Atlas API Username
variable "atlas_api_username" {
  type        = string
  description = "MongoDB Atlas API username"
  sensitive   = true  # Marking as sensitive
}

# MongoDB Atlas Cluster Connection String
variable "atlas_connection_string" {
  type        = string
  description = "MongoDB Atlas cluster connection string"
  sensitive   = true  # Marking as sensitive
}

# Databricks Host URL
variable "databricks_host" {
  type        = string
  description = "The Databricks instance URL"
  sensitive   = true
}

# Databricks API Token (for authentication with Databricks API)
variable "databricks_token" {
  type        = string
  description = "Databricks API token for authentication"
  sensitive   = true  # Sensitive variable
}

# Databricks Cluster Node Type ID
variable "databricks_node_type" {
  type        = string
  description = "Databricks cluster node type"
}

# Databricks Cluster Spark Version
variable "databricks_spark_version" {
  type        = string
  description = "Databricks Spark version"
}

# Databricks Cluster Autotermination Timeout
variable "databricks_autotermination_minutes" {
  type        = number
  description = "Number of minutes of inactivity before cluster is terminated"
}

# Databricks Libraries (for LlamaIndex)
variable "databricks_libraries" {
  type        = list(string)
  description = "List of libraries to be installed on the Databricks cluster"
  default     = ["llama-index"]  # LlamaIndex by default
}