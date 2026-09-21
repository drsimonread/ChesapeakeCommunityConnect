f 

**Greenwell Project** 

**Software Test Plan** 

**Version 2.0** 

**04/26/2023** 

**![][image1]**

**Greenwell QA** 

Caleb Jenkins 

Kylie Hall 

Yaro Kulchyckyj 

Matthew Grimelli  
**Table of Contents** 

**1\. Introduction 1** 1.1 Purpose 1 1.2 Scope 1 1.3 Definitions, Acronyms, and Abbreviations 1 1.4 Document References 1 1.5 System Overview 1 

**2\. Requirements to Be Tested 1** 2.1 Requirements List 2 2.2 Aspects List 3 2.3 Traceability Table 4 

**3\. Testing Approach 7** 3.1 White Box Testing 7 3.2 Black Box Testing 7 

**4\. Test Process 7** 4.1 Unit Testing 7 4.2 Integration Testing 7 4.3 Validation Testing 8 4.4 System Testing 8 

**5\. Reporting and Corrective Action 8 6\. Test Environment 8** 6.1 Unit Testing Environment 8 6.2 Integration Testing Environment 8 6.3 Validation Testing Environment 8 6.4 System Testing Environment 9 **7\. Test Procedures 9** 7.1 Requirements to be tested 9 7.2 POV of User 11 7.3 POV of Non-User 16 7.4 POV of Admin User 17 **8\. Miscellaneous 23**  
**Revision History**

| Date  | Version  | Description  | Author(s) |
| ----: | ----: | ----- | :---: |
| 10/24/2022  | 1.0  | First Draft | Aaron Guethlein, Caleb Jenkins |
| 04/26/2023  | 2.0  | Most recent Version | Caleb Jenkins, Kylie Hall, Yaro Kulchyckyj, Matthew Grimelli |

**1\. Introduction** 

**1.1 Purpose** 

The purpose of this document is to provide tests for the development of the Greenwell file share website. This document will formally state the procedures to be used for testing the software product and identify specific test cases. It will provide all testing processes, approaches, environments, and procedures that will be performed for each requirement to be tested. 

**1.2 Scope** 

The scope of this document is to thoroughly list the tests from the points of view of a non-user, standard user, and admin users. There will also be tests with multiple users, multiple user actions simultaneously on the same page, and multiple log-ins from the same account. 

**1.3 Definitions, Acronyms, and Abbreviations** 

| SRS  | Software Requirement Specification |
| :---- | :---- |
| SDD  | Software Design Description |

**1.4 Document References** 

This section is not currently applicable. 

**1.5 System Overview** 

This system will be an internet hosted database used by board members and trustees of the Greenwell Foundation. The intended use of this database is to replace their current content distribution and organization system with a centralized, proprietary solution. To accomplish this, the website must facilitate the uploading and downloading of documents, videos and photos. The website must also have an intuitive method of version control and segmenting of different types of content. 

**2\. Requirements to Be Tested** 

The purpose of this Traceability Matrix is to clearly state the relationship between requirements from the SRS, in terms of the database filemanager, and design artifacts from the SDD through cross-references for the purpose of allowing access to how an activity relates to a requirement 

at any point in development and to ensure that no requirements have failed to be represented in the design process. The Traceability Matrix also ensures there are no design aspects that do not satisfy a requirement. It contains a list with every requirement numbered, another list with  
every aspect numbered, and a traceability table with the list of requirements crossed with the list of aspects. In this table, boxes are marked with an ‘X’ where an aspect meets a requirement. 

**2.1 Requirements List**

| Requirement Number  | SRS Section  Number | SRS Section Title |
| ----- | ----- | :---: |
| R1  | 2.1.1  | ADA Compliant |
| R2  | 2.2.1  | Login Page |
| R3  | 2.2.2  | Startup to Login |
| R4  | 2.2.3  | Registering Users |
| R5  | 2.2.4  | Form Requirements |
| R6  | 2.2.5  | Username/Email for Login |
| R7  | 2.2.6  | Password for Login |
| R8  | 2.2.7  | Incorrect Login |
| R9  | 2.2.8  | Login Page Redirect |
| R10  | 2.3.1  | Main Screen Readability |
| R11  | 2.3.2  | Main Screen Tabs/Links |
| R12  | 2.3.3  | Return to Main Screen |
| R13  | 2.3.4  | Logout Option |
| R14  | 2.3.5  | Logout Tab |
| R15  | 2.3.6  | Buttons |
| R16  | 2.3.7  | Entering Text |
| R17  | 2.3.8  | Logo |
| R18  | 2.4.1  | Files |
| R19  | 2.4.2  | File/Folder Filter |
| R20  | 2.4.3  | Folders |
| R21  | 2.4.4  | Version Control |
| R22  | 2.4.5  | Picture Storage |

