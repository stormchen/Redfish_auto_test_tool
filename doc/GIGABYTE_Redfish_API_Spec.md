GIGABYTE Proprietary & Confidential
GIGABYTE Redfish API Spec 1.11.0
Document No.:
Authors: Approved By:
Wenny Chen TS Hwang
Eason Tsai PJ Sun
Bob Wang
Storm Chen
Iris Wang
PROPRIETARY INFORMATION -- NOT FOR PUBLICATION
The information contained herein is the property of Gigabyte Technology Co., Ltd. and is
supplied without liability for errors or omissions. No part may be reproduced or used except as
authorized by contract or other written permission. The copyright and the foregoing restriction on
reproduction and use extend to all media in which the information may be embodied.
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 1/54

GIGABYTE Proprietary & Confidential
C o n t e n t s
0. General Information ............................................................................................................................................. 5
0.1. Issue Control ........................................................................................................................................................ 5
0.2. Record of Changes .............................................................................................................................................. 5
0.3. References ........................................................................................................................................................... 5
0.4. Acronyms ............................................................................................................................................................ 5
0.5. Change History .................................................................................................................................................... 5
1. Introduction ........................................................................................................................................................... 7
2. Redfish request methods ....................................................................................................................................... 7
2.1. HTTP GET (Read) .............................................................................................................................................. 7
2.2. HTTP POST (Create) .......................................................................................................................................... 7
2.3. HTTP PATCH (Partial Update) .......................................................................................................................... 7
2.4. HTTP DELETE (Delete) ..................................................................................................................................... 7
3. Redfish API ............................................................................................................................................................ 7
Resource API ................................................................................................................................................................. 7
Notes ............................................................................................................................................................................... 7
4. Common Field to all Schemas ............................................................................................................................ 13
5. ServiceRoot .......................................................................................................................................................... 13
6. ODATA ................................................................................................................................................................ 14
7. $metadata ............................................................................................................................................................. 14
8. AccountService .................................................................................................................................................... 14
8.1. Account Collection ............................................................................................................................................ 14
8.1.1. Accounts .................................................................................................................................................... 15
8.2. PAM Configuration ........................................................................................................................................... 15
8.3. Radius Authentication ....................................................................................................................................... 15
8.3.1. AdvancedRADIUSSetting ......................................................................................................................... 16
8.4. Role Collection .................................................................................................................................................. 16
8.4.1. Role ........................................................................................................................................................... 16
9. CertificateService ................................................................................................................................................ 16
9.1. CertificateLocations .......................................................................................................................................... 18
9.1.1. Certificate .................................................................................................................................................. 18
10. Chassis Collection ............................................................................................................................................ 19
10.1. Chassis ........................................................................................................................................................... 20
10.1.1. Power ......................................................................................................................................................... 21
10.1.2. LogServices (Support services after version 12.41.07) ............................................................................. 22
10.1.2.1. Log Service .........................................................................................................................................................22
10.1.3. Sensor Collection ....................................................................................................................................... 23
10.1.3.1. Sensor ..................................................................................................................................................................23
10.1.3.2. Sensor Energy .....................................................................................................................................................24
10.1.3.3. Sensor Power.......................................................................................................................................................24
10.1.4. Thermal ..................................................................................................................................................... 24
10.1.4.1. FanprofileService (GBT) .....................................................................................................................................25
10.1.5. NetworkAdapterCollection ........................................................................................................................ 26
10.1.5.1. NetworkAdapter ..................................................................................................................................................26
10.1.6. PCIeDevice Collection .............................................................................................................................. 26
10.1.6.1. PCIeDecice..........................................................................................................................................................26
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 2/54

GIGABYTE Proprietary & Confidential
11. CompositionService .......................................................................................................................................... 27
11.1. ResourceBlocks Collection ............................................................................................................................ 27
11.1.1. ResourceBlocks ......................................................................................................................................... 27
11.2. ResourceZones Collection ............................................................................................................................. 27
11.2.1. ResourceZones .......................................................................................................................................... 27
12. AMI OEM Entities - Configuration ................................................................................................................. 28
13. EventService ..................................................................................................................................................... 28
13.1. Subscription Collection ................................................................................................................................. 29
13.1.1. Subscription ............................................................................................................................................... 29
13.1.2. Subscription Test Event ............................................................................................................................. 30
14. JsonSchemas Collection .................................................................................................................................. 30
14.1. JsonSchemas .................................................................................................................................................. 30
15. Manager Collection ......................................................................................................................................... 30
15.1. Manager ......................................................................................................................................................... 30
15.1.1. EthernetInterfaces Collection .................................................................................................................... 31
15.1.1.1. EthernetInterfaces ...............................................................................................................................................31
15.1.2. CertificateCollection .................................................................................................................................. 34
15.1.3. Factory Reset ActionInfo ........................................................................................................................... 34
15.1.4. HostInterfaces Collection .......................................................................................................................... 34
15.1.4.1. HostInterfaces .....................................................................................................................................................34
15.1.4.2. HostEthernetInterface Collection ........................................................................................................................34
15.1.5. LogServices Collection.............................................................................................................................. 35
15.1.5.1. LogServices .........................................................................................................................................................35
15.1.6. NetworkProtocol ........................................................................................................................................ 36
15.1.7. Reset ActionInfo ........................................................................................................................................ 37
15.1.8. SerialInterfaces Collection ........................................................................................................................ 37
15.1.8.1. SerialInterfaces ....................................................................................................................................................37
15.1.9. VirtualMedia Collection ............................................................................................................................ 38
15.1.9.1. VirtualMedia Collection ......................................................................................................................................38
16. - InventoryDataMessage Registry File Collection.......................................................................................... 39
16.1. Message Registries ........................................................................................................................................ 39
16.2. Message Registries File ................................................................................................................................. 39
17. Session Service ................................................................................................................................................. 39
17.1. Session Collection ......................................................................................................................................... 39
17.1.1. Session ....................................................................................................................................................... 40
18. System Collection............................................................................................................................................. 40
18.1. Capabilities .................................................................................................................................................... 40
18.2. System ........................................................................................................................................................... 41
18.2.1. BIOS .......................................................................................................................................................... 42
18.2.1.1. BIOS SD .............................................................................................................................................................42
18.2.2. BootOption Collection ............................................................................................................................... 43
18.2.2.1. BootOptions ........................................................................................................................................................43
18.2.3. EthernetInterfaces Collection .................................................................................................................... 43
18.2.3.1. EthernetInterfaces ...............................................................................................................................................43
18.2.4. LogServices Collection.............................................................................................................................. 44
18.2.4.1. LogServices .........................................................................................................................................................44
18.2.5. Memory Collection .................................................................................................................................... 45
18.2.5.1. Memory ...............................................................................................................................................................45
18.2.6. MemoryDomains Collection ..................................................................................................................... 46
18.2.7. NetworkInterface Collection ..................................................................................................................... 46
18.2.7.1. NetworkInterface.................................................................................................................................................46
18.2.8. Processor Collection .................................................................................................................................. 47
18.2.8.1. Processor .............................................................................................................................................................47
18.2.9. SimpleStorage Collection .......................................................................................................................... 47
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 3/54

GIGABYTE Proprietary & Confidential
18.2.9.1. SimpleStorage .....................................................................................................................................................48
18.2.10. Storage Collection ................................................................................................................................. 48
18.2.10.1. Storage ................................................................................................................................................................48
19. - RedundancyTaskService ............................................................................................................................... 48
19.1. Task Collection .............................................................................................................................................. 48
19.1.1. Task ........................................................................................................................................................... 49
20. TelemetryService ............................................................................................................................................... 49
20.1. MetricReportLog Collection .......................................................................................................................... 49
20.1.1. MetricReportLog ....................................................................................................................................... 50
20.1.1.1. Entries Collection ................................................................................................................................................50
20.2. MetricDefinitions Collection ......................................................................................................................... 51
20.2.1. - NameMetricDefinitions ........................................................................................................................... 51
20.3. MetricReportDefinition Collection ................................................................................................................ 51
20.3.1. MetricReportDefinitions ............................................................................................................................ 51
20.4. MetricReports Collection .............................................................................................................................. 52
20.4.1. - NameMetricReports ................................................................................................................................ 52
20.5. Triggers Collection ........................................................................................................................................ 52
20.5.1. Triggers ..................................................................................................................................................... 53
21. UpdateService .................................................................................................................................................. 53
21.1. SimpleUpdateActionInfo ............................................................................................................................... 53
21.2. FirmwareInventory Collection....................................................................................................................... 54
21.2.1. FirmwareInventory .................................................................................................................................... 54
F i g u r e s
T a b l e s
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 4/54

| GIGABYTE  |     |     |     |     |     |     | Proprietary & Confidential  |     |
| --------- | --- | --- | --- | --- | --- | --- | --------------------------- | --- |

0.  General Information

0.1.  Issue Control
This document was edited with Microsoft Word, Version 2003. The graphic drawings are originally sketched in
Microsoft PowerPoint Version 2003.

0.2.  Record of Changes
Table 0-1.  Record of Changes
|     | Issue  | Date        | Authors     |                   | Reason for Changes  |     |     |     |
| --- | ------ | ----------- | ----------- | ----------------- | ------------------- | --- | --- | --- |
|     | 1.00   | 01/07/2022  | Eason Tsai  | Creation          |                     |     |     |     |
|     | 1.01   | 10/19/2022  | Eason Tsai  | Change some URIs  |                     |     |     |     |
1.02  04/28/2023  Bob Wang  Add NetworkAdapters Info and remove unsupported URIs
1.03  05/16/2023  Wenny Chen  Remove AccelerationFunctions unsupported URI
1.04  06/01/2023  Eason Tsai  Fix typo and remove certificate rekey&renew related description
|     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

0.3.  References
|     | 1  Redfish Resource and Schema Guide(DSP2046)                        |     |     |     |     |     |     |     |
| --- | -------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|     | 2  Redfish Scalable Platforms Management API Specification(DSP0266)  |     |     |     |     |     |     |     |
|     |                                                                      |     |     |     |     |     |     |     |
|     |                                                                      |     |     |     |     |     |     |     |
|     |                                                                      |     |     |     |     |     |     |     |
|     |                                                                      |     |     |     |     |     |     |     |
|     |                                                                      |     |     |     |     |     |     |     |
|     |                                                                      |     |     |     |     |     |     |     |
|     |                                                                      |     |     |     |     |     |     |     |
|     |                                                                      |     |     |     |     |     |     |     |

0.4.  Acronyms
|     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |     |     |
|     |     |     |     |     |     |     |     |     |
|     |     |     |     |     |     |     |     |     |
0.5.  Change History

Method: GET, POST, PATCH, DELETE
Action: AU – Add URI, MU – Modify URI, DU – Delete URI
AP – Add Property, MP – Modify Property, DP – Delete Property
1.11.0.001
|                                                |     |     |     | URI  |     |     | Method  | Action  |
| ---------------------------------------------- | --- | --- | --- | ---- | --- | --- | ------- | ------- |
| /redfish/v1/Chassis/{instance}                 |     |     |     |      |     |     | GET     | AP      |
| /redfish/v1/Chassis/{instance}/Power/Voltages  |     |     |     |      |     |     | GET     | AP      |
/redfish/v1/Chassis/{instance}/Thermal /Temperatures  GET  AP
| /redfish/v1/Chassis/{instance}/Thermal /Fans  |     |     |     |     |     |     | GET  | AP  |
| --------------------------------------------- | --- | --- | --- | --- | --- | --- | ---- | --- |
/redfish/v1/Chassis/{instance}/LogServices/Logs  GET/PATCH  AU
/redfish/v1/Chassis/{instance}/LogServices/Logs/Actions/LogService.ClearLog  POST  AU
/redfish/v1/Chassis/{instance}/LogServices/Logs/Entries  GET  AU
/redfish/v1/Chassis/{instance}/LogServices/Logs/Entries/{instance}  GET  AU
| /redfish/v1/Chassis/{instance}/PCIeDevices  |     |     |     |     |     |     | GET  | AU  |
| ------------------------------------------- | --- | --- | --- | --- | --- | --- | ---- | --- |
/redfish/v1/Chassis/{instance}/PCIeDevices/{instance}  GET  AP
| © Copyright Gigabyte 2017  |     |     |        |     |     |     | All Rights Reserved  |     |
| -------------------------- | --- | --- | ------ | --- | --- | --- | -------------------- | --- |
  EasonWenny  GIGABYTE Redfish API Spec  GIGABYTE Redfish API Spec 1.11.0
|     |     | ChenTsai        |     |     |     | Doc V1.04 (AMI).Doc  |     |       |
| --- | --- | --------------- | --- | --- | --- | -------------------- | --- | ----- |
|     |     | 0605/1601/2023  |     |     |     |                      |     | 5/54  |

| GIGABYTE  |     |     |     | Proprietary & Confidential  |     |
| --------- | --- | --- | --- | --------------------------- | --- |

