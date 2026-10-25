![Image of Map Pin Logo](/Documentation/Sorted%20Documents%20(SP25)/SDD%20Images/Map-Pin-Icon.png)

|Chesapeake Community Connection Website - Software Design Description Version 1.1 - January 24th, 2024 - St. Mary’s College of Maryland Capstone |
|:---:|

_all images should be in except for the last diagram since it needs to be reuploaded since the original had no background and was very hard to read_

**Table of Contents**

[**1\. Introduction	3**](#1-introduction-1-introduction)

[1.1 Purpose	3](#11-purpose-11-purpose)

[1.2 Scope	3](#12-scope-12-scope)

[1.3 Definitions, Acronyms, and Abbreviations	3](#13-definitions-acronyms-and-abbreviations-13-definitions-acronyms-and-abbreviations)

[1.4 Document References	4](#14-document-references-14-document-references)

[1.5 System Overview	4](#15-system-overview-15-system-overview)

[**2\. Data Design	4**](#2-data-design-2-data-design)

[2.1 Internal Data Structures	5](#21-internal-data-structures-21-internal-data-structures)

[2.2 Data Flow Diagram	5](#22-data-flow-diagram-22-data-flow-diagram)

[**3\. Architecture Design	5**](#3-architecture-design-3-architecture-design)

[3.1 Program Structure	6](#31-program-structure-31-program-structure)

[**4\. Interface Design	6**](#4-interface-design-4-interface-design)

[4.1 Internal System Interfaces	6](#41-internal-system-interfaces-41-internal-system-interfaces)

[4.2 External System Interfaces	6](#42-external-system-interfaces-42-external-system-interfaces)

[4.3 User Interfaces	6](#43-user-interfaces-43-user-interfaces)

[4.3.1 Home Screen Display	6](#431-home-screen-display-431-home-screen-display)

[4.3.2 Contributor Page	7](#432-contributor-page-432-contributor-page)

[4.3.3 Login Display	9](#433-login-display-433-login-display)

[4.3.4 Sign Up Display	10](#434-sign-up-display--434-sign-up-display)

[4.3.5 Upload Submission Display	11](#435-upload-submission-display-435-upload-submission-display)

[4.3.6 Profile Management Display	12](#436-profile-management-display-436-profile-management-display)

[4.3.7 About Display	13](#437-about-display-437-about-display)

[4.3.8 Help & Tutorial Display	13](#438-help--tutorial-display-438-help--tutorial-display)

[4.3.9 Admin Page	14](#439-admin-page-439-admin-page)

[**5\. Procedural Design	15**](#5-procedural-design-5-procedural-design)

[5.1 Flowchart Reference Key	15](#51-flowchart-reference-key-51-flowchart-reference-key)

[**6\. Miscellaneous	16**](#6-miscellaneous-6-miscellaneous)

**Revision History**

| Date | Version | Description | Author(s) |
| :---: | :---: | :---: | :---: |
| October 11th, 2023 | 1.1  | Initial Draft  | Kylie Hall John Heinig Malik Hill Naheed John Yaro Kulchyckyj Isabella Stephens  Brittany Brenneman |
| January 24th, 2024 | 1.1 | Start of revisions for 2024 | Daniel Reina Alex Ochman Gavin McDonald John Heinig Kendahl Michael Shively  |

---

# **1\. Introduction** {#1.-introduction}

## **1.1 Purpose** {#1.1-purpose}

The purpose of the Software Design Description (SDD) is to provide a detailed description \- both internal and external \- of the Chesapeake Community Connection (CCC) Website via the use of visual diagrams and models. It consists of four distinct but interrelated activities: data design, architectural design, interface design, and procedural design. These activities are described as the following:

* **Data Design**: It shall provide an understanding of the data in the software and how it is stored. Attributes and relationships between data objects dictate the choice of data structures. The data design includes flow diagrams that illustrate how the data will be handled.   
* **Architectural Design**: It shall illustrate the overall structure of the CCC Website and map the information flow to the program structure. It shall serve as a blueprint for the overall application, illustrating what the CCC Website will look like when developed.   
* **Interface Design**: It shall describe the internal and external program interfaces. It shall capture the appearance and design of the interface the user shall use upon deployment of the CCC Website.   
* **Procedural Design**: It shall describe the internal logic of the CCC Website, including the graphical, tabular, and textual notations. It shall act as a blueprint for all of the software engineering work on the program where pseudocode will be the medium used to describe the full design of the software. 

## **1.2 Scope** {#1.2-scope}

This Software Design Description (SDD) shall closely relate to the development of the software. The final product shall follow and reflect the final version of this document.

The SDD contains the following sections

* Introduction  
* Data Design  
* Architecture Design   
* Interface Design  
* Procedural Design  
* Miscellaneous

## **1.3 Definitions, Acronyms, and Abbreviations** {#1.3-definitions,-acronyms,-and-abbreviations}

| Acronym | Meaning |
| :---: | :---: |
| SDD | Software Design Document |
| SDP | Software Development Plan |
| SRS | Software Requirements Specification |
| STP | Software Test Plan |
| TM | Traceability Matrix |
| WP | WordPress |

## 

## **1.4 Document References** {#1.4-document-references}

| Document Title | Version | Date | Author(s) |
| :---: | :---: | :---: | :---: |
| TBD | 1.0 | October 11, 2023 | Kylie Hall John Heinig Malik Hill Naheed John Yaro Kulchyckyj Isabella Stephens  |

## 

## **1.5 System Overview** {#1.5-system-overview}

The Chesapeake Community Connection website serves as a hub for improving connections and knowledge exchange within the Chesapeake Community. Its core function is to encourage users to share their environmental stories in audiovisual formats. The platform features an accessible user interface accompanied with a designated page explaining the user interface and its capabilities, content submission capabilities, admin oversight for safety, a filtering system for efficient content discovery, and an interactive map system highlighting community-related locations. It ensures seamless access on both mobile and desktop devices through the Google Chrome browser, facilitating widespread community engagement and knowledge sharing.

---

# **2\. Data Design** {#2.-data-design}

This section outlines all data structures to be implemented and how they should be implemented.

## **2.1 Internal Data Structures** {#2.1-internal-data-structures}

| Plugins | Description |
| :---- | :---- |
| WP Google Maps  | A plugin to allow for a customizable map using google maps |
| oneTap google sign in | Allows the user to sign in using their google account |

## **2.2 Data Flow Diagram** {#2.2-data-flow-diagram}

The Data flow diagram describes the relationship between hardware and software devices, and the information each will communicate between each other.  
![Diagram detailing relations between keyboard, mouse/touchscreen, server, and display](/Documentation/Sorted%20Documents%20(SP25)/SDD%20Images/Data-Flow-Diagram.png)

---

# **3\. Architecture Design** {#3.-architecture-design}

The architecture design outlines the hierarchy of the program, as well as indicating coupling relations between modules. 

## **3.1 Program Structure** {#3.1-program-structure}

![Diagram of pages on the website)](/Documentation/Sorted%20Documents%20(SP25)/SDD%20Images/Diagram-of-Pages-on-Site.png)

---

# **4\. Interface Design** {#4.-interface-design}

The interface designs contain internal, external, and user. These are used to expand the architectural model and to further depict visual and operational interfaces.  

## **4.1 Internal System Interfaces** {#4.1-internal-system-interfaces}

## **4.2 External System Interfaces** {#4.2-external-system-interfaces}

## **4.3 User Interfaces** {#4.3-user-interfaces}

The user interfaces are what the user will see upon entering the website.

### **4.3.1 Home Screen Display** {#4.3.1-home-screen-display}

- **Areas**:  
  - **Map**: Area where the user can access content. Contains a compass and a zoom-in/zoom-out option.  
  - **Header**: Area where the user can access the Contributor Page, the Tutorial & Help Page, and the About Page.  
  - **Filter**: Area where the user can filter content to appear on the map.  
  - **Bottom**: Area with news/current uploads displayed. Area where selected content information appears, including the audiovisual file, area, and description. 

![Mockup of Home Screen display](/Documentation/Sorted%20Documents%20(SP25)/SDD%20Images/Mockup-of-Map-Page.png)

### **4.3.2 Contributor Page** {#4.3.2-contributor-page}

- **Areas** : Before Log-In  
  - **Log-in & Sign Up**: Log-In/Sign Up options for contributors.  
  - **Description**: “What it means to be a contributor” section, describing what a contributor is and how to become one.  
  - **Links**: Area where the user can visit related contributors via links.   
- **Areas**: After Log-In  
  - **Logout**: An option that replaces the previous Log-In and Sign Up options.  
  - **Upload**: Option to upload content to the website (check if exclusive to members)  
  - **Profile Management**: Option to manage information regarding the user's account.  
  - **Description**  
  - **Links**  
- **Areas**: Contributor Search  
  - **Search Bar**: Searches via username.  
  - **Alphabetical Display**: There is a navigator at the top of the page that lets the user sort by alphabetical order.  
  - **Contributor**: Each contributor has their name and their mission statement displayed.

![Mockup of Contributor Page Before Log-in](/Documentation/Sorted%20Documents%20(SP25)/SDD%20Images/Mockup-of-Contributor-Page-Before-Login.png)  
![Mockup of Contributor Page While Logged In](/Documentation/Sorted%20Documents%20(SP25)/SDD%20Images/Mockup-of-Contributor-Logged-In-Page.png)  
![Mockup of Contributor Search](/Documentation/Sorted%20Documents%20(SP25)/SDD%20Images/Mockup-of-Contributor-Search-Page.png)

### **4.3.3 Login Display** {#4.3.3-login-display}

- **Areas**:  
  - **Login Username**: The user puts in their name.  
  - **Login Password**: The user puts in their password.  
  - **Login with Google**  
  - **Sign Up**: For users if they are not in the database.  
  - **Forgot Password**: Gives the option of resetting the user's password (if an individual) or getting in contact with an administrator (if an individual or organization).  
  - **Help & Tutorial Page Link**

![Mockup of Login page with username/password, Google sign-in, forgot password, Sign Up, and Help options](/Documentation/Sorted%20Documents%20(SP25)/SDD%20Images/Mockup-of-Contributor-Login-Page.png)

### **4.3.4 Sign Up Display**  {#4.3.4-sign-up-display}

- **Areas**:   
  - User Name  
  - Password  
  - Password Confirmation  
  - Email Address  
  - "What does it mean to be a Contributor?" Blurb

![Mockup of Account Creation Screen](/Documentation/Sorted%20Documents%20(SP25)/SDD%20Images/Mockup-of-Account-Creation-Page.png)

### **4.3.5 Upload Submission Display** {#4.3.5-upload-submission-display}

- **Areas**:  
  - **Title**: Area where the user can input the title for the content that they are uploading.  
  - **Author**: Text box that allows the user to input the Author of the content to be displayed with the content.  
  - **Location**: the location attributed to the content being uploaded, could take in an address or a set of coordinates. A set of coordinates are automatically assigned if not put in.  
  - **Content Description**: A short description of the content, to be displayed along with the title and author when searching.  
  - **Upload Files**: the area to upload files from a local device to be uploaded as the main body of the content. The user should be able to upload from file types .mp3/.mp4/.png/.jpg/.pdf.  
  - **Choose Categories**: a dropdown menu showing the available tags to assign to the content.

![Mockup of Upload Screen](/Documentation/Sorted%20Documents%20(SP25)/SDD%20Images/Mockup-of-Submit-Page.png)

### **4.3.6 Profile Management Display** {#4.3.6-profile-management-display}

- **Areas**:  
  - **User Information**: Information about the user that is already established in the system, such as their name, their password (censored by stars), their profile picture, their contact information, and their location (if they choose to show it).  
  - **Change Name**: A text box that allows the user to change their name.   
  - **Change Password**: Three text boxes that allow the user to change their password. The first text box requires the user to type in their old password. The other two require the user to type in their new password. All passwords are censored.   
  - **Change Profile Picture**: Upload a .png/.jpg image from the user’s device. Discards previous profile picture.   
  - **Change Contact Information**: Allows the user to change their email address or phone number.   
  - **List of Submissions**: List of the user’s submissions.

![Mockup of Profile Management Page](/Documentation/Sorted%20Documents%20(SP25)/SDD%20Images/Mockup-of-Account-Management-Page.png)

### **4.3.7 About Display** {#4.3.7-about-display}

- **Areas:**  
  - **About the Website**: Talks about its creation, purpose, etc.  
  - **About the Contributors**: Talks about the contributors (has a link to the contributor page at the bottom).

![Mockup of About Us Display](/Documentation/Sorted%20Documents%20(SP25)/SDD%20Images/Mockup-of-About-Us-Page.png)

### **4.3.8 Help & Tutorial Display** {#4.3.8-help-&-tutorial-display}

- **Areas**:  
  - **Frequently Asked Questions**: a showcase of questions we think a user might have   
  - **Map Tutorial**: A video explanation that demonstrates the use of filters and how to open pin descriptions.   
  - **Website Tutorial**: Tutorial about the basic features of the website.  
  - **Contact Information**

![Mockup of Help page containing FAQ, Map Tutorial, Website Tutorial, and Contact Information](/Documentation/Sorted%20Documents%20(SP25)/SDD%20Images/Mockup-of-FAQ-Page.png)

### **4.3.9 Admin Page** {#4.3.9-admin-page}

- **Areas**:  
  - **Admin User Request Page**: Area where user submissions appear. The admin can either approve or reject the user submissions.  
  - **Account Search**: Lists current users. The admin can search for a specific user either by email or username. Clicking on a user leads to a page similar to the user’s profile management display, but with the options to   
    - **Account Editing**: Admins are able to create, edit, and delete accounts of other users. 

![Mockup of Admin Page containing Pending Submissions and User List](/Documentation/Sorted%20Documents%20(SP25)/SDD%20Images/Mockup-of-Admin-Page.png)  
![Mockup of Admin Profile Management Page](/Documentation/Sorted%20Documents%20(SP25)/SDD%20Images/Mockup-of-Admin-Profile-Management-Page.png)

---

# **5\. Procedural Design** {#5.-procedural-design}

## **5.1 Flowchart Reference Key** {#5.1-flowchart-reference-key}

![Diagram of Pages and Interactions on Site](/Documentation/Sorted%20Documents%20(SP25)/SDD%20Images/Diagram-of-Pages-and-Interactions.png)


# **6\. Miscellaneous** {#6.-miscellaneous}

No miscellaneous items at this time. 