| Requirement Number  | SRS Section  Number | SRS Section Title |
| ----- | ----- | :---: |
| R23  | 2.4.6  | Video Storage |
| R24  | 2.4.7  | Working and Programs Folder |
| R25  | 2.5.1  | Access to Important Data |
| R26  | 2.5.2  | Adding Files |
| R27  | 2.5.3  | Removing Files |
| R28  | 2.5.4  | Admin Permissions |
| R29  | 2.5.5  | Restricted Access |
| R30  | 2.6.1  | Allowing only Employees to the Page |
| R31  | 2.6.2  | Employee Login Page |
| R32  | 2.6.3  | Two-Factor Authentication |

**2.2 Aspects List**

| Aspect Number  | Aspect (Subsystem) Description |
| :---: | :---: |
| A1  | Font Size: 20 Pixels |
| A2  | Font Style: Arial, San Serif, Calibri |
| A3  | Spacing Compliance |
| A4  | Emphasis Compliance |
| A5  | Color Guidelines |
| A6  | Display Username/Password Input |
| A7  | Accept Username/Email Input |
| A8  A9  A10  | Accept Password Input  Allow Administrator Permissions  Allow Foundation Member Permissions |
| A11  | Allow Pending User Permissions |

| A12  | Display Non-User Permissions |
| :---: | :---: |
| A13  | Display Page Directory Commands |
| A14  | Allow Page Directory Commands |
| A15  | Display Filter Option for Files |
| A16  | Allows Filter input for File Sorting |
| A17  | Allow Removal of Files |
| A18  | Allow download of Files |
| A19  | Display Main Screen Tabs |
| A20  | Display Main Screen Folders |
| A21  | Allow Access to Open Main Screen Folders |
| A22  | Display Two Factor Authentication |
| A23  | Allow Two Factor Authentication Input |
| A24  | Allow Reset of Password |
| A25  | Display Registration Form to Create Account |
| A26  | Accept Registration Form Input |
| A27  | Allow Logout Input Through One-Click Button |
| A28  | Display Logo |
| A29  | Allow Upload of Files |

**2.3 Traceability Table**

|  | A  1 | A  2 | A  3 | A  4 | A  5 | A  6 | A  7 | A  8 | A  9 | A  1  0 | A  1  1 | A  1  2 | A  1  3 | A  1  4 | A  1  5 | A  1  6 | A  1  7 | A  1  8 | A  1  9 | A  2  0 | A  2  1 | A  2  2 | A  2  3 | A  2  4 | A  2  5 | A  2  6 | A  2  7 | A  2  8 | A  2  9 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| R  1 | **X**  | **X**  | **X**  | **X**  | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| R  2 |  |  |  |  |  | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

|  | A 1 | A 2 | A 3 | A 4 | A 5 | A 6 | A 7 | A 8 | A 9 | A 1 0 | A 1 1 | A 1 2 | A 1 3 | A 1 4 | A 1 5 | A 1 6 | A 1 7 | A 1 8 | A 1 9 | A 2 0 | A 2 1 | A 2 2 | A 2 3 | A 2 4 | A 2 5 | A 2 6 | A 2 7 | A 2 8 | A 2 9 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| R 3 |  |  |  |  |  |  |  |  |  |  |  | **X** | **X** | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| R 4 |  |  |  |  |  | **X** | **X** | **X** |  |  | **X** |  | **X** | **X** |  |  |  |  |  |  |  |  |  |  | **X** | **X** |  |  |  |
| R 5 |  |  |  |  |  | **X** | **X** | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** | **X** |  |  |  |
| R 6 |  |  |  |  |  | **X** | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| R 7 |  |  |  |  |  |  |  | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| R 8 |  |  |  |  |  |  |  |  |  |  |  | **X** |  |  |  |  |  |  |  |  |  |  |  | **X** |  |  |  |  |  |
| R 9 |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| R  10 | **X** | **X** | **X** | **X** | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| R 11 |  |  |  |  |  |  |  |  |  |  |  |  | **X** | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| R  12 |  |  |  |  |  |  |  |  |  |  |  |  | **X** | **X** |  |  |  |  | **X** |  |  |  |  |  |  |  |  |  |  |
| R  13 |  |  |  |  |  | **X** |  |  |  |  |  |  | **X** | **X** |  |  |  |  |  |  |  |  |  |  |  |  | **X** |  |  |
| R  14 |  |  |  |  |  | **X** |  |  |  |  |  |  |  |  |  |  |  |  | **X** |  |  |  |  |  |  |  | **X** |  |  |
| R  15 | **X** | **X** | **X** | **X** | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| R  16 | **X** | **X** | **X** | **X** | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| R  17 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** |  |

