# Deployment (POC)
- Takes a repo URL, branch name & commit ID
- Clones down the repo, at the specific branch & commit
- Parses the launch.yaml file
- Handles the provided config file sections
  - Run: setup phase
  - Per site:
      - Run: tenant phase
	  - Generate all environment variables (including any resources)
	  - Create the envdir
	  - Generate the Nginx & uWSGI config files
	  - Send test traffic through the service

----

# Deployment sub-system:
- Handles deploying a service (based on branch & commit hash)
- When:
  - During container startup (each service's current deployed commit)
  - When a service is created
  - When a site is created
  - When a service's config is updated
  - When a new service commit is deployed

# Networking sub-system
- Updated to parse launch.yaml routes
- And generate appropriate Nginx & uWSGI config (per site)

# Resources sub-system
- Handles creating/managing resources on behalf of services/sites
- Provides config information for sites

# Communication sub-system
- Containers can send each other messages over a postgres notification channel

# Bridge sub-system
- Site -> management bridge API
  - Implement as separate bottle API
  - Endpoints:
    - Metadata
    - Auth (plugin based, example: SAML integration)
    - Identity (plugin based, example: LDAP integration)
    - Resources

# Workers sub-system
- Parses workers from launch.yaml
- Handles running workers on provided schedule (per site) using envdir

----

# Dashboard
- Updated dashboard interface that allows creation & management of services
- Update site interface that shows service-specific information

# API
- Create new management API routes for frontend changes