| /redfish/v1/TelemetryService                       |     |     |     | PATCH  | AU  |
| -------------------------------------------------- | --- | --- | --- | ------ | --- |
| /redfish/v1/Chassis/{instance}/Sensors             |     |     |     | GET    | AU  |
| /redfish/v1/Chassis/{instance}/Sensors/{instance}  |     |     |     | GET    | AU  |
/redfish/v1/TelemetryService/MetricReportDefinitions/{instance}  GET  AP
/redfish/v1/TelemetryService/MetricReports/{instance}  GET  AP
/redfish/v1/TelemetryService/LogService/Actions/LogService.ClearLog  POST  AU
| /redfish/v1/Systems/{instance}/Bios/SD  |     |     |     | POST  | AP  |
| --------------------------------------- | --- | --- | --- | ----- | --- |
/redfish/v1/Systems/{instance}/BootOptions/{instance}  GET  AU
/redfish/v1/Systems/{instance}/EthernetInterfaces/{instance}/VLANs  POST  AU
/redfish/v1/Systems/{instance}/EthernetInterfaces/{instance}/VLANs/{instance}  PATCH  AU
/redfish/v1/Systems/{instance}/EthernetInterfaces/{instance}/VLANs/{instance}  DELETE  AU
/redfish/v1/Managers/{instance}/Actions/Oem/AMIManager.RedfishDBReset  POST  AU
| /redfish/v1/Managers/{instance}  |     |     |     | GET  | AP  |
| -------------------------------- | --- | --- | --- | ---- | --- |
/redfish/v1/Managers/{instance}/HostInterfaces/{instance}  PATCH  AU
| /redfish/v1/AccountService  |     |     |     | GET  | AP  |
| --------------------------- | --- | --- | --- | ---- | --- |
/redfish/v1/AccountService/ExternalAccountProviders/RADIUS  GET  AU
/redfish/v1/AccountService/ExternalAccountProviders/RADIUS  PATCH  AU
/redfish/v1/AccountService/ExternalAccountProviders/RADIUS/Oem/Ami/AdvancedRA GET/PATCH  AU
DIUSSetting
| /redfish/v1/EventService                           |     |     |     | GET        | AP  |
| -------------------------------------------------- | --- | --- | --- | ---------- | --- |
| /redfish/v1/EventService/Subscriptions/{instance}  |     |     |     | GET        | AP  |
| /redfish/v1/UpdateService                          |     |     |     | GET/PATCH  | AP  |
| /redfish/v1/Oem/Ami/InventoryData/Status           |     |     |     | GET        | AP  |
| /redfish/v1/UpdateService/FirmwareInventory        |     |     |     | GET        | AU  |
/redfish/v1/UpdateService/FirmwareInventory/{instance}  GET  AU
| /redfish/v1/CertificateService  |     |     |     | GET  | AU  |
| ------------------------------- | --- | --- | --- | ---- | --- |
/redfish/v1/CertificateService/Actions/CertificateService.GenerateCSR  POST  AU
/redfish/v1/CertificateService/Actions/CertificateService.ReplaceCertificate  POST  AU
/redfish/v1/CertificateService/CertificateLocations  GET  AU
/redfish/v1/Managers/{instance}/NetworkProtocol/HTTPS/Certificates  GET  AU
/redfish/v1/Managers/{instance}/NetworkProtocol/HTTPS/Certificates/{instance}  GET  AU
| /redfish/v1/ AccountService/LDAP/Certificates/1  |     |     |     | GET  | AU  |
| ------------------------------------------------ | --- | --- | --- | ---- | --- |
/redfish/v1/ AccountService/LDAP/Certificates/Oem/Ami/ClientCertificates/1  GET  AU
| /redfish/v1/ AccountService/LDAP/Certificates  |     |     |     | POST  | AU  |
| ---------------------------------------------- | --- | --- | --- | ----- | --- |
/redfish/v1/ AccountService/LDAP/Certificates/Oem/Ami/ClientCertificates  POST  AU
| /redfish/v1/AccountService/LDAP/Certificates/1  |     |     |     | DELETE  | AU  |
| ----------------------------------------------- | --- | --- | --- | ------- | --- |
/redfish/v1/ AccountService/LDAP/Certificates/Oem/Ami/ClientCertificates/1  DELETE  AU
/redfish/v1/AaccountService/Accounts/{instance}/Certificates/{instance}/Actions/Certific POST  AU
ate.Rekey
redfish/v1/AaccountService/Accounts/{instance}/Certificates/{instance}/Actions/Certifica POST  AU
te.Renew

| © Copyright Gigabyte 2017  |     |        |     | All Rights Reserved  |     |
| -------------------------- | --- | ------ | --- | -------------------- | --- |
  EasonWenny  GIGABYTE Redfish API Spec  GIGABYTE Redfish API Spec 1.11.0
|     | ChenTsai        |     | Doc V1.04 (AMI).Doc  |     |       |
| --- | --------------- | --- | -------------------- | --- | ----- |
|     | 0605/1601/2023  |     |                      |     | 6/54  |

GIGABYTE Proprietary & Confidential
1. Introduction
The Redfish Scalable Platform Management API ("Redfish") is a management standard using a data model
representation inside of a hypermedia RESTful interface. Because it is based on REST, Redfish is easier to use and
implement than many other solutions. Since it is model oriented, it is capable of expressing the relationships between
components in modern systems as well as the semantics of the services and components within them. It is also easily
extensible. By using a hypermedia approach to REST, Redfish can express a large variety of systems from multiple
vendors. By requiring JSON representation, a wide variety of resources can be created in a denormalized fashion not
only to improve scalability, but the payload can be easily interpreted by most programming environments as well as
being relatively intuitive for a human examining the data. The model is exposed in terms of an interoperable Redfish
Schema, expressed in an OData Schema representation with translations to a JSON Schema representation, with the
payload of the messages being expressed in a JSON following OData JSON conventions. The ability to externally
host the Redfish Schema definition of the resources in a machine-readable format allows the meta data to be
associated with the data without encumbering Redfish services with the meta data, thus enabling more advanced
client scenarios as found in many data center and cloud environments.
2. Redfish request methods
The following HTTP methods are provided on our Redfish APIs.
2.1. HTTP GET (Read)
Use GET requests to retrieve resource representation/information only. For any given HTTP GET API, if
resource is found on server then it must return HTTP response code 200 (OK) – along with response body which is
JSON content. In case resource is NOT found on server then it must return HTTP response code 404 (NOT FOUND).
Similarly, if it is determined that GET request itself is not correctly formed then server will return HTTP response
code 400 (BAD REQUEST).
2.2. HTTP POST (Create)
Use POST APIs to create new subordinate resources, POST methods are used to create a new resource into the
collection of resources. In this case, either HTTP response code 200 (OK) or 204 (No Content) is the appropriate
response status.
2.3. HTTP PATCH (Partial Update)
HTTP PATCH requests are to make partial update on a resource.
2.4. HTTP DELETE (Delete)
DELETE APIs are used to delete resources. A successful response of DELETE requests SHOULD be HTTP
response code 200 (OK) if the response includes an entity describing the status, 202 (Accepted) if the action has been
queued, or 204 (No Content) if the action has been performed but the response does not include an entity.
3. Redfish API
Resource API Notes
/redfish/v1
/redfish/v1/odata
/redfish/v1/$metadata
/redfish/v1/AccountService
/redfish/v1/AccountService/Accounts
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 7/54

GIGABYTE Proprietary & Confidential
/redfish/v1/AccountService/Accounts/{instance}
/redfish/v1/AccountService/Configurations
/redfish/v1/AccountService/ExternalAccountProviders/RADIUS
/redfish/v1/AccountService/ExternalAccountProviders/RADIUS/Oem/Ami/AdvancedRADIUSSetting
/redfish/v1/ AccountService/LDAP/Certificates
/redfish/v1/ AccountService/LDAP/Certificates/1
/redfish/v1/AccountService/LDAP/Certificates/Oem/Ami/ClientCertificates
/redfish/v1/ AccountService/LDAP/Certificates/Oem/Ami/ClientCertificates/1
/redfish/v1/AccountService/Roles
/redfish/v1/AccountService/Roles/{instance}
/redfish/v1/AccountService/PrivilegeMap
/redfish/v1/CertificateService
/redfish/v1/CertificateService/Actions/CertificateService.GenerateCSR
/redfish/v1/CertificateService/Actions/CertificateService.ReplaceCertificate
/redfish/v1/CertificateService/CertificateLocations
/redfish/v1/Chassis
/redfish/v1/Chassis/{instance}
/redfish/v1/Chassis/{instance}/Actions/Chassis.Reset
/redfish/v1/Chassis/{instance}/Power
/redfish/v1/Chassis/{instance}/LogServices
/redfish/v1/Chassis/{instance}/LogServices/Logs/Entries
/redfish/v1/Chassis/{instance}/LogServices/Logs/Entries/{instance}
/redfish/v1/Chassis/{instance}/LogServices/Logs
/redfish/v1/Chassis/{instance}/LogServices/Logs/Actions/LogService.ClearLog
/redfish/v1/Chassis/{instance}/NetworkAdapters
/redfish/v1/Chassis/{instance}/PCIeDevices
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 8/54

GIGABYTE Proprietary & Confidential
/redfish/v1/Chassis/{instance}/PCIeDevices/{instance}
/redfish/v1/Chassis/{instance}/PCIeDevices/{instance}/PCIeFunctions/{instance}
/redfish/v1/Chassis/{instance}/Sensors
/redfish/v1/Chassis/{instance}/Sensors/{instance}
/redfish/v1/Chassis/{instance}/Sensors/Energy
/redfish/v1/Chassis/{instance}/Sensors/Power
/redfish/v1/Chassis/{instance}/Thermal
/redfish/v1/Chassis/{instance}/Thermal/FanprofileService
/redfish/v1/Chassis/{instance}/Thermal/FanprofileService/Fanprofile
/redfish/v1/Chassis/{instance}/Thermal/FanprofileService/SupportPCIEDevice
/redfish/v1/Oem/Ami/Cconfigurations
/redfish/v1/CompositionService
/redfish/v1/CompositionService/ResourceBlocks
/redfish/v1/CompositionService/ResourceBlocks/{instance}
/redfish/v1/CompositionService/ResourceZones
/redfish/v1/CompositionService/ResourceZones/{ instance }
/redfish/v1/EventService
/redfish/v1/EventService/Actions/EventService.SubmitTestEvent
/redfish/v1/EventService/Subscriptions
/redfish/v1/EventService/Subscriptions/{instance}
/redfish/v1/EventService/SubmitTestEventActionInfo
/redfish/v1/JsonSchemas
/redfish/v1/JsonSchemas/{instance}
/redfish/v1/Managers
/redfish/v1/Managers/{instance}
/redfish/v1/Managers/{instance}/Actions/Oem/AMIManager.RedfishDBReset
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 9/54

GIGABYTE Proprietary & Confidential
/redfish/v1/Managers/{instance}/EthernetInterfaces
/redfish/v1/Managers/{instance}/EthernetInterfaces/{instance}
/redfish/v1/Managers/{instance}/HostInterfaces
/redfish/v1/Managers/{instance}/HostInterfaces/{instance}
/redfish/v1/Managers/{instance}/HostInterfaces/{instance}/HostEthernetInterfaces
/redfish/v1/Managers/{instance}/LogServices
/redfish/v1/Managers/{instance}/LogServices/{instance}
/redfish/v1/Managers/{instance}/LogServices/{instance}/Actions/LogServices.ClearLog
/redfish/v1/Managers/{instance}/LogServices/{instance}/Entries
/redfish/v1/Managers/{instance}/LogServices/{instance}/Entries/{instance}
/redfish/v1/Managers/{instance}/NetworkProtocol
/redfish/v1/Managers/{instance}/NetworkProtocol/HTTPS/Certificates
/redfish/v1/Managers/{instance}/NetworkProtocol/HTTPS/Certificates/{instance}
/redfish/v1/Managers/{instance}/Oem/RedfishDBResetActionInfo
/redfish/v1/Managers/{instance}/ResetActionInfo
/redfish/v1/Managers/{instance}/SerialInterfaces
/redfish/v1/Managers/{instance}/SerialInterfaces/{instance}
/redfish/v1/Managers/{instance}/VirtualMedia
/redfish/v1/Managers/{instance}/VirtualMedia/{instance}
/redfish/v1/Managers/{instance}/VirtualMedia/{instance}/Actions/VirtualMedia.InsertMedia
/redfish/v1/Managers/{instance}/VirtualMedia/{instanc}/Actions/VirtualMedia.EjectMedia
/redfish/v1/Managers/{instance}/Actions/Oem/AMIVirtualMedia.ConfigureCDInstance
/redfish/v1/Managers/{instance}/Actions/Oem/AMIVirtualMedia.EnableRMedia
/redfish/v1/Registries
/redfish/v1/Registries/{instance}
/redfish/v1/Registries/{instance.json}
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 10/54