|  | A 1 | A 2 | A 3 | A 4 | A 5 | A 6 | A 7 | A 8 | A 9 | A 1 0 | A 1 1 | A 1 2 | A 1 3 | A 1 4 | A 1 5 | A 1 6 | A 1 7 | A 1 8 | A 1 9 | A 2 0 | A 2 1 | A 2 2 | A 2 3 | A 2 4 | A 2 5 | A 2 6 | A 2 7 | A 2 8 | A 2 9 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| R  18 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** | **X** |  |  |  |  |  |  |  |  |  |  |  |
| R  19 |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** | **X** |  |  |  |  | **X** |  |  |  |  |  |  |  |  |
| R  20 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** | **X** |  |  |  |  |  |  |  |  |
| R  21 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** | **X** |  | **X** | **X** |  |  |  |  |  |  |  |  |
| R  22 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** | **X** |  |  |  |  |  |  |  |  |
| R  23 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** | **X** |  | **X** | **X** |  |  |  |  |  |  |  |  |
| R  24 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** |  |  |  |  |  |  |  |  |  |
| R  25 |  |  |  |  |  |  |  |  | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| R  26 |  |  |  |  |  |  |  |  | **X** | **X** |  |  |  |  |  |  | **X** |  |  |  |  |  |  |  |  |  |  |  | **X** |
| R  27 |  |  |  |  |  |  |  |  | **X** |  |  |  |  |  |  |  | **X** |  |  |  |  |  |  |  |  |  |  |  |  |
| R  28 |  |  |  |  |  |  |  |  | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| R  29 |  |  |  |  |  |  |  |  | **X** | **X** | **X** | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| R  30 |  |  |  |  |  |  |  |  | **X** | **X** | **X** | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| R  31 |  |  |  |  |  | **X** | **X** | **X** |  |  |  |  | **X** | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| R  32 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** | **X** |  |  |  |  |  |  |

**3\. Testing Approach** 

**3.1 White Box Testing** 

White box testing is largely concerned with the logic and internal functions of the software. It will largely be important for the boundaries and limitations of the software, such as character limits for user name lengths. Our white box testing will be most commonly used in relation to less strictly guided user input, such as input through text boxes. 

**3.2 Black Box Testing** 

Black box testing, as it is what is mainly concerned with what is visible (the output), will be what is most important to our customer. The Greenwell File Share system is a file sharing system in which files are the content; as a result, it will be our first priority in testing. 

**4\. Test Process** 

**4.1 Unit Testing** 

Unit testing will occur intermittently as new, independently functional aspects of the software become complete. The importance of unit testing is assuring that these aspects work alone, and without consideration for other factors, so the testing will occur on a few various systems, such as team members’ personal computers. 

**4.2 Integration Testing** 

Integration testing occurs towards the end of most other tests. Once features are proven to work individually, they will be combined into larger, more expansive tests to assure the correct operation of the file share system in a more realistic fashion. Integration tests have been included as a part of our test procedures, and will be completely both implicitly and explicitly, as the software will contain plenty of separate frames which the user will navigate between (i.e. from a log-in screen to the main file share page, etc.). 

**4.3 Validation Testing** 

Validation testing will be concerned with ensuring that the software meets the requirements requested by the user. As such, a test should exist for each requirement.  
**4.4 System Testing** 

