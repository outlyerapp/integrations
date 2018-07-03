Outlyer Integrations
====================

Outlyer Integration Packs allow you to create installable modules that 
can enable monitoring integrations with your services. At its core, an 
integration will encapsulate a plugin to deploy to the Outlyer agent to 
monitor the service and collect performance metrics and events, a 
dashboard template and alert template. Integration Packs can be 
installed in one click by users making Integrations completely 
self-service by any user in your Outlyer account.

This repository contains all our supported, out of the box, Integration 
Packs for all the common services our users rely on. We welcome 
contributions from users for other services we don't support currently, 
as well as improvements to our existing Integrations (See Contributing 
section below). 

## Building Integration Packs

You can find full instructions on how to build your own Integration Packs
[here](https://docs2.outlyer.com/development/integration-packs/)

## Contributing

Please ensure your Integrations are fully tested before submitting a 
pull request. In general, we follow the "fork-and-pull" Git workflow.

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request** so that we can review your changes

## Schema validation

The Python script in `./_test/validate.py` will check all plugin and package
YAML files to ensure correctness. Please run it before committing to
this repo or submitting a pull request.