GIGABYTE Proprietary & Confidential
/redfish/v1/SessionService
/redfish/v1/SessionService/Sessions
/redfish/v1/SessionService/Sessions/{instance}
/redfish/v1/Systems
/redfish/v1/Systems/Capabilities
/redfish/v1/Systems/{instance}
/redfish/v1/Systems/{instance}/Actions/ComputerSystem.Reset
/redfish/v1/Systems/{instance}/Bios
/redfish/v1/Systems/{instance}/Bios/Actions/Bios.ResetBios
/redfish/v1/Systems/{instance}/Bios/Actions/Bios.ChangePassword
/redfish/v1/Systems/{instance}/Bios/SD
/redfish/v1/Systems/{instance}/BootOoptions
/redfish/v1/Systems/{instance}/BootOoptions/{instance}
/redfish/v1/Systems/{instance}/EthernetInterfaces
/redfish/v1/Systems/{instance}/EthernetInterfaces/{instance}
/redfish/v1/Systems/{instance}/EthernetInterfaces/{instance}/VLANs
/redfish/v1/Systems/{instance}/EthernetInterfaces/{instance}/VLANs/{instance}
/redfish/v1/Systems/{instance}/LogServices
/redfish/v1/Systems/{instance}/LogServices/{instance}
/redfish/v1/Systems/{instance}/LogServices/{instance}/Actions/LogService.ClearLog
/redfish/v1/Systems/{instance}/LogServices/{instance}/Entries
/redfish/v1/Systems/{instance}/LogServices/{instance}/Entries/{instance}
/redfish/v1/Systems/{instance}/Memory
/redfish/v1/Systems/{instance}/Memory/{instance}
/redfish/v1/Systems/{instance}/MemoryDomains
/redfish/v1/Systems/{instance}/NetworkInterfaces
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 11/54

GIGABYTE Proprietary & Confidential
/redfish/v1/Systems/{instance}/NetworkInterfaces/{instance}
/redfish/v1/Systems/{instance}/Processors
/redfish/v1/Systems/{instance}/Processors/{instance}
/redfish/v1/Systems/{instance}/SimpleStorage
/redfish/v1/Systems/{instance}/SimpleStorage/{instance}
/redfish/v1/Systems/{instance}/Storage
/redfish/v1/Systems/{instance}/Storage /{instance}
/redfish/v1/TaskService
/redfish/v1/TaskService/Tasks
/redfish/v1/TaskService/Tasks/{instance}
/redfish/v1/TelemetryService
/redfish/v1/TelemetryService/Actions/ TelemetryService.SubmitTestMetricReport
/redfish/v1/TelemetryService/LogService
/redfish/v1/TelemetryService/LogService/Actions/LogService.ClearLog
/redfish/v1/TelemetryService/LogService/
/redfish/v1/TelemetryService/LogService/ /Actions/LogService.ClearLog
/redfish/v1/TelemetryService/LogService/ /Entries
/redfish/v1/TelemetryService/LogService/ /Entries/{instance}
/redfish/v1/TelemetryService/MetricDefinitions
/redfish/v1/TelemetryService/MetricDefinitions/{instance}
/redfish/v1/TelemetryService/MetricReportDefinitions
/redfish/v1/TelemetryService/MetricReportDefinitions/{instance}
/redfish/v1/TelemetryService/MetricReports
/redfish/v1/TelemetryService/MetricReports/{instance}
/redfish/v1/TelemetryService/Triggers
/redfish/v1/TelemetryService/Triggers/{instance}
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 12/54

GIGABYTE Proprietary & Confidential
/redfish/v1/UpdateService
/redfish/v1/ UpdateService/Actions/SimpleUpdate
/redfish/v1/UpdateService/FirmwareInventory
/redfish/v1/UpdateService/FirmwareInventory/{instance}
/redfish/v1/UpdateService/SimpleUpdateActionInfo
4. Common Field to all Schemas
- @odata.context
- @odata.id
- @odata.type
- @odata.etag
- Id
- Name
5. ServiceRoot
[GET] /redfish/v1
- Oem
- Ami
- Configurations
- RtpVersion
- Id
- Name
- Description
- RedfishVersion
- Systems
- Chassis
- Managers
- Tasks
- AccountService
- EventService
- SessionService
- Registries
- JsonSchemas
- UpdateService
- CompositionService
- TelemetryService
- Links
- Sessions
- JobService
- Product
- ProtocolFeaturesSupported
- ExcerptQuery
- ExpandQuery
- ExpandAll
- Levels
- Links
- MaxLevels
- NoLinks
- FilterQuery
- OnlyMemberQuery
- SelectQuery
- UUID
- Vendor
- CertificateService
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 13/54

GIGABYTE Proprietary & Confidential
- Oem
6. ODATA
[GET] /redfish/v1/odata
7. $metadata
[GET] /redfish/v1/$metadata
8. AccountService
[GET] /redfish/v1/AccountService
[PATCH] /redfish/v1/AccountService
- AccountLockoutCounterResetAfter
- AccountLockoutDuration
- AccountLockoutThreshold
- Accounts
- AuthFailureLoggingThreshold
- Description
- Id
- MaxPasswordLength
- MinPasswordLength
- Name
- Oem
- Ami
- Configuration
- Roles
- ServiceEnabled
- Status
- Health
- State
- PrivilegeMap
- ActiveDirectory
- Authentication
- AuthenticationType
- Username
- Password
- RemoteRoleMapping
- ServiceEnabled
- AccountLockoutCounterResetEnabled- AdditionalExternalAccountProviders
- LDAP
- Authentication
- AuthenticationType
- Username
- Password
- LDAPService
- SearchSettings
- GroupNameAttribute
- GroupsAttribute
- UsernameAttribute
- RemoteRoleMapping
- ServiceEnabled
8.1. Account Collection
[GET] /redfish/v1/AccountService/Accounts
[POST] /redfish/v1/AccountService/Accounts
- Description
- Members@odata.count
- Members
- Name- Oem
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 14/54

GIGABYTE Proprietary & Confidential
POST
Request:
POST https://{{ip}}/redfish/v1/AccountService/Accounts
Content-Type: application/json
Example POST Request Body:
{
"Name": "TestUser Account",
"Description": "Test User Account",
"Enabled": true,
"Password": "superuser",
"UserName": "user_account",
"RoleId": "Operator",
"Locked": false,
"PasswordChangeRequired": false
}
8.1.1. Accounts
[GET] /redfish/v1/AccountService/Accounts/{instance}
[PATCH] /redfish/v1/AccountService/Accounts/{instance}
[DELETE] /redfish/v1/AccountService/Accounts/{instance}
- Description
- Enabled
- Id
- Links
- Role
- Locked
- Name
- RoleId
- UserName
- Password
- PasswordChangeRequired
- Oem
- Actions
- Certificates
- AccountTypes
- SNMP
- AuthenticationProtocol
- EncryptionProtocol
8.2. PAM Configuration
[GET] /redfish/v1/AccountService/Configurations
[PATCH] /redfish/v1/AccountService/Configurations
- Id
- Name
- PAMEnabled
- PAMOrder
8.3. Radius Authentication
[GET] /redfish/v1/AccountService/ExternalAccountProviders/RADIUS
[PATCH] /redfish/v1/AccountService/ExternalAccountProviders/RADIUS
- ServicePort
- ServiceEnabled
- ExtendedPrivilege
- ServiceAddress
- Secret
- ExtendedPrivilege
- KVMAccess
- VMediaAccess
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 15/54

GIGABYTE Proprietary & Confidential
- AdvancedRADIUSSetting
- Timeout
- AccountProviderTypes
- Oem
8.3.1. AdvancedRADIUSSetting
[GET] /redfish/v1/AccountService/ExternalAccountProviders/RADIUS/Oem/Ami/AdvancedRADIUSSetting
[PATCH] /redfish/v1/AccountService/ExternalAccountProviders/RADIUS/Oem/Ami/AdvancedRADIUSSetting
- RADIUSAuthorization
8.4. Role Collection
[GET] /redfish/v1/AccountService/Roles
[POST] /redfish/v1/AccountService/Roles
- Description
- Members@odata.count
- Members
- Name
- Oem
POST
Request:
POST https://{{ip}}/redfish/v1/AccountService/Roles
Content-Type: application/json
Example POST Request Body:
{
"AssignedPrivileges": [
"ConfigureUsers",
"ConfigureManager",
"ConfigureSelf",
"Login",
"ConfigureComponents"
],
"Description": "TestRole User Role",
"Id": "TestRole",
"RoleId": "TestRole",
"Enabled": true,
"IsPredefined": true,
"Name": "TestRole Role",
"OemPrivileges": [
"OemPowerControl",
"OemClearLog"
]
}
8.4.1. Role
[GET] /redfish/v1/AccountService/Roles/{instance}
[PATCH] /redfish/v1/AccountService/Roles/{instance}
[DELETE] /redfish/v1/AccountService/Roles/{instance}
- AssignedPrivileges
- Description
- Id
- IsPredefined
- Name
- RoleId
- OemPrivileges
- Actions
- Oem
9. CertificateService
[GET] /redfish/v1/CertificateService
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 16/54