When the software is at the point where it is ready for system testing, it should be near completion. There should be a few preliminary tests while the software is early in development, alongside the unit tests, to ensure that the program’s functionality will not be disrupted by the final version it will appear on. This system will be a file share system. 

**5\. Reporting and Corrective Action** 

The team members, if they find nonmajor issues with the program, may directly notify each other member in Discord Greenwell team group chat. This group chat is a dynamic, mobile based platform, and may be directly accessed over online platforms. For more serious issues, the team should relay information directly to their team and project leads. 

**6\. Test Environment** 

**6.1 Unit Testing Environment** 

The unit testing will be performed on both the development website and wordpress to maximize efficiency of testing the website. 

**6.2 Integration Testing Environment** 

The integration tests will be performed on the coding hardware in the IDE software to maximize the efficiency of creating and implementing stubs and drivers. Tests of high abstraction (defined by complete usability by an outside tester) will be tested outside of the IDE by non-developers. 

**6.3 Validation Testing Environment** 

Most necessary for validation testing is the team’s copy of the System Requirements Specification document to ensure all aspects of the software match the requirements. A deficiency list will need to be created to map where the software strays from specifications. 

**6.4 System Testing Environment** 

System testing will be completed in the Greenwell teams' meeting location: Schaefer 132\. 

Caleb Jenkins: Windows 10, AMD Ryzen 9 5900HS with Radeon Graphics 3.30 GHz, RTX 3060H 6 GB, 16.00 GB Ram. 

Kylie Hall: MacBook Pro (2019),Intel UHD Graphics 630 1536 MB, 6-Core Intel Core i7 2.6 GHz, 16.00 GB RAM  
Matthew Grimelli: Windows 11, Intel i5-11300h with intel Iris(R) Xe @3.1GHz, 16.00 GB RAM 

**7\. Test Procedures** 

**7.1 Requirements to be tested**

| SRS  Requirement  Section | SRS Requirement Title  | Test Status  | Test Number(s) |
| ----- | ----- | ----- | :---: |
| 2.1.1  | ADA Compliant  | PASS  | N/A |
| 2.2.1  | Login Page  | PASS  | PU-001, PAU-001 |
| 2.2.2  | Startup to Login  | PASS  | PU-001, PAU-001 |
| 2.2.3  | Registering Users  | PASS  | PU-002, PU-008, PAU-010 |
| 2.2.4  | Form Requirements  | PASS  | PU-002 |
| 2.2.5  | Username/Email for Login  | PASS  | PU-001, PNU-001 |
| 2.2.6  | Password for Login  | PASS  | PU-001, PNU-001 |
| 2.2.7  | Incorrect Login  | PASS  | PU-009 |
| 2.2.8  | Login Page Redirect  | PASS  | PNU-002 |
| 2.3.1  | Main Screen Readability  | PASS  | N/A |
| 2.3.2  | Main Screen Tabs/Links  | PASS  | PU-011 |
| 2.3.3  | Return to Main Screen  | PASS  | PU-010 |
| 2.3.4  | Logout Option  | PASS  | PU-006 |
| 2.3.5  | Logout Tab  | PASS  | PU-006 |
| 2.3.6  | Buttons  | PASS  | PU-012 |
| 2.3.7  | Entering Text  | PASS  | PU-014 |
| 2.3.8  | Logo  | PASS  | PU-016 |

| SRS  Requirement  Section | SRS Requirement Title  | Test Status  | Test Number(s) |
| ----- | ----- | ----- | :---: |
| 2.4.1  | Files  | PASS  | PU-004 |
| 2.4.2  | File/Folder Filter  | PASS  | PAU-004 |
| 2.4.3  | Folders  | PASS  | PAU-005 |
| 2.4.4  | Version Control  | PASS  | PU-015 |
| 2.4.5  | Picture Storage  | PASS  | PU-007 |
| 2.4.6  | Video Storage  | PASS  | PAU-009 |
| 2.4.7  | Working and Programs Folder  | PASS  | PU-013 |
| 2.5.1  | Access to Important Data  | PASS  | PAU-011 |
| 2.5.2  | Adding Files  | PASS  | PU-004 |
| 2.5.3  | Removing Files  | PASS  | PAU-006, PU-017 |
| 2.5.4  | Admin Permissions  | PASS  | PAU-007 |
| 2.5.5  | Restricted Access  | PASS  | PAU-008 |
| 2.6.1  | Allowing only Employees to the Page  | PASS  | PNU-001 |
| 2.6.2  | Employee Login Page  | PASS  | PU-001 |
| 2.6.4  | Creating Events on Calendar  | PASS  | PAU-12 |
| 2.6.5  | Delete Event on Calendar  | PASS  | PAU-13 |

