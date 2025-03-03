#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 陈烜 42766
    :时间: 2023/3/24 14:12
    :修改者: 陈烜 42766
    :更新时间: 2023/3/24 14:12
"""
# flake8: noqa


first_categories = """
006	物联网设备      Internet of Things device   a hardware device that is connected to the internet and has the ability to collect and exchange data with other devices, often through sensors and wireless communication
100	数据库          Database                    a structured collection of data that is stored and organized in a way that allows for efficient retrieval and manipulation of information, often used to support software applications and business operations
101	中间件          Middleware                  software that acts as a bridge between different applications, systems, or components, providing a common platform for communication and data exchange.
102	开发语言        Language                    a formal language used to write computer programs, which are sets of instructions that can be executed by a computer to perform specific tasks
103	开发框架        Framework                   a set of pre-written code and tools that provide a foundation for building software applications, allowing developers to focus on writing application-specific code rather than low-level infrastructure
104	应用服务        Application                 a software program designed to perform a specific task or set of tasks, often used to support business operations, productivity, entertainment, or communication
001	服务器设备      Server device               a piece of hardware designed to provide services or resources to other devices or computers on a network
002	终端设备        Terminal device             a hardware device that allows a user to interact with a computer or network, typically through a keyboard and monitor or display
003	内网设备        Intranet device             a hardware device that is connected to a private network, allowing it to communicate with other devices on the same network but not with devices on external networks
004	互联网设备      Internet device             a hardware device that is connected to the global network of networks, allowing it to communicate with other devices and access resources and services available on the internet
005	网络设备        Networking device           a hardware device that facilitates communication and data transfer between devices on a network, such as routers, switches, hubs, and modems
007	移动设备        Mobile device               a portable hardware device, such as a smartphone or tablet, that is designed for wireless communication and can be easily carried and used on the go
008	网络安全设备    Network security device     a hardware device designed to protect a network from unauthorized access, attacks, and other security threats, such as firewalls, intrusion detection and prevention systems, and VPN gateways
009	云平台设备      Cloud platform device       a hardware device that provides the infrastructure and resources for cloud computing services, such as servers, storage, and networking equipment, to enable users to access and use cloud-based applications and services
010	工控设备        Industrial Control device   a hardware device used to monitor and control industrial processes, such as manufacturing, production, and distribution, often through sensors, programmable logic controllers (PLCs), and human-machine interfaces (HMIs)
200	操作系统        Operation system            a software program that manages computer hardware and software resources, providing a stable and consistent environment for applications to run and interact with the underlying hardware
"""

c_001 = """
Server Module	                                    00100002
Server Management	                                00100003
File Transfer Protocol Server	                    00100004
HyperText Transfer Protocol Proxy Server	        00100005
Simple Mail Transfer Protocol Server	            00100006
Open Simple Mail Transfer Protocol Relay Server	    00100007
Server Message Block Protocol Server	            00100008
Remote Authentication Dial In User Service Server	00100009
Software Update Server	                            00100010
Security Audit Server	                            00100011
Active Directory Server	                            00100012
Domain Controller Server	                        00100013
Database Server	                                    00100014
Authentication Server	                            00100015
World Wide Web Server	                            00100016
Application Server	                                00100017
Attendance Server	                                00100018
Code Management Server	                            00100019
File Management Server	                            00100020
Distributed Server	                                00100021
Mail Server	                                        00100022
Mining Server	                                    00100023
Domain Name Server	                                00100024
Distributed Numerical Control Server	            00100025
Other Server device	                                00100001
"""

c_002 = """
Desktop	                                            00200002
Laptop	                                            00200003
Connection-Sharing Endpoint                         00200004
Dumb Endpoint	                                    00200005
Thin Client	                                        00200006
Other Terminal device	                            00200001
"""

c_003 = """
Other Intranet device	                            00300001
"""

c_004 = """
Other Internet device	                            00400001
"""

c_005 = """
Traditional Network Service Device	                00500002
Gateway Device	                                    00500003
Network Agent Device	                            00500004
Network Module Device	                            00500005
Network Adapter Device	                            00500006
Voice over Internet Protocol Adapter	            00500007
Voice over Internet Protocol Device	                00500008
Universal Media Gateway Device                      00500009
Plug and Play Device	                            00500010
Network Load Balancer Device	                    00500011
Uninterruptible Power Supply Device	                00500012
Router Device	                                    00500013
Switch Device	                                    00500014
Broadband Router Device	                            00500015
Wireless Access Point Device	                    00500016
Wireless Fidelity Probe Device	                    00500017
Keyboard-Video-Mouse Switch Device	                00500018
Network Management Device	                        00500019
Modem Device	                                    00500020
Asymmetric Digital Subscriber Line Device	        00500021
Wireless Local Area Network Device	                00500022
Wireless Access Controller	                        00500023
Other Networking device	                            00500001
"""

c_006 = """
Decoder Device                                                          00600002
Encoder Device                                                          00600003
Traffic Signal Controller Device	                                    00600004
Network Control Keyboard Device	                                        00600005
Red Light Signal Detector Device	                                    00600006
Access Control System Device	                                        00600007
Law Enforcement Data Collection Device	                                00600008
Monitoring System Device	                                            00600009
Digital Video Recorder	                                                00600010
Network Video Recorder	                                                00600011
X-Video Recorder	                                                    00600012
Traffic Enforcement Camera Device	                                    00600013
Traffic Signal Detector Device	                                        00600014
Endpoint Management Device	                                            00600015
Video Surveillance All-in-one Device	                                00600016
Printer	                                                                00600017
Copier	                                                                00600018
Fax Device	                                                            00600019
Scanner	                                                                00600020
Medical Imaging Device	                                                00600021
ECG Monitor	                                                            00600022
Ventilator	                                                            00600023
Video Surveillance Device	                                            00600024
Automated Control	                                                    00600025
Edge Computing Device	                                                00600026
Digital Radiography Device	                                            00600027
Medical Image Printer	                                                00600028
Computed Tomography Scanner	                                            00600029
Radiology Workstation	                                                00600030
Radiology Information System Device	                                    00600031
Picture Archiving and Communication System Device	                    00600032
Digital Imaging And Communications In Medicine Workstation	            00600033
Digital Imaging And Communications In Medicine Gateway	                00600034
Digital Imaging And Communications In Medicine Modality System Device	00600035
Digital Imaging And Communications In Medicine Video Recorder	        00600036
Computed Tomography Workstation	                                        00600037
Medical Ultrasonic Instrument	                                        00600038
Ultrasonic Workstation	                                                00600039
Medical Information System Device	                                    00600040
Proton-Therapy Imaging System Device	                                00600041
Radiotherapy System Device	                                            00600042
Radiotherapy Workstation	                                            00600043
X-Ray Workstation	                                                    00600044
Mammography System Device	                                            00600045
Mammography Workstation	                                                00600046
Image-Guided Therapy System Device	                                    00600047
Image-Guided Surgery System Device	                                    00600048
Treatment Planning System Device	                                    00600049
Surgical Microscope Device	                                            00600050
Optometry and Ophthalmology System Device	                            00600051
Optical Biometric Identification System Device	                        00600052
Optical Coherence Tomography System Device	                            00600053
Optical Coherence Tomography Station	                                00600054
Positron Emission Tomography And Computed tomography Scanner	        00600055
Magnetic Resonance Imaging Scanner	                                    00600056
Magnetic Resonance Imaging Workstation	                                00600057
Angiography System Device	                                            00600058
Interventional X-Ray System Device	                                    00600059
Computed Radiography Medical Image Scanner	                            00600060
Nuclear Medicine System Device	                                        00600061
Positron Emission Tomography Scanner	                                00600062
Cardiology Workstation	                                                00600063
Mobile C-arm X-Ray System Device	                                    00600064
Nuclear Medicine Workstation	                                        00600065
Molecular Imaging System Device	                                        00600066
Fluoroscopic Examination System Device	                                00600067
Electrocardiogram Gateway Device	                                    00600068
Electrocardiograph Recorder	                                            00600069
ECG Data Collection Workstation	                                        00600070
Cardiovascular Workstation	                                            00600071
Dental Image View Device	                                            00600072
Vascular Diagnostic Device	                                            00600073
Other Medical Device	                                                00600074
Intelligent Control System Device	                                    00600075
Embedded Device	                                                        00600076
Satellite Related System Device	                                        00600077
Positioning System Device	                                            00600078
Local Maintenance Terminal	                                            00600079
Intelligent Entrance Guard Device	                                    00600080
Network Attached Storage Device	                                        00600081
Video Conferencing System Device	                                    00600084
Media Device	                                                        00600085
On board Remote System Device	                                        00600086
License Plate Recognition Device	                                    00600087
Large-Screen Device	                                                    00600088
Alarm Device	                                                        00600089
Intelligent Collection Device	                                        00600090
Vehicle Inspection Device	                                            00600091
Camera	                                                                00600092
Automatic Gate Machine	                                                00600096
Smart Ward Device	                                                    00600097
Mobile Nursing Device	                                                00600098
Ward-Round Trolley	                                                    00600099
Queue Management System Device	                                        00600100
Blood Collecting System Device	                                        00600101
Self-Service Terminal Device	                                        00600102
Patient Call Screen Device	                                            00600103
Personal Digital Assistant Device	                                    00600104
B-Scan Device	                                                        00600105
Patient Monitor	                                                        00600106
Other Internet of Things device	                                        00600001
"""

c_007 = """
Mobile Phone	    00700002
Tablet	            00700003
Other Mobile device	00700001
"""

c_008 = """
Security Access Control System	                        00800002
Honeypot Device	                                        00800003
Firewall Device	                                        00800004
Endpoint Detection and Response Device	                00800005
Extended Detection and Response Device	                00800006
Penetration Testing Device	                            00800007
Security Scanner	                                    00800008
File Transfer Security	                                00800009
Situational-Awareness and Security Operations Device	00800010
Bastion Host	                                        00800011
Threat Intelligence Product	                            00800012
Virtual Private Network Device	                        00800013
Anti-DDoS Device	                                    00800014
World Wide Web Application Firewall	                    00800015
Intrusion Detection and Prevention Device	            00800016
Log Audit and Management Device	                        00800017
Log Analysis Platform	                                00800018
Penetration Tool Platform	                            00800019
Traffic Analysis and Audit	                            00800020
Air Gap	                                                00800021
Internet Access Management	                            00800022
Database Audit	                                        00800023
Security Audit	                                        00800024
Authentication System	                                00800025
website Cloud-Based Protection	                        00800026
Security Check Platform	                                00800027
Anti-Defacement System	                                00800028
Encryption Product	                                    00800029
Security Software	                                    00800030
Penetration Tool	                                    00800031
Antivirus Software	                                    00800032
Other Network security device	                        00800001
"""

c_009 = """
Content Delivery Network Virtualization	    00900002
Software As A Service Platform	            00900003
webmaster Platform	                        00900004
Enterprise Cloud Platform	                00900005
Managed Cloud Platform	                    00900006
Big Data Platform	                        00900007
Virtual Machine	                            00900008
Application Container	                    00900009
Image Management	                        00900010
Other Cloud platform device	                00900001
"""

c_010 = """
Programmable Logic Controller	                01000002
Distributed Control System	                    01000003
Supervisory Control and Data Acquisition System	01000004
Human-Machine Interface	                        01000005
Machine Vision System	                        01000006
Motion Control System	                        01000007
Artificial Intelligence System	                01000008
Power Electronics System	                    01000009
Sensors and Actuators	                        01000010
Robot Control System	                        01000011
Other Industrial Control device	                01000001
"""

c_100 = """
Database	                    10000002
Storage Management Product	    10000003
Storage System	                10000004
Big Data System	                10000005
Other Database	                10000001
"""

c_101 = """
World Wide Web Middleware	    10100002
World Wide Web Server	        10100003
Message Queue	                10100004
Message Middleware	            10100005
Embedded World Wide Web Server	10100006
Other Middleware	            10100001
"""

c_102 = """
Programming Language	        10200002
Other Language	                10200001
"""

c_103 = """
Development Template	                10300002
World Wide Web Development Framework	10300003
Software Development Kit	            10300004
World Wide Web Application Plugin	    10300005
Other Framework	                        10300001
"""

c_104 = """
Customer Service System	                            10400002
Blockchain	                                        10400003
Outdoor Advertising	                                10400004
Machine Learning	                                10400005
Remote Control	                                    10400006
Data Collection	                                    10400008
Application Programming Interface	                10400009
Data Processing	                                    10400010
Version Management Tool	                            10400011
Software Tool	                                    10400012
Remote Control Service	                            10400013
Digital Publishing	                                10400014
Voice and Live Chat                             	10400015
Development Kit	                                    10400016
E-Commerce Transaction	                            10400017
Mobile Device Management	                        10400018
Application Program Interface Management Platform	10400019
Collaborative Product	                            10400020
Office Software	                                    10400021
Antivirus Software	                                10400022
Security Software	                                10400023
Penetration Tool	                                10400024
Financial System	                                10400025
Office Automation System	                        10400026
Enterprise Management	                            10400027
Project Management	                                10400028
Enterprise Resource Planning	                    10400029
Source Code Management	                            10400030
Issue Management System	                            10400031
Human Resources Management System	                10400032
Database Management Tool	                        10400033
File Management Product	                            10400034
Content Management System	                        10400035
Customer Relationship Management System         	10400036
Asset Management System	                            10400037
Online Document Management System	                10400038
Collaborative Editor	                            10400039
Electronic Forum and Bulletin Board	                10400040
Phone Call System	                                10400041
Project Management	                                10400042
Browser	                                            10400043
Other Application	                                10400001
"""

c_200 = """
Windows	                    20000002
Linux	                    20000003
MacOS	                    20000004
iOS	                        20000005
AirOS	                    20000006
Android	                    20000007
FreeBSD	                    20000008
VMware	                    20000009
Cisco	                    20000010
MikroTik	                20000011
VxWorks	                    20000012
F5 Networks	                20000013
UNIX	                    20000014
HP-UX	                    20000015
Turbo	                    20000016
UbuntuKylin	                20000017
Deepin	                    20000018
NeoKylin	                20000019
StartOS	                    20000020
RedFlag	                    20000021
Asianux	                    20000022
CGSL	                    20000023
BCLinux	                    20000024
SUSE	                    20000025
Fedora	                    20000026
Ubuntu	                    20000027
Debian	                    20000028
CentOS	                    20000029
Gentoo	                    20000030
Slackware	                20000031
RHEL	                    20000032
openSUSE	                20000033
ArchLinux	                20000034
OracleLinux	                20000035
EulerOS	                    20000036
Alpine	                    20000037
UOS	                        20000038
Cloud OS	                20000039
Embedded Operating System	20000040
FreeboxOS	                20000041
Contiki	                    20000042
Fedora OS	                20000043
OneFS OS	                20000044
Other Operation system	    20000001
"""

CATEGORIES_MAP = {
    "first": first_categories,
    "001": c_001,
    "002": c_002,
    "003": c_003,
    "004": c_004,
    "005": c_005,
    "006": c_006,
    "007": c_007,
    "008": c_008,
    "009": c_009,
    "010": c_010,
    "100": c_100,
    "101": c_101,
    "102": c_102,
    "103": c_103,
    "104": c_104
}