GIGABYTE Proprietary & Confidential
[POST] /redfish/v1/CertificateService/Actions/CertificateService.GenerateCSR
[POST] redfish/v1/CertificateService/Actions/ CertificateService.ReplaceCertificate
- Action
- Id
- Name
- Description
- CertificateLocations
- Oem
POST
Request:
POST https://{{ip}}/redfish/v1/CertificateService/Actions/CertificateService.GenerateCSR
Content-Type: application/json
Example POST Request Body:
{
"Country": "US",
"State": "Oregon",
"City": "Portland",
"Organization": "Contoso",
"OrganizationalUnit": " Service Processors",
"CommonName": "manager.contoso.org",
"AlternativeNames": [ "manager.contoso.com", "manager.contoso.us", "169.254.0.17" ],
"Email": "admin@contoso.org",
"KeyBitLength": 2048,
"KeyUsage": [ "DigitalSignature" ],
"ChallengePassword" : "challengepassword",
"GivenName" : "userGivenName",
"ContactPerson" : "AMI Manager",
"Initials" : "userInitials",
"Surname" : "userSurname",
"UnstructuredName" : "userUnstructuredName",
"CertificateCollection" : {"@odata.id" : "/redfish/v1/Managers/Self/NetworkProtocol/HTTPS/Certificates"}
}
Request:
POST https://{{ip}}/redfish/v1/CertificateService/Actions/CertificateService. ReplaceCertificate
Content-Type: application/json
Note : If use Certificate chain, the "CertificateType" must be "PEMchain"
Example POST Request Body:
{
"CertificateString": "-----BEGIN CERTIFICATE-----
\nMIIEOzCCAyOgAwIBAgIJAO8c/Hd0c/0GMA0GCSqGSIb3DQEBCwUAMIG7MQswCQYD\nVQQGEwJVU
zEQMA4GA1UECAwHR2VvcmdpYTERMA8GA1UEBwwITm9yY3Jvc3MxNDAy\nBgNVBAoMK0FtZXJpY2F
uIE1lZ2F0cmVuZHMgSW50ZXJuYXRpb25hbCBMTEMgKEFN\nSSkxGzAZBgNVBAsMElNlcnZpY2UgUHJvY
2Vzc29yczEUMBIGA1UEAwwLbWVnYXJh\nYy5jb20xHjAcBgkqhkiG9w0BCQEWD3N1cHBvcnRAYW1pLmN
vbTAeFw0xOTA4Mjcx\nMzAzMDBaFw0zNDA4MjMxMzAzMDBaMIG7MQswCQYDVQQGEwJVUzEQMA
4GA1UECAwH\nR2VvcmdpYTERMA8GA1UEBwwITm9yY3Jvc3MxNDAyBgNVBAoMK0FtZXJpY2FuIE1l\nZ
2F0cmVuZHMgSW50ZXJuYXRpb25hbCBMTEMgKEFNSSkxGzAZBgNVBAsMElNlcnZp\nY2UgUHJvY2Vzc2
9yczEUMBIGA1UEAwwLbWVnYXJhYy5jb20xHjAcBgkqhkiG9w0B\nCQEWD3N1cHBvcnRAYW1pLmNvbTC
CASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoC\nggEBAPjhY7RBU5kLGB3yHZfiEk9Zm9vJhe/1mRZlW
TT77g8iy5eo2L9BiIsctpTm\n2clMGBRwFgCjOyZqkldU2Mu2zeALS31Bkvx12/OOloG/MkvVxc09MrNWwEU0
Q2Az\njGu7X+bEKSAQAYzFZIWSYf4hnadEtzh53rkdk9mKYp101YfnAqZ+zg9MxXuzl8TM\nEGh7iemTtwozs
LTHlwIiH6cIKNm7TmsL7ILifEQUP4wBTJBf1nmVe80fdNoDC+FB\nvXwSuvHI5wIt4Nd2hthI6Ll6GRJrKGF
E7FsqxVzBVb2anp8U44VDV69guPo47XlS\n2yYXHPNwZmw9zm7mD5TCRJLKT20CAwEAAaNAMD4wCQ
YDVR0TBAIwADALBgNVHQ8E\nBAMCBeAwJAYDVR0RBB0wG4ILbWVnYXJhYy5jb22CDDE2OS4yNTQu
MC4xNzANBgkq\nhkiG9w0BAQsFAAOCAQEAZi3ILVGGyVR6LJ+Au7gY5w9T+k+CpXgzorF+yRcSJo/h\n/kfS
MPPgH6yY+5ja4Z9kQ57nTfnaBqmHnEhwhAQrPVAPd3iKYEHNHO4u0gB4ZnkA\nyeLA4vM3KG5510Iry8o
BhYuvwZwE3YhtYNNocZd1ct5A8zJmpeuS4ffPwWFGZGmV\nfiDSGa4NdzLr1auPt5FUgbsm5V0FNPNhYNRP
YvHRMYh+orv727sJrxocr4BJ3ncq\nUGNdPvVow5QQrmm0WsSjv285F3BiIeE1b6iSDksiiZ4lYLcr8twBeTq5gjc9
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 17/54

GIGABYTE Proprietary & Confidential
1qVh\nY7Ms4UrZYTJhYxq0oVGplADOn+LL9qEZ9MXAR6SkeQ==\n-----END CERTIFICATE-----\n-----
BEGIN RSA PRIVATE KEY-----
\nMIIEowIBAAKCAQEA+OFjtEFTmQsYHfIdl+IST1mb28mF7/WZFmVZNPvuDyLLl6jY\nv0GIixy2lObZyUw
YFHAWAKM7JmqSV1TYy7bN4AtLfUGS/HXb846Wgb8yS9XFzT0y\ns1bARTRDYDOMa7tf5sQpIBABjMVkh
ZJh/iGdp0S3OHneuR2T2YpinXTVh+cCpn7O\nD0zFe7OXxMwQaHuJ6ZO3CjOwtMeXAiIfpwgo2btOawvsguJ8
RBQ/jAFMkF/WeZV7\nzR902gML4UG9fBK68cjnAi3g13aG2EjouXoZEmsoYUTsWyrFXMFVvZqenxTjhUNX\n
r2C4+jjteVLbJhcc83BmbD3ObuYPlMJEkspPbQIDAQABAoIBACTpiNgbOELimlkW\np7z3ErAiIjOe1/aW/nWL
4ocxNkWYa4m6ySrUlWPMhmffNT3dw1SEqz689vDjrYC2\nXNEZ877e7ftN1ncLI+wjob7slJEay5N9GB/xJeMdt
UB3ZMQ1riuTvGW8+f3e6OHG\nrDH82l0MnAAMUzQxZtRE6gtgYKsfFSyxgMc+X4i1hZUszA1IKa2uXk+6X
mEEtuCu\noadu5KmHM0Oxh5ph4JCb1HgSxrRVjunsd+x1zNPFcJchjz4V5CRQ6gDPl/EzmrF1\nTtdnsW8gFzh6
v6faHe11bCDrXIG3wDlqOwPHm7Vk0TqToMgEceEu+DcLcnEun2iK\nrWD13SECgYEA/xyzJOenwIEVuxHizb
8H7ZwgYV5k1jj0ygzRFEGf+vrDi8ao9HR+\nbSKmqG1oZi0Dorat1wQb3Lj5ggoYRiYP1SPGqdFDaDgdn9jcuVF
QpQ+5jsLB8V03\noAUmSEB9Yk3eGZ1XAZro+FzGb5BsZyaG0QlLnCcQx/GcJZ+G75lgJt8CgYEA+b8j\nKu0Xr
BaBrGCs988OSpuebEQgO7zZH9TvN+ea2ZR9N7cDOXsSpsTQsjJsQ4pwIhOD\ng0Jv3CTFKCqK2inXA3SJ+Uz
lmvIPDg31+Y3qbpA+ZBYjG8rp7v4uSjbBBFkbxJuV\n1S8oVQbIfljdTfnypK5+TPTNig4C5IBzAuqUjzMCgYB0
+VHjIB05FXdDWYYnVOpr\ntuTaAJA38dG8O3g604RpbkXvd13NCQVXQUYtgE0YXJeIKj83kfi8kkxFph9POv
CT\niF31S7CevuxGeQdsKa7SoI0yunZ3F4kD5JiTFI7pXk7ya8STRdaA2vlZ+lzaRz4V\n5y82IGt/Ynd4gNc8UZV
W/QKBgQCKdeubauMK51dxKA/9O3Ai8O/9+i8cr3B482bE\nycTSCD772p0RCyimCMvjX40iTOgqHEN3TCg
UFtavlBZzKWspYTz1WCqbosOx+Q98\nEa/9KD9O4e8JA5B6jbVAM+cC8Bwy/kctb/2eVipl0gKvrnlVz9/57mbdu
TLlWElr\nPn6qfQKBgEqL9ShURu6pytGIfF6CVPT1DiXXvzAvj8KWwdWpwob3BFl+82T9jNgt\nVv441iirH4iz
d7IzPNv56vb3F4D2lY4zAfWhfrMytrv8aKghDyyZq5Qo6mXmz5hq\nd071CuwqgoRn6UG5gZWs+B/Oh16xPYk
wZmZOYEZaoE7ubEtzB7qW\n-----END RSA PRIVATE KEY-----",
"CertificateType": "PEM",
"CertificateUri" : {"@odata.id":"/redfish/v1/Managers/Self/NetworkProtocol/HTTPS/Certificates/1"}
}
9.1. CertificateLocations
[GET] /redfish/v1/CertificateService/CertificateLocations
- Id
- Name
- Description
- Links
- Certificates
- Action
- Oem
9.1.1. Certificate
[GET] /redfish/v1/Managers/{instance}/NetworkProtocol/HTTPS/Certificates/{instance}
[GET] /redfish/v1/ AccountService/LDAP/Certificates/1
[GET] /redfish/v1/ AccountService/LDAP/Certificates/Oem/Ami/ClientCertificates/1
[POST] /redfish/v1/ AccountService/LDAP/Certificates
[POST] /redfish/v1/ AccountService/LDAP/Certificates/Oem/Ami/ClientCertificates
[DELETE] /redfish/v1/ AccountService/LDAP/Certificates/1
[DELETE] /redfish/v1/ AccountService/LDAP/Certificates/Oem/Ami/ClientCertificates/1
POST
Request:
POST https://{{ip}}/redfish/v1/AccountService/LDAP/Certificates
POST https://{{ip}}/redfish/v1/AccountService/LDAP/Certificates/Oem/Ami/ClientCertificates
Content-Type: application/json
Example POST Request Body:
{
"CertificateString": "------BEGIN CERTIFICATE-----
\nMIIC2DCCAoICCQDrKFHkCkpC2zANBgkqhkiG9w0BAQsFADCB8jELMAkGA1UEBhMC\nVVMxDzAN
BgNVBAgMBk9yZWdvbjERMA8GA1UEBwwIUG9ydGxhbmQxEDAOBgNVBAoM\nB0NvbnRvc28xDDAKBg
NVBAsMA0FCQzEcMBoGA1UEAwwTbWFuYWdlci5jb250b3Nv\nLm9yZzEgMB4GCSqGSIb3DQEJARYRYW
RtaW5AY29udG9zby5vcmcxGjAYBgNVBCkM\nEXRlc3RDb250YWN0UGVyc29uMRYwFAYDVQQqDA10ZX
N0R2l2ZW5OYW1lMRUwEwYD\nVQQrDAx0ZXN0SW5pdGlhbHMxFDASBgNVBAQMC3Rlc3RTdXJuYW1
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 18/54

GIGABYTE Proprietary & Confidential
lMB4XDTE5MTIx\nOTAyNTg0NVoXDTIwMDExODAyNTg0NVowgfIxCzAJBgNVBAYTAlVTMQ8wDQYD
VQQI\nDAZPcmVnb24xETAPBgNVBAcMCFBvcnRsYW5kMRAwDgYDVQQKDAdDb250b3NvMQww\nCgY
DVQQLDANBQkMxHDAaBgNVBAMME21hbmFnZXIuY29udG9zby5vcmcxIDAeBgkq\nhkiG9w0BCQEWE
WFkbWluQGNvbnRvc28ub3JnMRowGAYDVQQpDBF0ZXN0Q29udGFj\ndFBlcnNvbjEWMBQGA1UEKgwN
dGVzdEdpdmVuTmFtZTEVMBMGA1UEKwwMdGVzdElu\naXRpYWxzMRQwEgYDVQQEDAt0ZXN0U3Vy
bmFtZTBcMA0GCSqGSIb3DQEBAQUAA0sA\nMEgCQQC2vTAZtvPrByReb065z6E/n7Rv8ymt4Goowjet6s0kf
m/WnJumTt0/eJfk\n2j5c+XSg6q1wgmZOZA+NZVL7DFUjAgMBAAEwDQYJKoZIhvcNAQELBQADQQCsYyR
Y\n3RX7fsLQr0M/LgHCHF9ke9mF8KsockAQlZLkXuwSZHe6+0b7p6OeWrdiuil6cpmO\nb32QIGFrKWq8JXD
+\n-----END CERTIFICATE-----\n-----BEGIN PRIVATE KEY-----
\nMIIBVgIBADANBgkqhkiG9w0BAQEFAASCAUAwggE8AgEAAkEAtr0wGbbz6wckXm9O\nuc+hP5+0b/Mpre
BqKMI3rerNJH5v1pybpk7dP3iX5No+XPl0oOqtcIJmTmQPjWVS\n+wxVIwIDAQABAkEAn6j0WcNLolF/KTM/
KYGLdTdoQ1fFVrH4jtwCIeZAjlygCliT\nKcb1AOsO/jxKFaK/ZUUVk5lWomxnZBy641r+AQIhANpX0+K7kUU
m4L7x1VgFfRUh\nal8ns1MneAkbL0z0j+NjAiEA1kFjSAJIki1fkakXtixdiZz9GdRbgLBFM4cZJXtT\n00ECIQCN
kCIdwBTI7BMNWghD4JMfryGjfj8DK/Tkmo6Ja4sbFwIhAKF1FwcNyXh2\nvt06qsa6uiZY6pbLY8UfkJabCUUo
oevBAiAzw38GApvYqlQeSRQcHTMx/LN6a6NY\nJlxeaUXwCcsIuw==\n-----END PRIVATE KEY-----\n",
"CertificateType": "PEM"
}
9.1.1.1. Rekey
[POST] /redfish/v1/AaccountService/Accounts/{instance}/Certificates/{instance}/Actions/Certificate.Rekey
POST
Request:
POST https://{{ip}}/redfish/v1/AaccountService/Accounts/{instance}/Certificates/{instance}/Actions/Certificate.Rekey
Content-Type: application/json
Example POST Request Body:
{
"KeyBitLength": 512,
"ChallengePassword" : "challengepassword"
}
9.1.1.2. Renew
[POST] redfish/v1/AaccountService/Accounts/{instance}/Certificates/{instance}/Actions/Certificate.Renew
- Oem
- Actions
- Id
- Name
- Description
- Issuer
- KeyUsage
- Subject
- ValidNotAfter
- ValidNotBefore
- CertificateString
- CertificateType
POST
Request:
POST https://{{ip}}/redfish/v1/AaccountService/Accounts/{instance}/Certificates/{instance}/Actions/Certificate.Renew
Content-Type: application/json
Example POST Request Body:
{
"ChallengePassword" : "challengepassword"
}
10. Chassis Collection
[GET] /redfish/v1/Chassis
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 19/54

GIGABYTE Proprietary & Confidential
- Description
- Name
- Members@odata.count
- Members
- Oem
10.1. Chassis
[GET] /redfish/v1/Chassis/{instance}
[PATCH] /redfish/v1/Chassis/{instance}
[POST] /redfish/v1/Chassis/{instance}/Actions/Chassis.Reset
- Id
- Name
- Description
- ChassisType
- Manufacturer
- Model
- SKU
- Sensors
- SerialNumber
- PartNumber
- PCIeDevices
- AssetTag
- IndicatorLED
- Links
- ComputerSystems
- ComputerSystems@odata.count
- ManagedBy
- ManagedBy@odata.count
- Drives
- Drives @odata.count
- Storage
- Storage@odata.count
- ResourceBlocks
- ResourceBlocks @odata.count
- ContainedBy
- Contains
- Contains @odata.count
- PowerBy
- PowerBy @odata.count
- CooledBy
- CooledBy @odata.count
- ManagersInChassis
- ManagersInChassis @odata.count
- Processors
- Processors @odata.count
- Actions
- Status
- LogServices
- Thermal
- Power
- PowerState
- NetworkAdapters
- Assembly
- Oem
- UUID
- Location
- HeightMm
- WidthMm
- DepthMm
- WeightKg
- MediaControllers
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 20/54