**7.2 POV of User** 

**\<\>...................................................................................................................................\<\> Test Number: PU-001 PASS** 

**Author:** Aaron Guethlein 

**Date:** 10/31/22 

**Revision:** 1.0 

**Test Purpose:** Ensure the User can log-in to file share 

**Test Procedures:** 

1\. Navigate on the home page to log-in page 

2\. Input a working access code  
**Measure of Success:** A successful log-in and the ability to see the file share system. 

**\<\>...................................................................................................................................\<\> Test Number: PU-002 PASS** 

**Author:** Aaron Guethlein 

**Date:** 10/31/22 

**Revision:** 1.0 

**Test Purpose:** Reset code 

**Test Procedures:** 

1\. Navigate from the home page to log-in page 

2\. Input a non-working access code 

3\. Fill out a form to be sent to the admin 

**Measure of Success:** A successful test is when a message is sent to the admin. **\<\>...................................................................................................................................\<\> Test Number: PU-003 PASS** 

**Author:** Caleb Jenkins 

**Date:** 11/14/22 

**Revision:** 1.0 

**Test Purpose:** Return to main screen 

**Test Procedures:** 

1\. Navigate from the home page to log-in page 

2\. Input a working access code 

3\. Click on Greenwell logo to return to main site 

**Measure of Success:** A successful test is when the user returns to the main page. 

**\<\>...................................................................................................................................\<\> Test Number: PU-004 PASS** 

**Author:** Aaron Guethlein 

**Date:** 11/14/22 

**Revision:** 1.0 

**Test Purpose:** Ensure the User can upload to file share 

**Test Procedures:** 

1\. Navigate on the home page to log-in page 

2\. Input a working access code 

3\. Navigate to “upload file” folder 

4\. Upload a file of 10 mb or less  
**Measure of Success:** A success is if the admin is able to see the upload file. **\<\>...................................................................................................................................\<\> Test Number: PU-005 PASS** 

**Author:** Aaron Guethlein 

**Date:** 11/14/22 

**Revision:** 1.0 

**Test Purpose:** Ensure the User can download from file share 

**Test Procedures:** 

1\. Navigate on the home page to log-in page 

2\. Input a working access code 

3\. Navigate to “Photos” folder 

4\. Download the first photo in the folder 

**Measure of Success:** A success is if the user is able to download the file. **\<\>...................................................................................................................................\<\> Test Number: PU-006 PASS** 

**Author:** Caleb Jenkins 

**Date:** 11/14/22 

**Revision:** 1.0 

**Test Purpose:** Ensure the user can log out of the file-share 

**Test Procedures:** 

1\. Navigate from the home page to log-in page 

2\. Input a working access code 

3\. Click logout button 

**Measure of Success:** A successful test is when the user returns to the main page. 

**\<\>...................................................................................................................................\<\> Test Number: PU-007 PASS** 

**Author:** Aaron Guethlein 

**Date:** 11/14/22 

**Revision:** 1.0 

**Test Purpose:** Ensure pictures can be seen before downloading 

**Test Procedures:** 

1\. Navigate from the home page to log-in page 

2\. Input a working access code 

3\. Click logout button 

4\. Navigate to “Photos” folder  
5\. Click on the first photo in the “Photo” folder 

**Measure of Success:** A successful test is when a window showing the photo before being downloaded is seen. 

**\<\>...................................................................................................................................\<\> Test Number: PU-008 PASS** 

**Author:** Caleb Jenkins 

**Date:** 11/14/22 

**Revision:** 1.0 

**Test Purpose:** Register a New User 

**Test Procedures:** 

1\. Navigate from the home page to log-in page 

2\. Click “Registration” 

3\. Fill form 

4\. Click “Register” 

5\. Inform Admin to change user role 

**Measure of Success:** A successful test is when a new user account is created **\<\>...................................................................................................................................\<\> Test Number: PU-009 PASS** 

**Author:** Matthew Grimelli 

