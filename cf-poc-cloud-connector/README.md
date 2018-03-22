# cf-poc-cloud-connector

This is a reference app written in python, with the bare minimum that 
is necessary to access an on-premise resources from _SAP Cloud Platform - Cloud Foundry_ 
using _SAP Cloud Connector_.

The app access an internal REST service from our JIRA QA instance at the address
https://sapjira-qa-app.wdf.sap.corp/rest/api/2/serverInfo and shows the result  

The code here is not a best practice as it aims for easy understanding of each basic step
necessary to do a request to an on-prem systems, therefore it does "manually" what could 
pottentially be achieved by reusing standard libraries.

# Instructions

1. Adjust the manifest and security configuration  
   Open the file `manifest.yml`, follow the instructions on the comments  
   Open the file `approuter/security.json` and change the name of the app (i.e.: `cf-poc-cloud-connector-<your user>`)
2. Create the necessary services. Below we list the command lines to create them using the 
   [Cloud Foundry CLI](https://github.com/cloudfoundry/cli)  
   `cf cs xsuaa application cf-poc-cc-uaa -c approuter\security.json`  
   `cf cs destination lite cf-poc-cc-destination`  
   `cf cs connectivity lite cf-poc-cc-connectivity`
3. Configure an instace of the Cloud Connector.  
   You can run your own instance, even in your own pc, or subscribe to a DLM hosted instance as 
   described [here](https://wiki.wdf.sap.corp/wiki/display/HCPCollaboration/Development+Project+Setup#DevelopmentProjectSetup-CreateAccountforDLMManagedCloudConnector).  
   For more information on how to configure the connection between the Cloud Connector and the 
   Canary instance of Cloud Foundry, refer to the [this Jam Blog](https://jam4.sapjam.com/wiki/show/A9IVxXkRiGY7DuMgcOtdi9)  
   Configure the _Cloud To On-Premise_ configuration as shown on [this screenshot](screenshots/cloud_connector_cloud_to_onpremise_configuration.png)
4. Configure the _Destination_ configuration as shown on [this screenshot](screenshots/destination_configuration.png)  
   Pay attention to the URL, even though we are accessing a HTTPS resource, we have to write the URL 
   with HTTP protocol and explicitely user port 443, as the _connectivity_ service only supports HTTP proxy.
   Use your own credentials.
5. Vendor the requirements, as explained in the section [CF Deployment](https://github.wdf.sap.corp/xs2/PySec#cf-deployment) of the PySec readme file.
6. Push your app with the command line `cf push`

# References

* [PySec - Internal Github](https://github.wdf.sap.corp/xs2/PySec)
* [SAP Help - Consuming the destination and connectivity services](https://help.sap.com/viewer/cca91383641e40ffbe03bdc78f00f681/Cloud/en-US/34010ace6ac84574a4ad02f5055d3597.html)
* [SAP Community blog - How to use SAP Cloud Platform Connectivity and Cloud Connector in the Cloud Foundry environment](https://blogs.sap.com/2017/07/09/how-to-use-the-sap-cloud-platform-connectivity-and-the-cloud-connector-in-the-cloud-foundry-environment-part-1/)
* [SAP Help - Cloud Connector](https://help.sap.com/viewer/cca91383641e40ffbe03bdc78f00f681/Cloud/en-US/e6c7616abb5710148cfcf3e75d96d596.html)
* [SAP Cloud Platform Core Product Management Team - Jam Group](https://jam4.sapjam.com/groups/sQlem2KIGQfhT8wAaeHmb4/overview_page/HpPYLp0rPgXnL8FBDPj5qZ)