GIGABYTE Proprietary & Confidential
- EnvironmentalClass
POST
Request:
POST https://{{ip}}/redfish/v1/Chassis/Self/Actions/Chassis.Reset
Content-Type: application/json
Request Body:
The ResetType can be one of the following values: "On", "ForceOff", "GracefulShutdown", "ForceRestart".
Example POST Request Body:
{
"ResetType" : "On"
}
10.1.1. Power
[GET] /redfish/v1/Chassis/{instance} /Power
[PATCH] /redfish/v1/Chassis/{instance}/Power
- Description
- Id
- Name
- PowerControl
- Name
- MemberId
- PowerMetrics
- IntervalInMin
- MinConsumedWatts
- MaxConsumedWatts
- AverageConsumedWatts
- RelatedItem@odata.count
- PhysicalContext
- PowerConsumedWatts
- PowerRequestedWatts
- PowerAvailableWatts
- PowerCapacityWatts
- PowerAllocatedWatts
- PowerLimit
- LimitInWatts
- LimitException
- CorrectionInMs
- PowerControl@odata.count
- Voltage
- MemberId
- Name
- SensorNumber
- Status
- ReadingVolts
- UpperThresholdNonCritical
- UpperThresholdCritical
- LowerThresholdNonCritical
- LowerThresholdCritical
- MinReadingRange
- MaxReadingRange
- RelatedItem
- OwnerLUN
- UpperThresholdFatal
- LowerThresholdFatal
- PhysicalContext
- RelatedItem (RelatedItem@odata.count)
- Voltages@odata.count
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 21/54

GIGABYTE Proprietary & Confidential
- PowerSupply
- MemberId
- Name
- LineInputVoltage
- PowerCapacityWatts
- LastPowerOutputWatts
- Model
- FirmwareVersion
- SerialNumber
- PowerInputWatt
- PowerOutputWatts
- PowerSupplyType
- LineInputVoltageType
- PartNumber
- SparePartNumber
- Status
- Location
- EfficiencyPercent
- HotPluggable
- RelatedItem
- Redundancy
- Oem
10.1.2. LogServices (Support services after version 12.41.07)
[GET] /redfish/v1/Chassis/{instance}/LogServices
- Description
- Members
- Members@odata.count
- Name
- Oem
10.1.2.1. Log Service
[GET] /redfish/v1/Chassis/{instance}/LogServices/Logs
[PATCH] /redfish/v1/Chassis/{instance}/LogServices/Logs
[POST] /redfish/v1/Chassis/{instance}/LogServices/Log/Actions/LogServices.ClearLog
- Id
- Name
- Description
- ServiceEnabled
- MaxNumberOfRecords
- OverWritePolicy
- DateTime
- DateTimeLocalOffset
- Actions
- Status
- Entries
- LogEntry Type
- Oem
POST
Request:
POST https://{{ip}}/redfish/v1/Chassis/Self/LogServices/SEL/Actions/LogServices.ClearLog
Content-Type: application/json
Example POST Request Body:
{
}
10.1.2.1.1. Entry Collection
[GET] /redfish/v1/Chassis/{instance}/LogServices/Log/Entries
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 22/54

GIGABYTE Proprietary & Confidential
- Description
- Members
- Members@odata.count
- Name
- Oem
10.1.2.1.1.1. Entry
[GET] /redfish/v1/Chassis/{instance}/LogServices/Log/Entries/{instance}
- Id
- Name
- Description
- Severity
- Created
- EventTimestamp
- EntryType
- EntryCode
- SensorType
- SensorNumber
- Message
- MessageId
- Links
- OriginOfConfition
- Oem
- EventId
- MessageArgs
- OemLogEntryCode
- OemSensorType
10.1.3. Sensor Collection
[GET] /redfish/v1/Chassis/{instance}/Sensors
- Description
- Members
- Members@odata.count
- Name
- Oem
10.1.3.1. Sensor
[GET] /redfish/v1/Chassis/{instance}/Sensors/{instance}
- PeakReading
- PeakReadingTime
- Reading
- ReadingType
- Oem
- Accuracy
- AdjustedMaxAllowableOperatingValue
- AdjustedMinAllowableOperatingValue
- ApparentVA
- ElectricalContext
- LoadPercent
- Location
- MaxAllowableOperatingValue
- MinAllowableOperatingValue
- PhysicalContext
- PhysicalSubContext
- PowerFactor
- Precision
- ReactiveVAR
- ReadingRangeMax
- ReadingRangeMin
- ReadingUnits
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 23/54

GIGABYTE Proprietary & Confidential
- SensingFrequency
- SensorResetTime
- Status
- Thresholds
- VoltageType
10.1.3.2. Sensor Energy
[GET] /redfish/v1/Chassis/{instance}/Sensors/Energy
- Id
- Name
- Oem
- Reading
- ReadingType
- PeakReading
- PeakReadingTime
10.1.3.3. Sensor Power
[GET] /redfish/v1/Chassis/{instance}/Sensors/Power
- Id
- Name
- PeakReading
- PeakReadingTime
- Reading
- ReadingType
10.1.4. Thermal
[GET] /redfish/v1/Chassis/{instance} /Thermal
- Description
- Id
- Name
- Temperatures
- Name
- MemberId
- SensorNumber
- Status
- ReadingCelsius
- UpperThresholdNonCritical
- UpperThresholdCritical
- LowerThresholdNonCritical
- LowerThresholdCritical
- PhysicalContext
- OwnerLUN
- UpperThresholdFatal
- LowerThresholdFatal
- MinReadingRangeTemp
- MaxReadingRangeTemp
- RelatedItem
- DeltaReadingCelsius
- DeltaPhysicalContext
- MaxAllowableOperatingValue
- MinAllowableOperatingValue
- AdjustedMaxAllowableOperatingValue
- AdjustedMinAllowableOperatingValue
- Fan
- MemberId
- Name
- PhysicalContext
- Status
- Reading
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 24/54

GIGABYTE Proprietary & Confidential
- LowerThresholdNonCritical
- LowerThresholdCritical
- MinReadingRange
- MaxReadingRange
- RelatedItem (RelatedItem@odata.count)
- OwnerLUN
- UpperThresholdNonCritical
- UpperThresholdCritical
- UpperThresholdFatal
- LowerThresholdFatal
- Redundancy
- HotPluggable
- Location
- SensorNumebr
- Oem
- Redundancy
- Actions
10.1.4.1. FanprofileService (GBT)
[GET] /redfish/v1/Chassis/{instance}/Thermal/FanprofileService
- Fanprofile
- Id
- Name
- SupportPCIEDevice
10.1.4.1.1. Fanprofile
[GET] /redfish/v1/Chassis/{instance}/Thermal/FanprofileService/Fanprofile
[PUT] /redfish/v1/Chassis/{instance}/Thermal/FanprofileService/Fanprofile
- Id
- Name
- arrProfile
-arrPolicy
- arrDuty
- arrFanSensor
- arrHexDeviceID
- arrHexVendorID
- arrRef
- arrSensor
- iAmbientSensor
- iAmbientSensorTemp
- iCpuTdp
- iInSDR
- iInitDuty
- iPCIEDeviceEnable
- iPolicyType
- iSensorCode
- strName
- strVersion
- strMode
- strVersion
10.1.4.1.2. SupportPCIEDevice
[GET] /redfish/v1/Chassis/{instance}/Thermal/FanprofileService/SupportPCIEDevice
[PUT] /redfish/v1/Chassis/{instance}/Thermal/FanprofileService/SupportPCIEDevice
- Id
- Name
- arrPCIEDevices
- hexDeviceID
- hexVendorID
- strName
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 25/54

GIGABYTE Proprietary & Confidential
- strVersion
10.1.5. NetworkAdapterCollection
[GET] /redfish/v1/Chassis/{instance}/NetworkAdapters
- Description
- Members
- Members@odata.count
- Name
- Oem
10.1.5.1. NetworkAdapter
[GET] /redfish/v1/Chassis/{instance}/NetworkAdapters/{instance}
- Id
- Name
- Controllers
- NetworkDeviceFunctions
- Ports
- Status
10.1.6. PCIeDevice Collection
[GET] /redfish/v1/Chassis/{instance}/PCIeDevices
- Members
- Members@odata.count
- Name
- Description
- Oem
10.1.6.1. PCIeDecice
[GET] /redfish/v1/Chassis/{instance}/PCIeDevices/{instance}
- Id
- Name
- Description
- Status
- Manufacturer
- Model
- SKU
- SerialNumber
- PartNumber
- AssetTag
- FirmwareVersion
- Links
- PCIeFunctions
- PCIeInterface
- Oem
- DeviceType
- Assembly
10.1.6.1.1. PCIeFunction
[GET] /redfish/v1/Chassis/{instance}/PCIeDevices/{instance}/PCIeFunctions/{instance}
- Id
- Name
- Description
- Status
- DeviceClass
- VendorId
- ClassCode
- Link
- FunctionId
- FunctionType
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 26/54

GIGABYTE Proprietary & Confidential
- DeviceId
- RevisionId
- SubsystemId
- SubsystemVendorId
- Actions
11. CompositionService
[Get] /redfish/v1/CompositionService
[Patch] /redfish/v1/CompositionService
- Description
- Id
- Name
- ResourceBlocks
- ResourceZones
- ServiceEnabled
- Status
- Oem
11.1. ResourceBlocks Collection
[Get] /redfish/v1/CompositionService/ResourceBlocks
- Description
- Members
- Members@odata.count
- Name
- Oem
11.1.1. ResourceBlocks
[Get] /redfish/v1/CompositionService/ResourceBlocks/{instance}
[Patch] /redfish/v1/CompositionService/ResourceBlocks/{instance}
- Id
- Name
- Description
- Status
- CompositionStatus
- Reserved
- MaxCompositions
- CompositionState- ResourceBlockType
- Processors
- Memory
- Oem
- Link
- Chassis
- Storage
- SimpleStorage
- Drivers
- EthernetInterfaces
11.2. ResourceZones Collection
[Get] /redfish/v1/CompositionService/ResourceBlocks
- Description
- Members
- Members@odata.count
- Name
11.2.1. ResourceZones
[Get] /redfish/v1/CompositionService/ResourceBlocks/{instance}
- Id
- Name
- Description
- Links
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 27/54

GIGABYTE Proprietary & Confidential
- Oem
- ResourceBlocks
- Status
12. AMI OEM Entities - Configuration
[Get] /redfish/v1/Oem/Ami/Configuration
- Id
- Name
- CertificateAuthorityUrl
- Oem
13. EventService
[GET] /redfish/v1/EventService
[PATCH] /redfish/v1/EventService
[POST] /redfish/v1/EventService/Actions/EventService.SubmitTestEvent
- Actions
- DeliveryRetryAttempts
- DeliveryRetryIntervalSeconds
- Description
- EventFormatTypes
- Id
- Name
- ServiceEnabled
- Status
- Subscriptions
- ServerSentEventUri
- SSEFilterPropertiesSupported
- Oem
- RegistryPrefixes
- ResourceTypes
- SubordinateResourcesSupported
- SMTP
- Authentication
- ConnectionProtocol
- Password
- Port
- ServiceEnabled
POST
Request:
POST https://{{ip}}/redfish/v1/EventService/Actions/EventService.SubmitTestEvent
Content-Type: application/json
EventServie.SubmitTestEvent can test using below RegistryPrefiexes MessageId
 Base1.5.0
 EventLog.1.0.0
 HttpStatus.1.0.0
 IPMI.1.0.0
 Security.1.0.0
 SyncAgent.1.0.0
https://{{ip}}/redfish/v1/Registries/{{Registry_instance.json}}
Eg: https://{{ip}}/redfish/v1/Registries/Base.1.5.0.json
Example: Base.1.5.0 [ PropertyValueNotInList as MessageId ]
Example POST Request Body:
{
"EventTimestamp":"2019-09-20T23:04:09+02:00",
"EventId":"1531584914",
"OriginOfCondition":"/redfish/v1/Chassis/Self",
"MessageId":"PropertyValueNotInList",
"MessageArgs":["Lit","IndicatorLED"],
"Severity":"Warning"
}
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 28/54