**Date:** 4/3/2023 

**Revision:** 2.0 

**Test Purpose:** Ensure User can recover password 

**Test Procedures:** 

1\. Navigate to log-in page 

2\. Click “Lost your password?” 

3\. Enter Username/ Email 

4\. Click “Get new Password” 

5\. Follow email directions 

6\. Login with new password 

**Measure of Success:** User can reset password and login with it. 

**\<\>...................................................................................................................................\<\> Test Number: PU-010** 

**Author:** Matthew Grimelli 

**Date:** 4/17/2023 

**Revision:** 2.0 

**Test Purpose:** Ensure User can navigate back to main screen 

**Test Procedures:**  
1\. Access webpage 

2\. Navigate to subpage 

3\. Navigate back to main webpage using only buttons on the webpage 4\. Repeat for each subpage 

**Measure of Success:** User can navigate back to main screen using only navigation bar and buttons on webpage 

**\<\>...................................................................................................................................\<\> Test Number: PU-011** 

**Author:** Kylie Hall 

**Date:** 4/17/23 

**Revision:** 2.0 

**Test Purpose:** Allow navigation to open folders in one left click. 

**Test Procedures:** 

1\. Navigate from the home page to log-in page 

2\. Input a working access code 

3\. Navigate to the “Shared Files” section of the main page. 

4\. Left-click once on the folder “Board Assessments” 

**Measure of Success:** Folder is opened to see folders and files within it. **\<\>...................................................................................................................................\<\> Test Number: PU-012** 

**Author:** Matthew Grimelli 

**Date:** 4/17/2023 

**Revision:** 2.0 

**Test Purpose:** Ensure User can access and read buttons with a mouse **Test Procedures:** 

1\. Navigate to main page using default browser formatting options 2\. Read each button 

3\. Click on each button with mouse 

**Measure of Success:** User can read and use buttons with a mouse **\<\>...................................................................................................................................\<\> Test Number: PU-013** 

**Author:** Kylie Hall 

**Date:** 4/17/23 

**Revision:** 2.0 

**Test Purpose:** Allow navigation to open folders in one left click. 

**Test Procedures:**  
1\. Navigate from the home page to log-in page 

2\. Input a working access code 

3\. Navigate to the “Shared Files” section of the main page. 

4\. Navigate to two default folders titled “working” and “programs” 

**Measure of Success:** Folders “working” and “programs” exist. 

**\<\>...................................................................................................................................\<\> Test Number: PU-014** 

**Author:** Matthew Grimelli 

**Date:** 4/17/23 

**Revision:** 2.0 

**Test Purpose:** Ensure the user can easily input text to text areas 

**Test Procedures:** 

1\. Navigate to login page 

2\. Check that text-entry boxes are clear and easily read 

3\. Click on the “Register” link 

4\. Check that text-entry boxes are clear and easily read 

5\. Back out to login page 

6\. Click on “Lost your password?” link 

7\. Check that text-entry boxes are clear and easily read 

**Measure of Success:** All text-entry boxes are clear and easily read **\<\>..................................................................................................................................\<\> Test Number: PU-015** 

**Author:** Kylie Hall 

**Date:** 4/17/23 

**Revision:** 2.0 

**Test Purpose:** Maintain version control 

**Test Procedures:** 

1\. Navigate from the home page to log-in page 

2\. Input a working access code 

3\. On “Shared Files” page select the “Board Meeting Materials” folder 

**Measure of Success:** If the permissions and modified dates are visible. **\<\>...................................................................................................................................\<\> Test Number: PU-016** 

**Author:** Kylie Hall 

**Date:** 4/24/23  
**Revision:** 2.0 

**Test Purpose:** Logo Redirection 

**Test Procedures:** 

1\. Navigate from the home page to log-in page 

2\. Left-click on the greenwell logo in the top left corner of the screen. 

**Measure of Success:** If the user is redirected to the home page of the website. **\<\>...................................................................................................................................\<\> Test Number: PU-017** 

**Author:** Kylie Hall 

**Date:** 4/17/2023 

**Revision:** 2.0 

**Test Purpose:** Ensure only Administrator can delete files. 

**Test Procedures:** 

1\. Navigate from the home page to log-in page 

2\. Input a working access code 

3\. Navigate to the working folders/files 

4\. Access the specific files 

