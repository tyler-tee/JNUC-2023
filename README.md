# API endpoints

These endpoints allow you to interact with Jamf Pro App Installers and their deployments programmatically.

## GET
[/v1/app-installers/titles/](#app-installers-titles)<br/>
[/v1/app-installers/titles/{TITLE_ID}](#app-installers-titles-titleid) <br/>
[/v1/app-installers/deployments](#app-installers-deployments) <br/>
[/v1/app-installers/deployments/{DEPLOYMENT_ID}](#app-installers-deployments-deployid) <br/>
[/v1/app-installers/deployments/{DEPLOYMENT_ID}/computers](#app-installers-deployments-computers) <br/>
[/v1/app-installers/deployments/{DEPLOYMENT_ID}/installation-summary](#app-installers-deployments-install-summary) <br/>


## POST
[/v1/app-installers/deployments/{DEPLOYMENT_ID}/computers/installation-retry](#app-installers-retry) <br/>
[/v1/app-installers/deployments/{DEPLOYMENT_ID}/computers/{COMPUTER_ID}/installation-retry](#app-installers-computers-retry) <br/>

___

### GET /v1/app-installers/titles/
Get all available App Instalers from the Jamf Pro App Catalog.
                                                                   
**Response**

```
{
    "totalCount": integer,
    "results": [
        {
            "id": string,
            "bundleId": string,
            "titleName": string,
            "publisher": string,
            "iconUrl": string,
            "version": string
        },
        ...
    ]
}
```

___

### GET /v1/app-installers/titles/{TITLE_ID}
Get details for a particular App Installer by supplying its ID.

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|    `TITLE_ID` | true | string  | Can be retrieved using /v1/app-installers/titles/         |
                                                                   
**Response**

```
{
    "id": string,
    "bundleId": string,
    "titleName": string,
    "publisher": string,
    "iconUrl": string,
    "version": string,
    "sizeInBytes": integer,
    "minimumOsVersion": string,
    "language": string,
    "availabilityDate": string,
    "packageSigningIdentity": string,
    "installerPackageHashType": string,
    "installerPackageHash": string,
    "shortVersion": string,
    "architecture": string,
    "originalMediaSources": [
        {
        "hashType": string,
        "hash": string,
        "url": string
        }
    ],
    "launchDaemonIncluded": boolean,
    "notificationAvailable": boolean,
    "suppressAutoUpdate": boolean
    }
```
___

### GET /v1/app-installers/deployments/
Get all deployed App Installers (enabled or not) from your Jamf Pro instance.
                                                                   
**Response**

```
{
    "totalCount": integer,
    "results": [
        {
            "id": string,
            "name": string,
            "enabled": boolean,
            "selectedVersion": string,
            "latestVersion": string,
            "deploymentType": string,
            "updateBehavior": string,
            "site": {
                "id": string,
                "name": string
            },
            "smartGroup": {
                "id": string,
                "name": string
            },
            "category": {
                "id": string,
                "name": string
            },
            "computerStatuses": {
                "installed": integer,
                "available": integer,
                "inProgress": integer,
                "failed": integer,
                "unqualified": integer
            },
            "bundleId": string
        },
        ...
    ]
}
```

___

### GET /v1/app-installers/deployments/{DEPLOYMENT_ID}
Get details for a particular App Installer deployment by supplying the corresponding deployment ID.

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|    `DEPLOYMENT_ID` | true | string  | Can be retrieved using /v1/app-installers/deployments/         |
                                                                   
**Response**

```
        {
            "id": string,
            "name": string,
            "enabled": boolean,
            "appTitleId": string,
            "deploymentType": string,
            "updateBehavior": string,
            "siteId": string,
            "smartGroupId": string,
            "installPredefinedConfigProfiles": string,
            "titleAvailableInAis": boolean
            "notificationSettings": {
                "notificationMessage": string,
                "notificationInterval": integer,
                "deadlineMessage": string,
                "deadline": string,
                "quitDelay": string,
                "completeMessage": string,
                "relaunch": boolean
            },
            "selfServiceSettings": {
                "includeInFeaturedCategory": boolean,
                "includeInComplianceCategory": boolean,
                "forceViewDescription": boolean,
                "description": string,
                "categories": [
                {
                    "id": string,
                    "featured": boolean
                }
                ]
            },
            "selectedVersion": string,
            "latestAvailableVersion": string
        }
```
___

### GET /v1/app-installers/deployments/{DEPLOYMENT_ID}/computers

Get a system-level summary for a particular App Installer deployment.

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|    `DEPLOYMENT_ID` | true | string  | Can be retrieved using /v1/app-installers/deployments/         |
                                                                   
**Response**

```
{
    "totalCount": integer,
    "results": [
    {
        "id": string,
        "status": string,
        "error": string,
        "retryable": boolean,
        "computerName": string
    }
    ]
}
```
___

### GET /v1/app-installers/deployments/{DEPLOYMENT_ID}/installation-summary

Get the installation summary for a particular App Installer deployment.

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|    `DEPLOYMENT_ID` | true | string  | Can be retrieved using /v1/app-installers/deployments/         |
                                                                   
**Response**

```
{
    "installed": integer,
    "available": integer,
    "inProgress": integer,
    "failed": integer,
    "unqualified": integer
}
```
___

### POST /v1/app-installers/deployments/{DEPLOYMENT_ID}/computers/installation-retry

Issue a RETRY for failed App Installer installations for a deployment by providing its ID.

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|    `DEPLOYMENT_ID` | true | string  | Can be retrieved using /v1/app-installers/deployments/         |
                                                                   
**Response**

```
// Status 204 indicates successful retry submission
```
___

### POST /v1/app-installers/deployments/{DEPLOYMENT_ID}/computers/{COMPUTER_ID}/installation-retry

Retry a failed App Installer installation for a single system.

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|    `DEPLOYMENT_ID` | true | string  | Can be retrieved using /v1/app-installers/deployments/         |
|    `COMPUTER_ID` | true | string  | ID used to identify Computer in Jamf Pro.         |
                                                                   
**Response**
```
// Status 204 indicates successful retry submission
```
___