GIGABYTE Proprietary & Confidential
13.1. Subscription Collection
[GET] /redfish/v1/EventService/Subscriptions
[POST] /redfish/v1/EventService/Subscriptions
- Description
- Members
- Members@odata.count
- Name
- Oem
POST
Request:
POST https://{{ip}}/redfish/v1/EventService/Subscriptions
Content-Type: application/json
Example POST Request Body:
{
"Context": "Rocket All",
"Destination": "http://10.1.112.223:7628/",
"EventFormatType": "Event",
"Protocol": "Redfish",
"RegistryPrefixes":["SyncAgent.1.0.0","Base.1.5.0","EventLog.1.0.0"],
"ResourceTypes":["Chassis","Systems","EventService"]
}
Empty or Absent RegistryPrefixes, ResourceTypes and Absent EventFormatType:
RegistryPrefixes, ResourceTypes values are absent or empty are accepted in POST call. In this case service
shall sent events with any ResourceTypes or any RegistryPrefixes.
If EventFormatType property was absent on POST call then default value will be Event.
Example POST Request Body:
{
"Context": "Rocket All",
"Destination": "http://10.1.112.223:7628/",
"Protocol": "Redfish",
"RegistryPrefixes":[],
"ResourceTypes":[]
}
13.1.1. Subscription
[GET] /redfish/v1/EventService/Subscriptions/{instance}
[PATCH] /redfish/v1/EventService/Subscriptions/{instance}
[DELETE] /redfish/v1/EventService/Subscriptions/{instance}
- Id
- Name
- Description
- EventTypes
- Context
- SubscriptionType
- Protocol
- MessageIds
- OriginResources
- OriginResources@odata.count
- Status
- DeliveryRetryPolicy
- Oem
- Destination
- Actions
- SubordinateResources
- EventFormarType
- RegistryPrefixes
- ResourceTypes
- MetricReportDefinitions
- DeliveryRetryPolicy
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 29/54

GIGABYTE Proprietary & Confidential
13.1.2. Subscription Test Event
[GET] /redfish/v1/EventService/Subscriptions/SubmitTestEventActionInfo
- Description
- Id
- Name
- Parameters
- Oem
14. JsonSchemas Collection
[Get] /redfish/v1/JsonSchemas
- Description
- Members
- Members@odata.count
- Name
- Oem
14.1. JsonSchemas
[Get] /redfish/v1/ JsonSchemas/{instance}
- Oem
- Id
- Name
- Description
- Languages
- Schema
- Location
- Actions
15. Manager Collection
[GET] /redfish/v1/Managers
- Description
- Members
- Members@odata.count
- Name
15.1. Manager
[GET] /redfish/v1/Managers/{instance}
[PATCH] /redfish/v1/Managers/{instance}
[POST] /redfish/v1/Managers/{instance}/Actions/Manager.Reset
[POST] /redfish/v1/Managers/{instance}/Actions/Oem/AMIManager.RedfishDBReset
- Id
- Name
- Description
- ManagerType
- Links
- ManagerForServers
- ManagerForServers@odata.count
- ManagerForChassis
- ManagerForChassis@odata.count
- ManagerInChassis- ServiceEntryPointUUID
- UUID
- Model
- DateTime
- DateTimeLocalOffset
- FirmwareVersion
- SerialConsole
- CommandShell
- GraphicalConsole
- Actions
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 30/54

GIGABYTE Proprietary & Confidential
- Status
- EthernetInterfaces
- SerialInterfaces
- NetworkProtocol
- LogServices
- HostInterfaces
- PowerState
-
-
- Redundancy@odata.count
- Oem
- VirtualMedia
- ManagerServiceInfo
- CommandShellServiceInfo
- Links
- NetworkProtocol
- VirtualMedia
- AutoDSTEnabled
POST
Request:
POST https://{{ip}}/redfish/v1/Managers/Self/Actions/Manager.Reset
Content-Type: application/json
Request Body:
The ResetType can be one of the following values: "On", "ForceOff", "GracefulShutdown", "ForceRestart".
Example POST Request Body:
{
"ResetType" : "On"
}
{
"ResetType" : "On"
}
Request:
Request:
POST https://{{ip}}/redfish/v1/ Managers/Self/Actions/Oem/AMIManager.RedfishDBReset
Content-Type: application/json
Example POST Request Body:
{
"RedfishDBResetType": "ResetAll"
}
15.1.1. EthernetInterfaces Collection
[Get] /redfish/v1/Managers/{instance}/EthernetInterfaces
- Description
- Members
- Members@odata.count
- Name
- Oem
15.1.1.1. EthernetInterfaces
[Get] /redfish/v1/Managers/{instance}/EthernetInterfaces/bond0
[PATCH] /redfish/v1/Managers/{instance}/EthernetInterfaces/{{manager_ethifc_instance}}
- Id
- Name
- Description
- Status
- InterfaceEnabled
- PermanentMACAddress
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 31/54

GIGABYTE Proprietary & Confidential
- MACAddress
- SpeedMbps
- AutoNeg
- FullDuplex
- MTUSize
- HostName
- FQDN
- MaxIPv6StaticAddresses
- VLAN
- Ipv4Addresses
- Ipv6Addresses
- IPv6DefaultGateway
- NameServers
- LinkStatus
- DHCPv4
- Oem
- UefiDevicePath
- StatelessAddressAutoConfig
- Ipv6StaticAddresses
- VLANs
- Actions
- DHCPv6
- IPv6StaticDefaultGateways
- IPv4StaticAddresses
[GET] /redfish/v1/Managers/Self/EthernetInterfaces/eth0
- Id
- Name
- Description
- InterfaceEnabled
- PermanentMACAddress
- MACAddress
- LinkStatus
- Oem
- UefiDevicePath
- Status
- SpeedMbps
- StatelessAddressAutoConfig
- AutoNeg
- FullDuplex
- MTUSize
- HostName
- FQDN
- MaxIPv6StaticAddresses
- VLAN
- Ipv4Addresses
- Ipv6Addresses
- Ipv6DefaultGateway
- NameServers
- StaticNameServers
- VLANs
- Actions
- DHCPv4
- DHCPv6
- IPv6StaticDefaultGateways
- IPv4StaticAddresses
- IPv6AddressPolicyTable
[GET] /redfish/v1/Managers/Self/EthernetInterfaces/eth1
- Id
- Name
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 32/54

GIGABYTE Proprietary & Confidential
- Description
- InterfaceEnabled
- PermanentMACAddress
- MACAddress
- LinkStatus
- Oem
- UefiDevicePath
- Status
- SpeedMbps
- StatelessAddressAutoConfig
- AutoNeg
- FullDuplex
- MTUSize
- HostName
- FQDN
- MaxIPv6StaticAddresses
- VLAN
- Ipv4Addresses
- Ipv6Addresses
- Ipv6StaticAddresses
- Ipv6DefaultGateway
- NameServers
- VLANs
- Actions
- DHCPv4
- DHCPv6
- IPv6StaticDefaultGateways
- IPv4StaticAddresses
[GET] /redfish/v1/Managers/Self/EthernetInterfaces/usb0
- Id
- Name
- Description
- Status
- InterfaceEnabled
- PermanentMACAddress
- MACAddress
- Ipv4Addresses
- Ipv6Addresses
- LinkStatus
- Oem
- UefiDevicePath
- SpeedMbps
- StatelessAddressAutoConfig
- AutoNeg
- FullDuplex
- MTUSize
- HostName
- FQDN
- MaxIPv6StaticAddresses
- VLAN
- Ipv6StaticAddresses
- Ipv6DefaultGateway
- NameServers
- VLANs
- Actions
- DHCPv4
- DHCPv6
- IPv6StaticDefaultGateways
- IPv4StaticAddresses
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 33/54

GIGABYTE Proprietary & Confidential
15.1.2. CertificateCollection
[Get] /redfish/v1/Managers/{instance}/NetworkProtocol/HTTPS/Certificates
- Description
- Members
- Members@odata.count
- Name
- Oem
15.1.3. Factory Reset ActionInfo
[GET] /redfish/v1/Managers/{instance}/Oem/RedfishDBResetActionInfo
- Description
- Id
- Name
- Parameters
15.1.4. HostInterfaces Collection
[Get] /redfish/v1/Managers/{instance}/HostInterfaces
- Description
- Members
- Members@odata.count
- Name
- Oem
15.1.4.1. HostInterfaces
[Get] /redfish/v1/Managers/{instance}/HostInterfaces/{instance}
[PATCH] /redfish/v1/Managers/{instance}/HostInterfaces/{instance}
- Id
- Name
- Description
- HostInterfaceType
- Status
- InterfaceEnabled
- ExternallyAccessible
- AuthenticationModes
- KernelAuthRoleId
- KernelAuthEnabled
- FirmwareAuthRoleId
- FirmwareAuthEnabled
- Links
- ComputerSystems@odata.count
- ComputerSystems
- CredentialBootstrappingRole
- KernelAuthRole
- FirmwareAuthRole
- HostEthernetInterfaces
- ManagerEthernetInterface
- NetworkProtocol
- Oem
- AuthNoneRoleId
- CredentialBootstrapping
- Enabled
- EnableAfterReset
- RoleId
15.1.4.2. HostEthernetInterface Collection
[GET] /redfish/v1/Managers/Self/HostInterfaces/Self/HostEthernetInterfaces
- Description
- Members
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 34/54

GIGABYTE Proprietary & Confidential
- Members@odata.count
- Name
- Oem
15.1.5. LogServices Collection
[GET] /redfish/v1/Managers/{instance}/LogServices
[POST] /redfish/v1/Managers/{instance}/LogServices/AuditLog/Actions/LogService.ClearLog
[POST] /redfish/v1/Managers/{instance}/LogServices/EventLog/Actions/LogService.ClearLog
[POST] /redfish/v1/Managers/{instance}/LogServices/SEL/Actions/LogService.ClearLog
- Description
- Members
- Members@odata.count
- Name
- Oem
POST
Request:
POST https://{{ip}}/redfish/v1/Managers/Self/LogServices/AuditLog/Actions/LogService.ClearLog
https://{{ip}}/redfish/v1/Managers/Self/LogServices/EventLog/Actions/LogService.ClearLog
https://{{ip}}/redfish/v1/Managers/Self/LogServices/SEL/Actions/LogService.ClearLog
Content-Type: application/json
Example POST Request Body:
{
}
15.1.5.1. LogServices
[GET] /redfish/v1/Managers/{instance}/LogServices/{instance}
[PATCH] /redfish/v1/Managers/{instance}/LogServices/{instance}
- Id
- Name
- Description
- ServiceEnabled
- MaxNumberOfRecords
- OverWritePolicy
- DateTime
- DateTimeLocalOffset
- Actions
- Status
- Entries
- LogEntry Type
- Oem
15.1.5.1.1. Log Entry Collection
[GET] /redfish/v1/Managers/{instance}/LogServices/{instance}/Entries
- Description
- Members
- Members@odata.count
- Name
- Oem
15.1.5.1.1.1. Log Entry
[GET] /redfish/v1/Managers/Self/LogServices/AuditLog/Entries/{instance}
- Id
- Name
- Description
- Severity
- Created
- EventTimestamp
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 35/54

GIGABYTE Proprietary & Confidential
- EntryType
- Message
- MessageId
- MessageArgs
- Oem
- EventId
- EntryCode
- SensorType
- SensorNumber
- Links
- OriginOfCondition
- OemLogEntryCode
- OemSensorType
[GET] /redfish/v1/Managers/Self/LogServices/EventLog/Entries/{instance}
- Id
- Name
- Description
- Severity
- Created
- EventTimestamp
- EntryType
- EntryCode
- Message
- MessageId
- MessageArgs
- Links
- OriginOfCondition
- Oem
- EventId
- SensorType
- SensorNumber
- OemLogEntryCode
- OemSensorType
[GET] /redfish/v1/Managers/Self/LogServices/SEL/Entries/{instance}
- Id
- Name
- Description
- Severity
- Created
- EventTimestamp
- EntryType
- EntryCode
- SensorType
- SensorNumber
- MessageId
- Oem
- EventId
- Message
- MessageArgs
- Links
- OriginOfCondition
- OemLogEntryCode
- OemSensorType
15.1.6. NetworkProtocol
[GET] /redfish/v1/Managers/ {instance}/NetworkProtocol
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 36/54

GIGABYTE Proprietary & Confidential
[PATCH] /redfish/v1/Managers/{instance}/NetworkProtocol
- Id
- Name
- Description
- HostName
- FQDN
- HTTPS
- SNMP
- ProtocolEnabled
- Port
- AuthenticationProtocol
- EncryptionProtocol
- EngineId
- EnableSNMPv1
- EnableSNMPv2c
- EnableSNMPv3
- VirtualMedia
- SSDP
- IPMI
- SSH
- KVMIP
- Status
- Oem
- Telnet
- Actions
- NTP
- ProtocolEnabled
- Port
- NTPServers
15.1.7. Reset ActionInfo
[GET] /redfish/v1/Managers/{instance}/ResetActionInfo
- Description
- Id
- Name
- Parameters
15.1.8. SerialInterfaces Collection
[GET] /redfish/v1/Managers/{instance}/SerialInterfaces
- Description
- Members
- Members@odata.count
- Name
- Oem
15.1.8.1. SerialInterfaces
[GET] /redfish/v1/Managers/{instance}/SerialInterfaces/{instance}
[PATCH] /redfish/v1/Managers/{instance}/SerialInterfaces/{instance}
- Id
- Name
- Description
- Interface Enabled
- BitRate
- Parity
- DataBits
- StopBits
- FlowControl
- Oem
- SignalType
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 37/54