5\. Attempt to delete file 

**Measure of Success:** If user is unsuccessful at deleting file. 

**7.3 POV of Non-User** 

**\<\>...................................................................................................................................\<\> Test Number: PNU-001 PASS** 

**Author:** Aaron Guethlein 

**Date:** 10/31/22 

**Revision:** 1.0 

**Test Purpose:** Ensure non-users cannot log-in 

**Test Procedures:** 

1\. Navigate from the home page to log-in page 

2\. Input a non-working access code 

**Measure of Success:** A successful test is when the non-user can not enter the file share page. 

**\<\>...................................................................................................................................\<\> Test Number: PNU-002**  
**Author:** Kylie Hall 

**Date:** 4/17/2023 

**Revision:** 2.0 

**Test Purpose:** Ensure non-user is directed to login page at upon refresh of web page. 

**Test Procedures:** 

1\. Navigate to home page 

2\. Click the refresh button on browser 

**Measure of Success:** Displayed on monitor is the login page. 

**\<\>...................................................................................................................................\<\>** 

**7.4 POV of Admin User** 

**\<\>...................................................................................................................................\<\> Test Number: PAU-001 PASS** 

**Author:** Aaron Guethlein 

**Date:** 10/31/22 

**Revision:** 1.0 

**Test Purpose:** Ensure Admin can log in. 

**Test Procedures:** 

1.Navigate from the home page to log-in page 

2.Input a working access code 

3.See File Share webpage 

**Measure of Success:** A successful login and the ability to access the file share system. 

**\<\>...................................................................................................................................\<\> Test Number: PAU-002 PASS** 

**Author:** Aaron Guethlein 

**Date:** 10/31/22 

**Revision:** 1.0 

**Test Purpose:** Ensure the user cannot log in if password is incorrect **Test Procedures:** 

1.Navigate from the home page to log-in page 

2.Input a non-working access code 

3.Receive a message to re-enter password  
**Measure of Success:** A successful message is sent to the user if they incorrectly input the wrong password. 

**\<\>...................................................................................................................................\<\> Test Number: PAU-003 PASS** 

**Author:** Caleb Jenkins 

**Date:** 11/14/22 

**Revision:** 1.0 

**Test Purpose:** Return to main screen 

**Test Procedures:** 

1\. Navigate from the home page to log-in page 

2\. Input a working access code 

3\. Click on Greenwell logo to return to main site 

**Measure of Success:** A successful test is when the admin returns to the main page. 

**\<\>...................................................................................................................................\<\> Test Number: PAU-004 PASS** 

**Author:** Cole Doherty 

**Date:** 11/14/22 

**Revision:** 1.0 

**Test Purpose:** File/Folder Filter 

**Test Procedures:** 

1.Navigate from the home page to log-in page 

2.Input a working access code 

3.Navigate to the working folders/files 

4.Sort by alphabetical order, date, and keyword search across all folders 

**Measure of Success:** A successful test is when the admin is able to filter different folders. 

**\<\>...................................................................................................................................\<\> Test Number: PAU-005 PASS** 

**Author:** Cole Doherty 

**Date:** 11/14/22 

**Revision:** 1.0 

**Test Purpose:** Folders 

**Test Procedures:** 

1.Navigate from the home page to log-in page 

2.Input a working access code 

3.Navigate to a working folder  
4.Ensure that the folder can hold files 

**Measure of Success:** A successful test is when the admin is able to see different folders with files included within them. 

**\<\>...................................................................................................................................\<\>** 

**Test Number: PAU-006 PASS** 

**Author:** Naheed John 

**Date:** 11/14/22 

**Revision:** 1.0 

**Test Purpose:** Administrator Deleting Files 

**Test Procedures:** 

1\. Navigate from the home page to log-in page 

2\. Input a working access code 

3\. Navigate to the working folders/files 

4\. Access the specific files 

5\. Delete a file 

**Measure of Success:** Only the administrator(s) is allowed to remove files, users or non users are not granted this access. 

**\<\>...................................................................................................................................\<\>** 

**Test Number: PAU-007 PASS** 

**Author:** Caleb Jenkins 

**Date:** 11/14/22 

**Revision:** 1.0 

**Test Purpose:** Admin Permissions 

**Test Procedures:** 

1\. Navigate to wordpress website 

