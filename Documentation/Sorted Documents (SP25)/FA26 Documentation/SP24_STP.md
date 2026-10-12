

|  Chesapeake Community Connection Website Software Test Plan Version 1.0 January 24th, 2024 St. Mary’s College of Maryland Capstone Kylie Hall John Heinig Malik Hill Naheed John Yaro Kulchyckyj Isabella Stephens Brittany Brenneman  |
| ----- |

**Table of Contents**

[**1\.  Introduction	2**](#1.-introduction)

[1.1 Purpose	2](#1.1-purpose)

[1.3 Definitions, Acronyms, and Abbreviations	3](#1.3-definitions,-acronyms,-and-abbreviations)

[1.4 Document References	3](#1.4-document-references)

[1.5 System Overview	3](#1.5-system-overview)

[**2\. Requirements to be Tested	4**](#2.-requirements-to-be-tested)

[**3\. Testing Approach	4**](#3.-testing-approach)

[**4\. Test Process	4**](#4.-test-process)

[**5\. Reporting and Corrective Actions	4**](#5.-reporting-and-corrective-actions)

[**6\. Test Environment	5**](#6.-test-environment)

[**7\. Test Procedures	5**](#7.-test-procedures)

[**8\.  Miscellaneous	6**](#8.-miscellaneous)

**Revision History**

| Date | Version | Description | Author(s) |
| :---: | :---: | :---: | :---: |
|  October 30th, 2023 | 1.0 | Initial version Of STP | Kylie Hall John Heinig Malik Hill Naheed John Yaro Kulchyckyj Isabella Stephens  Brittany Brenneman |
|  January 24th, 2024 |  1.0 | Start of revisions for 2024 | Daniel Reina Alex Ochman Gavin McDonald John Heinig Kendahl Michael Shively   |
|   |   |   |   |

# **1\.  Introduction** {#1.-introduction}

## **1.1 Purpose** {#1.1-purpose}

The purpose of this document is to formally state the procedures to be used for testing the software product and identify specific test cases. It will provide all testing processes, approaches, environments, and procedures that will be performed for each requirement to be tested.

**1.2 Scope**

The Software Test Plan (STP) establishes a thoroughly detailed plan for the testing of all software requirements in the Chesapeake Community Connection website. First, in Section 2 (Requirements to Be Tested) the document will state all requirements that will be tested from the SRS document where none will be excluded for this project. Secondly, in Section 3 the approaches and techniques used for testing in this project will be stated. Thirdly, in Section 4 the use of test processes will be discussed including unit testing, integration testing, validation testing, and system testing. Fourthly, in Section 5 the process of reporting and correcting any errors, defects, or bugs found during testing will be stated. Fifthly, in Section 6 all test environments will be recorded including any resources necessary to do such testing including hardware, interfaces, and software. Lastly, in Section 7 all test cases will be documented including the test number, author(s), the date, revisions, test purpose, procedure, and the measure of success.

## **1.3 Definitions, Acronyms, and Abbreviations** {#1.3-definitions,-acronyms,-and-abbreviations}

| Acronym | Meaning |
| :---: | :---: |
| SRS | Software Requirements Specification |
| STP | Software Test Plan |

## **1.4 Document References** {#1.4-document-references}

| Document Title | Version | Date | Author(s) |
| :---: | :---: | :---: | :---: |
| Software Requirements Specification | 1.0 | January 24th, 2024 | Kylie Hall John Heinig Malik Hill Naheed John Yaro Kulchyckyj Isabella Stephens  Brittany Brenneman |
| STP Testing Tracking | 1.0 | 10/23/23 | Kylie Hall John Heinig Malik Hill Naheed John Yaro Kulchyckyj Isabella Stephens  Brittany Brenneman |

##  **1.5 System Overview** {#1.5-system-overview}

The Chesapeake Community Connection website serves as a hub for improving connections and knowledge exchange within the Chesapeake Community. Its core function is to encourage users to share their environmental stories in audiovisual formats; specifically, the website shall focus on community solutions and the current innovation involved in finding solutions to environmental conflicts.The platform features an accessible user interface accompanied with a designated page explaining the user interface and its capabilities, content submission capabilities, admin oversight for safety, a filtering system for efficient content discovery, and an interactive map system highlighting community-related locations. It ensures seamless access on both mobile and desktop devices through the Google Chrome browser, facilitating widespread community engagement and knowledge sharing.

# **2\. Requirements to be Tested** {#2.-requirements-to-be-tested}

The requirements tested in this document will include all requirements from the SRS document where none will be excluded from testing.  
                  

# **3\. Testing Approach** {#3.-testing-approach}

The requirements tested will be done using a combination of white box and black box testing. White box  
testing will test the internal workings and program logic of the software which is useful to verify input-output  
flow and the usability of the software. Black box testing will test for the validation of behavioral aspects of the  
software which is useful to validate the uncovered behavior or performance errors, interface errors, and errors  
in data structures. Both white box and black box testing approaches will be used complementary to each other  
in testing procedures.

# **4\. Test Process** {#4.-test-process}

Unit testing, integration testing, validation testing, and system testing will all be used within this STP. Unit  
testing will be written before the code is written to ensure the internal processing logic and data structures  
align with this predetermined test procedure. Unit testing will be performed on a personal laptop using Dell  
hardware with an 11th generation Intel i5 processor, 8.00 GB RAM, and \_\_\_ using Windows 11 Pro software  
on the St. Mary’s College of Maryland Campus. Integration testing will be used to bring together many aspects  
of internal logic to overall test a specific function. Integration testing will be performed on a personal laptop  
using Dell hardware using Windows 11 Pro Software on the St. Mary’s College of Maryland Campus. System testing will be used to test software in the environment it will be incorporated into during deployment and is based on system engineering.

# **5\. Reporting and Corrective Actions** {#5.-reporting-and-corrective-actions}

Within the STP Testing Tracking document, the process used to record errors (found during testing) is to mark the Pass/Fail column as FAIL. This will change the fill color of the respective test’s row to red allowing it to be more easily tracked. Additionally, there is a column designated for taking note of what happened instead of the expected result and a section for additional comments. As testing is being conducted, should issues arise they will be brought up during our team meetings by those that found the errors. After a test procedure passes the evaluation it will be marked as PASS under the Pass/Fail column \- changing the test row to green. 

# **6\. Test Environment** {#6.-test-environment}

The first testing environment focusing on unit, integration, and validation testing will be on a personal laptop  
using Dell hardware with an 11th generation 2.4 gigahertz Intel Core i5 processor, with 8.00 gigabytes RAM,  
and 235 gigabytes in storage size which uses Windows 11 Pro software. The location of testing on the personal  
Windows computer will be conducted in Schaefer Hall’s math lounge on the campus of St. Mary’s College of  
Maryland. Necessary interfaces needed to test in this environment include a trackpad or mouse and a keyboard.  
The second testing environment will be the system testing environment which includes an Acer monitor and a  
Dell desktop with an 11th generation Intel Core i7 processor, 8.00 gigabytes RAM and 256 gigabytes in  
storage size with Windows 11 software. The location of testing in the system testing environment will be  
conducted in room 160 in Schaefer Hall on the campus of St. Mary’s College of Maryland. Necessary  
interfaces needed to test in this environment include a mouse and keyboard.

# **7\. Test Procedures** {#7.-test-procedures}

A new Google Sheets document, called “[STP Testing Tracking](https://docs.google.com/spreadsheets/d/1cq4kdxZPHimY4N7v7Nw8LWtl3aS_fAO2/edit?usp=sharing&ouid=102831704549828776763&rtpof=true&sd=true)”,  shall be created (and saved in the team’s google drive under the STP document) to list all testing procedures and to track the testing process. The document shall take note of the following information in the form of separate columns: 

* Test \#: An ID number associated with the test. Composed of an abbreviation of the SRS heading test is associated with and a unique number to differentiate it from other tests.   
* SRS \#: The respective SRS requirement associated with the test.   
* Test Author: The name of the person who wrote the test.  
* Date: The date of when the test was written.   
* Test Evaluator: The name of the person conducting the test.  
* Evaluation Date: The date of when the test was evaluated.  
* Previous Evaluation Date: Should the test go through multiple versions, the date of when the test was previously evaluated.  
* Version Number: The version number of the test.  
* Test Purpose: A short description of the purpose of the test.  
* Test Procedures: A step by step process describing the steps needed to take place to properly evaluate the test.  
* Measure of Success: A short description of what a successful test should result in.  
* Pass/Fail: A section to denote is the test evaluation Passed or Failed  
* Failed Result: Short description of what happened instead of the expected result  
* Comment: Any additional comments/updates about the test.

Additionally the different columns within the STP Testing Tracking document have filter options allowing for easy sorting. 

# **8\.  Miscellaneous** {#8.-miscellaneous}

No miscellaneous information at this time.