GIGABYTE Proprietary & Confidential
- ConnectorType
- PinOut
- Actions
15.1.9. VirtualMedia Collection
[GET] /redfish/v1/Managers/{instance}/VirtualMedia
- Description
- Members
- Members@odata.count
- Name
- Oem
15.1.9.1. VirtualMedia Collection
[GET] /redfish/v1/Managers/{instance}/VirtualMedia/{instance}
[POST] /redfish/v1/Managers/{instance}/VirtualMedia/{instance}/Actions/VirtualMedia.InsertMedia
[POST] /redfish/v1/Managers/{instance}/VirtualMedia/{instanc}}/Actions/VirtualMedia.EjectMedia
[POST] /redfish/v1/Managers/{instance}/Actions/Oem/AMIVirtualMedia.ConfigureCDInstance
[POST] /redfish/v1/Managers/{instance}/Actions/Oem/AMIVirtualMedia.EnableRMedia
- Actions
- ConnectedVia
- Description
- Id
- Image
- ImageName
- Inserted
- Name
- WriteProtected
- Oem
- MediaType
- TransferProtocolType
- TransferMethod
- UserName
POST
Request:
POST https://{{ip}}/redfish/v1/Managers/Self/VirtualMedia/CD1/Actions/VirtualMedia.InsertMedia
Content-Type: application/json
Example POST Request Body:
{
"Image": "nfs://10.0.125.169/home/tamil/images/images/ubuntu-14.04.1-desktop-amd64.iso",
"TransferProtocolType" : "NFS"
}
Request:
POST https://{{ip}}/redfish/v1/Managers/Self/VirtualMedia/CD1/Actions/VirtualMedia.EjectMedia
Content-Type: application/json
Example POST Request Body:
{}
Request:
POST https://{{ip}}/redfish/v1/Managers/Self/Actions/Oem/AMIVirtualMedia.ConfigureCDInstance
Content-Type: application/json
Example POST Request Body:
{
"CDInstance": 4
}
Request:
POST https://{{ip}}/redfish/v1/Managers/Self/Actions/Oem/AMIVirtualMedia.EnableRMedia
Content-Type: application/json
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 38/54

GIGABYTE Proprietary & Confidential
Example POST Request Body:
{
"RMediaState": "Enable"
}
16. InventoryData Status URI
[GET] /redfish/v1/Oem/Ami/InventoryData/Status
- Id
- Name
- Description
17.16. - InventoryDataMessage Registry File Collection
[GET] /redfish/v1/Registries
- Description
- Members
- Members@odata.count
- Name
- Oem
17.1.16.1. Message Registries
[GET] /redfish/v1/Registries/{instance}
- Description
- Id
- Languages
- Name
- Oem
- RegistryPrefix
- RegistryVersion
- OwningEntity
- Messages
17.2.16.2. Message Registries File
[GET] /redfish/v1/Registries/{instance.json}
- Description
- Id
- Languages
- Messages
- Name
- OwningEntity
- RegistryPrefix
- RegistryVersion
- Oem
18.17. Session Service
[GET] /redfish/v1/SessionService
[PATCH] /redfish/v1/SessionService
- Description
- Id
- Name
- ServiceEnabled
- SessionTimeout
- Sessions
- Status
- Oem
- Actions
18.1.17.1. Session Collection
[GET] /redfish/v1/SessionService/Sessions
[POST] /redfish/v1/SessionService/Sessions
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 39/54

GIGABYTE Proprietary & Confidential
- Description
- Members
- Members@odata.count
- Name
- Oem
POST
Request:
POST https://{{ip}}/redfish/v1/SessionService/Sessions
Content-Type: application/json
Example POST Request Body:
{
"UserName": "admin",
"Password": "password"
}
18.1.1.17.1.1. Session
[GET] /redfish/v1/SessionService/Sessions/{instance}
[DELETE] /redfish/v1/SessionService/Sessions/{instance}
- Id
- Name
- Description
- UserName
- Oem
- Password
- Actions
19.18. System Collection
[GET] /redfish/v1/Systems
[POST] /redfish/v1/Systems
@Redfish.CollectionCapabilities
- Capabilities
- Members
- Members@odata.count
- Name
- Description
- Oem
POST
Request:
POST https://{{ip}}/redfish/v1/Systems
Content-Type: application/json
Example POST Request Body:
{
"Name": "NewSystem",
"Links": {
"ResourceBlocks": [{
"@odata.id": "/redfish/v1/CompositionService/ResourceBlocks/ComputeBlock"
}]
},
"HostName":"gigabyte"
}
19.1.18.1. Capabilities
[GET] /redfish/v1/Systems/Capabilities
- Id
- Name
- Description
- Links
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 40/54

GIGABYTE Proprietary & Confidential
- ResourceBlocks
- Boot
- HostName
19.2.18.2. System
[GET] /redfish/v1/Systems/{instance}
[PATCH] /redfish/v1/Systems/{instance}
[POST]/redfish/v1/Systems/{instance}/Actions/ComputerSystem.Reset
- Id
- Name
- Description
- SystemType
- Physical- Links
- Oem- Chassis
- Chassis@odata.count
- ManagedBy
- ManagedBy@odata.count
- AssetTag
- Manufacturer
- Model
- SKU
- SerialNumber
- PartNumber
- UUID
- IndicatorLED
- PowerState
- Boot
- BiosVersion
- ProcessorSummary
- Count
- Model
- Status
- MemorySummary
- TotalSystemMemoryGiB- Status
- MemoryMirroring
- TotalSystemPersistentMemoryGiB
- Actions
- Processors
- EthernetInterfaces
- SimpleStorage
- LogServices
- Status
- SecureBoot
- Bios
- Memory
- Storage
- NetworkInterfaces
- Oem
- SubModel
- Hostname
- TrustedModules
- HostingRoles
- HostedServices
- PCIeDevices
- PCIeDevices@odata.count
- PCIeFunctions
- PCIeFunctions@odata.count
- PowerRestorePolicy
POST
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 41/54

GIGABYTE Proprietary & Confidential
Request:
POST https://{{ip}}/redfish/v1/Systems/Self/Actions/ComputerSystem.Reset
Content-Type: application/json
Request Body:
The ResetType can be one of the following values: "On", "ForceOff", "GracefulShutdown", "ForceRestart".
Example POST Request Body:
{
"ResetType" : "On"
}
19.2.1.18.2.1. BIOS
[GET] /redfish/v1/Systems/{instance}/Bios
[POST] /redfish/v1/Systems/{instance}/Bios/Actions/Bios.ResetBios
[POST] /redfish/v1/Systems/{instance}/Bios/Actions/Bios.ChangePassword
- Oem
- Id
- Name
- Description
- AttributeRegistry
- Actions
- Attributes
POST
Request:
POST https://{{ip}}/redfish/v1/Systems/Self/Bios/Actions/Bios.ResetBios
Content-Type: application/json
Example POST Request Body:
{
"ResetType": "Reset"
}
Request:
POST https://{{ip}}/redfish/v1/Systems/Self/Bios/Actions/Bios.ChangePassword
Content-Type: application/json
Example POST Request Body:
{
"PasswordName": "SETUP001",
"OldPassword": "old",
"NewPassword": "new"
}
19.2.1.1.18.2.1.1. BIOS SD
[POST] /redfish/v1/Systems/{instance}/Bios/SD
[PATCH] /redfish/v1/Systems/{instance}/Bios/SD
[PUT] /redfish/v1/Systems/{instance}/Bios/SD
- Id
- Name
- Description
- AttributeRegistry
- Attributes
- Actions
POST
Request:
POST https://{{ip}}/redfish/v1/Systems/Self/Bios/SD
Content-Type: application/json
Example POST Request Body:
{
"Attributes": {
"PCIS003": "Disabled"
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 42/54

GIGABYTE Proprietary & Confidential
}
}
19.2.2.18.2.2. BootOption Collection
[GET] /redfish/v1/Systems/{instance}/BootOoptions
- Description
- Members
- Members@odata.count
- Name
- Oem
19.2.2.1.18.2.2.1. BootOoptions
[GET] /redfish/v1/Systems/{instance}/BootOoptions/{instance}
- Id
- Name
- Description
- BootOptionEnabled
- BootOptionReference
- DisplayName
- UefiDevicePath
- Alias
- Oem
- RelatedItem
- RelatedItem@odata.count
19.2.3.18.2.3. EthernetInterfaces Collection
[GET] /redfish/v1/Systems/{instance}/EthernetInterfaces
- Description
- Members
- Members@odata.count
- Name
- Oem
19.2.3.1.18.2.3.1. EthernetInterfaces
[GET] /redfish/v1/Systems/{instance}/EthernetInterfaces/{instance}
- Id
- Status
- MACAddress
- LinkStatus
- Links
- Name
- Oem
- UefiDevicePath
- InterfaceEnabled
- PermanentMACAddress
- Ipv4Addresses
- Ipv6Addresses
- Ipv6DefaultGateway
- VLANs
- Actions
- DHCPv4
- DHCPv6
19.2.3.1.1.18.2.3.1.1. VLAN Network Interface Collection
[GET] /redfish/v1/Systems/{instance}/EthernetInterfaces/{instance}/VLANs
[POST] /redfish/v1/Systems/{instance}/EthernetInterfaces/{instance}/VLANs
- Members
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 43/54

GIGABYTE Proprietary & Confidential
- Members@odata.count
- Name
- Description
- Oem
POST
Request:
POST
https://{{ip}}/redfish/v1/Systems/{{system_instance}}/EthernetInterfaces/{{system_ethifc_instance}}/VLANs
Content-Type: application/json
Example POST Request Body:
{
"VLANId": 100,
"VLANEnable":true,
"VLANPriority":2
}
19.2.3.1.1.1.1.18.2.3.1.1.1.1. VLANNetworkInterface
[GET] /redfish/v1/Systems/{instance}/EthernetInterfaces/{instance}/VLANs/{instance}
[PATCH] redfish/v1/Systems/{instance}/EthernetInterfaces/{instance}/VLANs/{instance}
[DELETE] redfish/v1/Systems/{instance}/EthernetInterfaces/{instance}/VLANs/{instance}
- Id
- Name
- Description
- VLANEnable
- VLANId
- Oem
- Actions
19.2.4.18.2.4. LogServices Collection
[GET] /redfish/v1/Systems/{instance}/LogServices
- Description
- Members
- Members@odata.count
- Name
- Oem
19.2.4.1.18.2.4.1. LogServices
[GET] /redfish/v1/Systems/{instance}/LogServices /{instance}
[PATCH] /redfish/v1/Systems/{instance}/LogServices/{instance}
[POST] /redfish/v1/Systems/{instance}/LogServices/{instance}/Actions/LogService.ClearLog
- Oem
- Id
- Name
- Description
- ServiceEnabled
- MaxNumberOfRecords
- OverWritePolicy
- WrapsWhenFull
- DateTime
- DateTimeLocalOffset
- Actions
- Status
- Entries
- LogEntry Type
POST
Request:
POST https://{{ip}}/redfish/v1/Systems/Self/LogServices/BIOS/Actions/LogService.ClearLog
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 44/54

GIGABYTE Proprietary & Confidential
Content-Type: application/json
Example POST Request Body:
{
}
19.2.4.1.1.18.2.4.1.1. Log Entry Collection
[GET] /redfish/v1/Systems/{instance}/LogServices /{instance}/Entries
- Description
- Members
- Members@odata.count
- Name
- Oem
19.2.4.1.1.1.18.2.4.1.1.1. Log Entry
[GET] /redfish/v1/Systems/{instance}/LogServices /{instance}/Entries /{instance}
- Id
- Name
- Description
- Severity
- Created
- EventId
- EventTimestamp
- EntryType
- EntryCode
- SensorType
- SensorNumber
- Message
- MessageId
- MessageArgs
- Oem
- Links
- OriginOfCondition
- OemLogEntryCode
- OemSensorType
19.2.5.18.2.5. Memory Collection
[GET] /redfish/v1/Systems/{instance}/Memory
- Description
- Members
- Members@odata.count
- Name
- Oem
19.2.5.1.18.2.5.1. Memory
[GET] /redfish/v1/Systems/{instance}/Memory/{instance}
- Id
- Name
- Description
- MemoryType
- MemoryDeviceType
- CapacityMiB
- DataWidthBits
- BusWidthBits
- Manufacturer
- SerialNumber
- PartNumber
- AllowedSpeedsMHz
- DeviceLocator
- ErrorCorrection
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 45/54