2\. Login using admin credentials 

3\. Navigate to Users sidebar button 

4\. Select “User you wish to edit” 

5\. Click “role” dropdown menu 

6\. Choose appropriate role 

7\. Click “Update User” 

**Measure of Success:** A successful test is when the admin is able to change an existing user account into an admin account  
**\<\>...................................................................................................................................\<\>** 

**Test Number: PAU-008 PASS** 

**Author:** Kylie Hall 

**Date:** 04/24/2023 

**Revision:** 2.0 

**Test Purpose:** Restricted Permissions 

**Test Procedures:** 

1\. Navigate from the home page to log-in page 

2\. Input a working access code 

3\. Hover over the button “Greenwell Foundation” with the mouse 

4\. Left-click on “Dashboard” 

5\. On the left column left-click on “WP File Manager” 

6\. Below “WP File Manager” left-click on the “Settings” button 

7\. Left-click on “User Role Restrictions” 

8\. Change the first block where the first drop down menu selects 

“Administrator” 

9\. On the multiple select options select “Rename” as the only option. 10.Left-click on the “Greenwell foundation visit site” in top left corner of screen 

11\. Navigate from the home page to log-in page 

12.Input a working access code 

13.Rename a file 

**Measure of Success:** If the administrator is allowed to rename a file. **\<\>...................................................................................................................................\<\> Test Number: PAU-009 PASS** 

**Author:** Cole Doherty 

**Date:** 11/14/22 

**Revision:** 1.0 

**Test Purpose:** Video Storage 

**Test Procedures:** 

1.Navigate from the home page to log-in page 

2.Input a working access code 

3.Navigate to the videos folder 

4.Drop a video within the specific video folder 

5\. A file no larger than 10mb should be able to be added to the folder 6.If a file is larger than 10mb then a message will be displayed saying the file is too large.  
**Measure of Success:** A successful test is when the admin is able to drop videos into the video folder. 

**\<\>...................................................................................................................................\<\> Test Number: PAU-010 PASS** 

**Author:** Caleb Jenkins 

**Date:** 11/14/22 

**Revision:** 1.0 

**Test Purpose:** Register New User 

**Test Procedures:** 

1\. Navigate to wordpress website 

2\. Login using admin credentials 

3\. Navigate to Users sidebar button 

4\. Click “Add new” 

5\. Fill out form 

6\. Verify that role is correct 

7\. Click “Add new user” 

**Measure of Success:** A successful test is when a new user account is created **\<\>...................................................................................................................................\<\> Test Number: PAU-011** 

**Author:** Kylie Hall 

**Date:** 4/17/23 

**Revision:** 2.0 

**Test Purpose:** Maintain administrator read permissions 

**Test Procedures:** 

1\. Navigate from the home page to log-in page 

2\. Input a working access code 

3\. On “Shared Files” page select the “Board Meeting Materials” folder 

**Measure of Success:** If the read and write permissions are available **\<\>...................................................................................................................................\<\> Test Number: PAU-012** 

**Author:** Kylie Hall 

**Date:** 4/19/23 

**Revision:** 2.0 

**Test Purpose:** To ensure events can be made on the timely calendar. **Test Procedures:** 

1\. Navigate from the home page to log-in page  
2\. Input a working access code 

3\. Navigate to Wordpress dashboard 

4\. Click on timely plugin on left hand sidebar 

5\. Login if necessary 

6\. Click top right “Add event” button 

7\. Edit details 

8\. Click publish on bottom of the right sidebar 

**Measure of Success:** If the event is visible on the calendar 

**\<\>...................................................................................................................................\<\> Test Number: PAU-013** 

**Author:** Kylie Hall 

**Date:** 4/19/23 

**Revision:** 2.0 

**Test Purpose:** To Ensure events can be deleted on the timely calendar **Test Procedures:** 

1\. Navigate from the home page to log-in page 

2\. Input a working access code 

3\. Navigate to wordpress dashboard 

4\. Click timely plugin on left sidebar 

5\. Login if necessary 

6\. Navigate to pertinent event 

7\. Click “read more” on the event 

8\. Select the trash button within the event 

**Measure of Success:** If the event is no longer visible on the calendar 

**8\. Miscellaneous** 

This section is not currently applicable.

[image1]: <data:image/png;base64,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>