GIGABYTE Proprietary & Confidential
- OperatingSpeedMhz
- Links
- Chassis
- Status
- Oem
- BaseModuleType
- MemoryMedia
- Assembly
- FirmwareRevision
- FirmwareApiVersion
- FunctionClasses
- MaxTDPMilliWatts
- SecurityCapabilities
- SpareDeviceCount
- ConfigurationLocked
- RankCount
- MemoryLocation
- VolatileRegionSizeLimitMiB
- PersistentRegionSizeLimitMiB
- Regions
- OperatingMemoryModes
- PowerManagementPolicy
- IsSpareDeviceEnabled
- IsRankSpareEnabled
- VolatileRegionNumberLimit
- PersistentRegionNumberLimit
- VolatileRegionSizeMaxMiB
- PersistentRegionSizeMaxMiB
- AllocationIncrementMiB
- AllocationAlignmentMiB
- ModuleManufacturerID
- ModuleProductID
- MemorySubsystemControllerManufacturerID
- MemorySubsystemControllerProductID
- VolatileSizeMiB
- NonVolatileSizeMiB
- CacheSizeMiB
- LogicalSizeMiB
- Location
- Metrics
19.2.6.18.2.6. MemoryDomains Collection
[GET] /redfish/v1/Systems/{instance}/MemoryDomains
- Description
- Members
- Members@odata.count
- Name
- Oem
19.2.7.18.2.7. NetworkInterface Collection
[GET] /redfish/v1/Systems/{instance}/NetworkInterfaces
- Description
- Members
- Members@odata.count
- Name
- Oem
19.2.7.1.18.2.7.1. NetworkInterface
[GET] /redfish/v1/Systems/{instance}/NetworkInterfaces/{instance}
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 46/54

GIGABYTE Proprietary & Confidential
- Oem
- Id
- Name
- Description
- Status
- Links
- NetworkDeviceFunctions
- Actions
19.2.8.18.2.8. Processor Collection
[GET] /redfish/v1/Systems/{instance}/Processors
- Members
- Members@odata.count
- Name
- Description
- Oem
19.2.8.1.18.2.8.1. Processor
[GET] /redfish/v1/Systems/{instance}/Processors/{instance}
- Id
- Name
- Description
- Socket
- Status
- State
- Health
- ProcessorType
- ProcessorArchitecture
- InstructionSet
- ProcessorId
- IdentificationRegisters
- EffectiveFamily
- EffectiveModel
- Step- Manufacturer
- Model
- MaxSpeedMHz
- TotalCores
- TotalThreads
- Links- Chassis
-
- Oem
- Actions
- SubProcessors
- Location
- Assembly
- MaxTDPWatts
- Metrics
- TDPWatts
- TotalEnabledCores
- UUID
- FPGA
- ProcessorMemory
- CapacityMiB
- IntegratedMemory
- MemoryType
- SpeedMHz
19.2.9.18.2.9. SimpleStorage Collection
[GET] /redfish/v1/Systems/{instance}/SimpleStorage
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 47/54

GIGABYTE Proprietary & Confidential
- Members
- Members@odata.count
- Name
- Description
- Oem
19.2.9.1.18.2.9.1. SimpleStorage
[GET] /redfish/v1/Systems/{instance}/SimpleStorage/{instance}
- Id
- Name
- Description
- Links
- Oem
- UefiDevicePath
- Status
- Actions
19.2.10.18.2.10. Storage Collection
[Get] /redfish/v1/Systems/{instance}/Storage
- Members
- Members@odata.count
- Name
- Description
- Oem
19.2.10.1.18.2.10.1. Storage
[GET] /redfish/v1/Systems/{instance}/Storage/{instance}
- Id
- Name
- Description
- Oem
- Status
- Links
- StorageControllers@odata.count
- StorageControllers
- Drives@odata.count
- Drives
- Volumes
- Redundancy@odata.count
20.19. - RedundancyTaskService
[GET] /redfish/v1/TaskService
- CompletedTaskOverWritePolicy
- DateTime
- Description
- Id
- LifeCycleEventOnTaskStateChange
- Name
- ServiceEnabled
- Status
- Tasks
- Oem
- Actions
20.1.19.1. Task Collection
[GET] /redfish/v1/TaskService/Tasks
- Description
- Members
- Members@odata.count
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 48/54

GIGABYTE Proprietary & Confidential
- Name
- Oem
20.1.1.19.1.1. Task
[GET] /redfish/v1/TaskService/Tasks/{instance}
[DELETE] /redfish/v1/TaskService/Tasks/{instance}
- Oem
- Id
- Name
- Description
- TaskState
- StartTime
- EndTime
- TaskStatus
- Messages
- Actions
- HidePayload
- PercentComplete
- Payload
21.20. TelemetryService
[Get] /redfish/v1/TelemetryService
[POST] /redfish/v1/TelemetryService/Actions/TelemetryService.SubmitTestMetricReport
[PATCH] /redfish/v1/TelemetryService
- Oem
- Id
- MetricDefinitions
- MetricReportDefinitions
- MetricReports
- Triggers
- Status
- Name
- MaxReports
- MinCollectionInterval
- SupportedCollectionFunctions
- Actions
- LogService
- Description
- ServiceEnabled
- SupportedCollectionFunctions@Redfish.AllowableValues
POST
Request:
POST https://{{ip}}/redfish/v1/TelemetryService/Actions/TelemetryService.SubmitTestMetricReport
Content-Type: application/json
Example POST Request Body:
{
"MetricReportName":"Average2",
"GeneratedMetricReportValues":[{
"MetricId": "Temp_average_reading_Average",
"MetricProperty": "/redfish/v1/Chassis/Self/Thermal#/Temperatures/0/ReadingCelsius",
"MetricValue": "23",
"Timestamp": "2019-07-01T06:05:52Z"
}]
}
21.1.20.1. MetricReportLog Collection
[Get] /redfish/v1/TelemetryService/LogService
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 49/54

GIGABYTE Proprietary & Confidential
[POST] /redfish/v1/TelemetryService/LogService/Actions/LogService.ClearLog
- Description
- Members
- Members@odata.count
- Name
- Oem
POST
Request:
POST https://{{ip}}/redfish/v1//TelemetryService/LogService/Actions/LogService.ClearLog
Content-Type: application/json
Example POST Request Body:
{
}
21.1.1.20.1.1. MetricReportLog
[Get] /redfish/v1/TelemetryService/LogService/
[Post] redfish/v1/TelemetryService/LogServices/MetricReportLog/Actions/LogService.ClearLog
- Id
- Name
- Description
- ServiceEnabled
- MaxNumberOfRecords
- OverWritePolicy
- Actions
- Status
- Entries
- DateTime
- DateTimeLocalOffset
- Oem
- LogEntryType
POST
Request:
POST https://{{ip}}/TelemetryService/LogService/ /Actions/LogService.ClearLog
Content-Type: application/json
Example POST Request Body:
{
}
21.1.1.1.20.1.1.1. Entries Collection
[Get] /redfish/v1/TelemetryService/LogService/ Entries
- Description
- Members
- Members@odata.count
- Name
- Oem
21.1.1.1.1.20.1.1.1.1. Entries
[Get] /redfish/v1/TelemetryService/LogService/ Entries/{instance}
- Id
- Name
- Description
- Severity
- Created
- EntryType
- EntryCode
- Message
- MessageId
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 50/54

GIGABYTE Proprietary & Confidential
- MessageArgs
- Links
- OriginOfCondition
- Oem
- EventId
- EventTimestamp
- SensorType
- SensorNumber
- OemLogEntryCode
- OemSensorType
21.2.20.2. MetricDefinitions Collection
[Get] /redfish/v1/TelemetryService/MetricDefinitions
- Members
- Members@odata.count
21.2.1.20.2.1. - NameMetricDefinitions
[Get] /redfish/v1/TelemetryService/MetricDefinitions/{instance}
- Id
- Name
- MetricType
- MetricDataType
- Implementation
- Units
- IsLinear
- MetricProperties
- Precision
- Accuracy
21.3.20.3. MetricReportDefinition Collection
[Get] /redfish/v1/TelemetryService/MetricReportDefinitions
[POST] /redfish/v1/TelemetryService/MetricReportDefinitions
- Members
- Members@odata.count
- Name
POST
Request:
POST https://{{ip}}/redfish/v1/TelemetryService/MetricReportDefinitions
Content-Type: application/json
Example POST Request Body:
{
"Id":"Voltage_Report",
"Name":"Voltage_Report",
"Schedule":{
"RecurrenceInterval":"PT20S"
},
"MetricReportDefinitionType":"Periodic",
"MetricReport":{
"@odata.id":"/redfish/v1/TelemetryService/MetricReports/Voltage_Report"
},
"MetricProperties":["/redfish/v1/Chassis/Self/Power#/Voltages/0/ReadingVolts"]
}
21.3.1.20.3.1. MetricReportDefinitions
[Get] /redfish/v1/TelemetryService/MetricReportDefinitions/{instance}
[Delete] /redfish/v1/TelemetryService/MetricReportDefinitions/{instance}
[PATCH] /redfish/v1/TelemetryService/MetricReportDefinitions/{instance}
- Id
- Name
- Schedule
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 51/54

GIGABYTE Proprietary & Confidential
- MetricReportDefinitionType
- Status
- MetricReport
- Metrics/MetricProperties
- MetricReportDefinitionEnable
- ReportTimespan
- ReportActions
- ReportUpdates
- Metrics
- MetricProperties
21.4.20.4. MetricReports Collection
[Get] /redfish/v1/TelemetryService/MetricReports
- Members
- Members@odata.count
21.4.1.20.4.1. - NameMetricReports
[Get] /redfish/v1/TelemetryService/MetricReports/{instance}
- Id
- Name
- MetricReportDefinition
- Timestamp
- ReportSequence
- MetricValues
21.5.20.5. Triggers Collection
[Get] /redfish/v1/TelemetryService/Triggers
[Post] /redfish/v1/TelemetryService/Triggers
- Members
- Members@odata.count
- Name
POST
Request:
POST https://{{ip}}/redfish/v1/TelemetryService/Triggers
Content-Type: application/json
The following properties are mandatory to create a trigger:
 Id
 Name
 MetricType
 TriggerActions
 NumericTriggers or (DiscreteTriggerCondition & DiscreteTriggers)
 MetricProperties
Note:
 Status->State and Status-Health are read-only attributes and cannot be passed in the POST Request
Body.
 Only a maximum of 25 triggers can be created.
Example POST Request to create Numeric Triggers Body:
{
"Id":"Temperature_Trigger",
"Name":"Temperature_Trigger",
"MetricType":"Numeric",
"TriggerActions":["LogToLogService"],
"NumericTriggers":[ {
"Name":"UpperThresholdCritical",
"Value": 50.0,
"DirectionOfCrossing":"Increasing"
}, {
"Name":"UpperThresholdNonCritical",
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 52/54

GIGABYTE Proprietary & Confidential
"Value": 48.1,
"DirectionOfCrossing":"Increasing"
}],
"MetricProperties":["/redfish/v1/Chassis/Self/Thermal#/Temperatures/0/ReadingCelsius"]
}
Example POST Request to create Discrete Triggers Body:
{
"Id":"Chassis_LED",
"Name":"Chassis_LED",
"MetricType":"Discrete",
"TriggerActions":[ "LogToLogService", "RedfishEvent" ],
"DiscreteTriggerCondition":"Specified",
"DiscreteTriggers":[{
"Name":"LED_On",
"Value":"On",
"Severity":"Warning"
}],
"MetricProperties":[ "/redfish/v1/Chassis/Self#/IndicatorLED" ]
}
21.5.1.20.5.1. Triggers
[Get] /redfish/v1/TelemetryService/Triggers/{instance}
[Delete] /redfish/v1/TelemetryService/Triggers/{instance}
- Id
- Name
- MetricType
- DiscreteTriggerCondition
- Status
- DiscreteTriggers
- Description
22.21. UpdateService
[GET] /redfish/v1/UpdateService
[PATCH] /redfish/v1/UpdateService
[POST] /redfish/v1/UpdateService/Actions/SimpleUpdate
- Actions
- Description
- Id
- Name
- Oem
- ServiceEnabled
- Status
- MaxImageSizeBytes
- MultipartHttpPushUri
- FirmwareInventory
POST
Request:
POST https://{{ip}}/redfish/v1/UpdateService/Actions/SimpleUpdate
Content-Type: application/json
Example POST Request Body:
Anonymous:
{"TransferProtocol":" FTP ", "ImageURI": " ftp://{FTP_server_IP}/{image_name}.ima"}
{"TransferProtocol":" HTTP", "ImageURI": "http://{HTTP_server_IP}/{image_name}.ima"}
user account:
{"TransferProtocol":" FTP ",
"ImageURI":ftp://{FTP_server_IP}/{image_name}.ima","User":"User","Password":"Password"}
22.1.21.1. SimpleUpdateActionInfo
[GET] /redfish/v1/UpdateService/SimpleUpdateActionInfo
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 53/54

GIGABYTE Proprietary & Confidential
- Id
- Name
- Parameters
22.2.21.2. FirmwareInventory Collection
[GET] /redfish/v1/UpdateService/FirmwareInventory
- Description
- Members
- Members@odata.count
- Name
- Oem
22.2.1.21.2.1. FirmwareInventory
[GET] /redfish/v1/UpdateService/FirmwareInventory /{instance}
- Id
- Name
- Updateable
- Oem
- Description
© Copyright Gigabyte 2017 All Rights Reserved
EasonWenny GIGABYTE Redfish API Spec GIGABYTE Redfish API Spec 1.11.0
ChenTsai Doc V1.04 (AMI).Doc
0605/1601/2023 54/54