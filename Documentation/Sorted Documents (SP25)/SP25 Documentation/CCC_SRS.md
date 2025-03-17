

|  Chesapeake Community Connection Website Software Requirements Specification Version 1.2 February 24th, 2025 St. Mary’s College of Maryland Capstone Kylie Hall John Heinig Malik Hill Naheed John Yaro Kulchyckyj Isabella Stephens Brittany Brenneman  |
| :---: |

**Table of Contents**

[1\.  Introduction	5](#1.-introduction)

[1.1 Purpose	5](#1.1-purpose)

[1.2 Scope	5](#1.2-scope)

[1.3 Definitions, Acronyms, and Abbreviations	6](#1.3-definitions,-acronyms,-and-abbreviations)

[1.4 Document References	6](#1.4-document-references)

[1.5 System Overview	6](#1.5-system-overview)

[2\. Functional Description	7](#2.-functional-description)

[2.1 Website Display	7](#2.1-website-display)

[2.1.1   Homepage	7](#2.1.1-homepage)

[2.1.1.1  World Map Outline	7](#2.1.1.1-world-map-outline)

[2.1.1.2  World Map Filter	7](#2.1.1.2-world-map-filter)

[2.1.1.3  World Map Scope	7](#2.1.1.3-world-map-scope)

[2.1.1.4  Map Pins	7](#2.1.1.4-map-pins)

[2.1.1.5  Map Pin Color	7](#2.1.1.5-map-pin-color)

[2.1.1.6  Descriptive Info	7](#2.1.1.6-descriptive-info)

[2.1.1.7  Full Screen Option	7](#2.1.1.7-full-screen-option)

[2.1.1.8   Logo Display	7](#2.1.1.8-logo-display)

[2.1.2    Contributor Page Display	7](#2.1.2-contributor-page-display)

[2.1.2.1  Contributor Login Button	7](#2.1.2.1-contributor-login-button)

[2.1.2.2  Contributor Sign up Button	8](#2.1.2.2-contributor-sign-up-button)

[2.1.2.3  Contributor Search Alphabet Display	8](#2.1.2.3-contributor-search-alphabet-display)

[2.1.2.4  Contributor Search Bar Display	8](#2.1.2.4-contributor-search-bar-display)

[2.1.2.5  Contributor List	8](#2.1.2.5-contributor-list)

[2.1.2.6 View More Button	8](#2.1.2.6-view-more-button)

[2.1.3    Help/Tutorial Page	8](#2.1.3-help/tutorial-page)

[2.1.3.1 Frequently Asked Questions	8](#2.1.3.1-frequently-asked-questions)

[2.1.3.2 Map Animation	8](#2.1.3.2-map-animation)

[2.1.3.3 Tutorial Explaining how to use website	8](#2.1.3.3-tutorial-explaining-how-to-use-website)

[2.1.3.4   Logo Display	8](#2.1.3.4-logo-display)

[2.1.4    About Page Display	9](#2.1.4-about-page-display)

[2.1.4.1 Mission Statement	9](#2.1.4.1-mission-statement)

[2.1.4.2 Outline Company Story	9](#2.1.4.2-outline-company-story)

[2.1.4.3 Explain who is involved in the project	9](#2.1.4.3-explain-who-is-involved-in-the-project)

[2.1.4.4 Explain whom you serve	9](#2.1.4.4-explain-whom-you-serve)

[2.1.4.5   Logo Display	9](#2.1.4.5-logo-display)

[2.1.5    Admin Page	9](#2.1.5-admin-page)

[2.1.5.1 Admin Account Requests	9](#2.1.5.1-admin-account-requests)

[2.2.5.2  Admin User Request Page	9](#2.2.5.2-admin-user-request-page)

[2.1.5.3 Upload Requests	9](#2.1.5.3-upload-requests)

[2.1.5.4 Current Users	10](#2.1.5.4-current-users)

[2.1.5.5 Current Users	10](#2.1.5.5-current-users)

[2.2.5.6  Account Deletion	10](#2.2.5.6-account-deletion)

[2.2.5.7  Account Edit	10](#2.2.5.7-account-edit)

[2.1.5.8 Admin Add a Filter	10](#2.1.5.8-admin-add-a-filter)

[2.1.6 Contact Us Page	10](#2.1.6-contact-us-page)

[2.1.6.1 Name Field	10](#2.1.6.1-name-field)

[2.1.6.2 Email Field	10](#2.1.6.2-email-field)

[2.1.7   Logo Display	10](#2.1.7-logo-display)

[2.1.7.1 Name Field	10](#2.1.7.1-name-field)

[2.2  Website Functionality	11](#2.2-website-functionality)

[2.2.1  User Upload Submission	11](#2.2.1-user-upload-submission)

[2.2.1.1  Title	11](#2.2.1.1-title)

[2.2.1.2 Name	11](#2.2.1.2-name)

[2.2.1.3  Location	11](#2.2.1.3-location)

[2.2.1.4 Content Description	11](#2.2.1.4-content-description)

[2.2.1.5  Audio/Visual Content	11](#2.2.1.5-audio/visual-content)

[2.2.2  Map Functionality	11](#2.2.2-map-functionality)

[2.2.2.1  Submission Filter	11](#2.2.2.1-submission-filter)

[2.2.2.2  Filter Tab	11](#2.2.2.2-filter-tab)

[2.2.3  Administrator Features	11](#2.2.3-administrator-features)

[2.2.3.1  Upload Approval Process	11](#2.2.3.1-upload-approval-process)

[2.2.3.2  Upload Approval Process Notification	11](#2.2.3.2-upload-approval-process-notification)

[2.2.3.3  Upload Rejection Process	11](#2.2.3.3-upload-rejection-process)

[2.2.3.4  Upload Rejection Process Notification	12](#2.2.3.4-upload-rejection-process-notification)

[2.2.3.5  Account Search	12](#2.2.3.5-account-search)

[2.2.3.6  Account Deletion	12](#2.2.3.6-account-deletion)

[2.2.4  Contributor Features	12](#2.2.4-contributor-features)

[2.2.4.1  Contributor Login Button	12](#2.2.4.1-contributor-login-button)

[2.2.4.2  Contributor Sign up Button	12](#2.2.4.2-contributor-sign-up-button)

[2.2.4.3  Contributor Search Alphabet Display	12](#2.2.4.3-contributor-search-alphabet-display)

[2.2.4.4  Contributor Search Bar Display	12](#2.2.4.4-contributor-search-bar-display)

[2.2.4.5  Contributor List	12](#2.2.4.5-contributor-list)

[2.2.4.6  User Accessibility	12](#2.2.4.6-user-accessibility)

[2.2.4.7  User Submissions	12](#2.2.4.7-user-submissions)

[2.2.5  Integration Features	13](#2.2.5-integration-features)

[2.2.5.1  Integration with External Systems	13](#2.2.5.1-integration-with-external-systems)

[2.2.6  Website Menu Taskbar	13](#2.2.6-website-menu-taskbar)

[2.2.6.1  Homepage Menu Display	13](#2.2.6.1-homepage-menu-display)

[2.2.7  Project Display	13](#2.2.7-project-display)

[2.2.7.1 Project Selection	13](#2.2.7.1-project-selection)

[2.2.8 Contact us Page	13](#2.2.8-contact-us-page)

[2.2.8.1 Name Field	13](#2.2.8.1-name-field)

[2.2.8.2 Email Field	13](#2.2.8.2-email-field)

[3\.  System Requirements	13](#3.-system-requirements)

[3.1  Hardware Requirements	13](#3.1-hardware-requirements)

[3.1.1  Compatibility With Computer Hardware	13](#3.1.1-compatibility-with-computer-hardware)

[3.1.2  Compatibility With Mobile Hardware	14](#3.1.2-compatibility-with-mobile-hardware)

[3.1.3  Required Hardware for User Input	14](#3.1.3-required-hardware-for-user-input)

[3.2  Software Requirements	14](#3.2-software-requirements)

[3.2.1  Computer Software Compatibility	14](#3.2.1-computer-software-compatibility)

[3.2.2  Mobile Software Compatibility	14](#3.2.2-mobile-software-compatibility)

[4\. Interfaces	14](#4.-interfaces)

[4.1  Standalone Program	14](#4.1-standalone-program)

[5\. Performance	14](#5.-performance)

[6\. Delivery	14](#6.-delivery)

[6.1 Website Delivery	14](#6.1-website-delivery)

[7\.  Miscellaneous	14](#7.-miscellaneous)

**Revision History**

| Date | Version | Description | Author(s) |
| :---: | :---: | :---: | :---: |
|  November 29th, 2023 | 1.1  | Initial Draft  | Kylie Hall John Heinig Malik Hill Naheed John Yaro Kulchyckyj Isabella Stephens  Brittany Brenneman |
|  January 24th, 2024  |  1.1 |  Start of revisions for 2024 |  Daniel Reina Alex Ochman Gavin McDonald John Heinig Kendahl Michael Shively |
| February  24, 2025 | 1.2 | Revision for SP2025 | Sophia Lin |

# **1\.  Introduction** {#1.-introduction}

## **1.1 Purpose** {#1.1-purpose}

The purpose of the Software Requirements Specification (SRS) is to describe the software requirements of the Chesapeake Community Connection website. This document provides detailed information of the functional and non-functional capabilities along with user interface requirements. The SRS is a guideline to attempt to create a website with a positive atmosphere involving environmental justice; the development team shall focus on the following factors: positive imagery (pins and images outside of uploads must not contain negative imagery like skeletons and hazard signs), positive wording (emphasis on finding solutions to conflicts rather than finding conflicts by themselves), and fostering a sense of community (ideas for this pending). All requirements described in this document shall be used to aid the Research & Development (R\&D) and Quality Assurance (QA) teams in their development of the application. In addition, the SRS serves to establish the project schedule.

## **1.2 Scope** {#1.2-scope}

This Software Requirements Specification (SRS) establishes a thoroughly detailed overall description for the software requirements, testing, deployment, and qualifications for the website application. This SRS is organized into a total of seven sections. Excluding the first section being the introduction, the remaining six sections individually cover the software functional capabilities (Section 2), system requirements (Section 3), external interfaces (Section 4), performance specifications (Section 5), delivery method of the software (Section 6), and software delivery schedule (Section 7\) which go into detail pertaining to the information necessary to reference for the duration of development accurately. The development of the website shall focus on simplicity and ease of access to new users. The development must give careful consideration to said areas: the tag filtering system, the input information required to upload new submissions, and the map pins system. All options shall be easily seen and identified on the website with minimal exploration necessary on the user’s part. The approaches encompassed within this SRS document are contingent on the product requirements provided by the client’s description as they were comprehended at the time of writing.

## **1.3 Definitions, Acronyms, and Abbreviations** {#1.3-definitions,-acronyms,-and-abbreviations}

| Acronym | Meaning |
| :---: | :---: |
| QA | Quality Assurance |
| R\&D | Research and Development |
| SRS | Software Requirements Specification |

## **1.4 Document References** {#1.4-document-references}

| Document Title | Version | Date | Author(s) |
| :---: | :---: | :---: | :---: |
| Software Requirements Specification | 1.0 | January 24th, 2024 | Kylie Hall John Heinig Malik Hill Naheed John Yaro Kulchyckyj Isabella Stephens  Brittany Brenneman |

##  **1.5 System Overview** {#1.5-system-overview}

The Chesapeake Community Connection website serves as a hub for improving connections and knowledge exchange within the Chesapeake Community. Its core function is to encourage users to share their environmental stories in audiovisual formats; specifically, the website shall focus on community solutions and the current innovation involved in finding solutions to environmental conflicts. The platform features an accessible user interface accompanied with a designated page explaining the user interface and its capabilities, content submission capabilities, admin oversight for safety, a filtering system for efficient content discovery, and an interactive map system highlighting community-related locations. It ensures seamless access on both mobile and desktop devices through the Google Chrome browser, facilitating widespread community engagement and knowledge sharing.

# **2\. Functional Description** {#2.-functional-description}

The software requirements described in this document reflect the conditions required by the customer’s  
description of the Chesapeake Community Connection website. The statements in this document shall include non-requirements/desirements and requirements. Desirement statements contain the phrase “should” to indicate this statement is a desired feature in the software that are not absolute requirements. Requirement statements contain the verb “shall” to indicate this statement is an absolute requirement in the software. The specific wording used for non-requirement and requirement statements will be used separately to promote a clear understanding of what is expected in the software in regards to what will be required and desired.

## **2.1	Website Display** {#2.1-website-display}

### 2.1.1   Homepage  {#2.1.1-homepage}

##### 2.1.1.1  World Map Outline {#2.1.1.1-world-map-outline}

The website shall have the map on the homepage. 

##### 2.1.1.2  World Map Filter {#2.1.1.2-world-map-filter}

The website shall have a designated section to the left of the map that displays the filters available for the optional and necessary categories.

##### 2.1.1.3  **World Map** Scope {#2.1.1.3-world-map-scope}

The system shall display a map of the Chesapeake area. 

##### 2.1.1.4  **Map** Pins {#2.1.1.4-map-pins}

The website map shall feature basic markers to show uploaded projects.

##### 2.1.1.5  Map Pin Color {#2.1.1.5-map-pin-color}

		The website map shall give each pin a specific color to represent the project type. 

##### 2.1.1.6  **Descriptive I**n**fo** {#2.1.1.6-descriptive-info}

The website map shall show a description of the upload (which is obtained through upload submission by the user) located below the map plugin.

##### 2.1.1.7  **Full Screen Option** {#2.1.1.7-full-screen-option}

The website map shall allow the user to view the map in the full screen if desired and see resources linked to it.

##### 2.1.1.8   Logo Display {#2.1.1.8-logo-display}

There shall be a logo provided either by the Research & Development team that is displayed in the top left corner of this page.

### 2.1.2    Contributor Page Display {#2.1.2-contributor-page-display}

#### 2.1.2.1  Contributor Login Button {#2.1.2.1-contributor-login-button}

		There shall be a login button labeled “Contributor Login” at the top of the page.

#### 2.1.2.2  Contributor Sign up Button {#2.1.2.2-contributor-sign-up-button}

There shall be a sign up button labeled “Contributor Sign Up” at the top of the page accompanied by a description about what it means to be a contributor (“Do you want to contribute?”)

#### **2.1.**2.3  **Contributor Search Alphabet Display** {#2.1.2.3-contributor-search-alphabet-display}

There shall be a navigator function at the top of the page listing the alphabet to navigate to the contributors starting with that letter. 

#### 2.1.2.4  Contributor Search Bar Display {#2.1.2.4-contributor-search-bar-display}

There shall be a search bar at the top of the page to navigate to specific contributors.

#### 2.1.2.5  Contributor List {#2.1.2.5-contributor-list}

There shall be a list of all of the contributors that are registered to the site which will include the name and mission statement of the contributor.

#### 2.1.2.6 View More Button {#2.1.2.6-view-more-button}

There shall be a View More button located on the bottom of the contributon’s descriptive box that when interacted with, will show both that contribution and all other contributions within that same area and/or on that same pin.  
		

### 2.1.3    Help/Tutorial Page {#2.1.3-help/tutorial-page}

#### 	2.1.3.1 Frequently Asked Questions {#2.1.3.1-frequently-asked-questions}

There shall be a frequently asked question (FAQ) section that lists FAQs in the form of a dropdown option to open each question’s answer which is decided by the QA team and the customer.

#### 2.1.3.2 Map Animation {#2.1.3.2-map-animation}

There shall be a GIF animation demonstrating the use of filters and opening pin descriptions.  
		

#### 	2.1.3.3 Tutorial Explaining how to use website {#2.1.3.3-tutorial-explaining-how-to-use-website}

There shall be a text description of the steps on how to use the map.

#### 2.1.3.4   Logo Display {#2.1.3.4-logo-display}

There shall be a logo provided either by the customer or suggested by either the Research & Development or Quality Assurance teams that is displayed in the top left corner of this page.

### 2.1.4    About Page Display {#2.1.4-about-page-display}

#### 2.1.4.1 Mission Statement {#2.1.4.1-mission-statement}

This section shall include the mission statement of this website: “To showcase the resilience of the Chesapeake region through a user-friendly platform, where community members can share information on a spectrum of initiatives, each contributing to our collective ability to thrive amidst change. From ecological restoration to placemaking and racial healing, our platform serves as a dynamic hub for collaborative learning. We aim to inspire innovation and cultivate a deeper understanding of the diverse resilience work contributed within our communities.”

#### 2.1.4.2 Outline Company Story {#2.1.4.2-outline-company-story}

This section shall describe the story behind the website and how it will contribute to the community.  
		

#### 2.1.4.3 Explain who is involved in the project {#2.1.4.3-explain-who-is-involved-in-the-project}

This section shall recognize St. Mary’s College as the creators of this site on behalf of Parisa Rinaldi’s vision.  
		

#### 2.1.4.4 Explain whom you serve {#2.1.4.4-explain-whom-you-serve}

This section shall describe the values of the website and how it serves all contributors to the community.

#### 2.1.4.5   Logo Display {#2.1.4.5-logo-display}

There shall be a logo provided either by the Research & Development team that is displayed in the top left corner of this page.

### 2.1.5    Admin Page {#2.1.5-admin-page}

#### 	**2.1.5.1 Admin Account Requests** {#2.1.5.1-admin-account-requests}

The “User Requests” section shall list the account requests in order from oldest to newest.

#### 2.2.5.2  Admin User Request Page {#2.2.5.2-admin-user-request-page}

The “User Requests” section shall have an option to “accept” or “reject” each account request.

#### 2.1.5.3 Upload Requests {#2.1.5.3-upload-requests}

There shall be a section labeled “Upload Requests” which will list the current pending upload requests to the map.

#### 2.1.5.4 Current Users {#2.1.5.4-current-users}

There shall be a section labeled “Current Users” which will list the current pending users requesting access to a contributor account.

#### 2.1.5.5 Current Users {#2.1.5.5-current-users}

There shall be a search bar option within the “Current Users” page.

#### 2.2.5.6  Account Deletion {#2.2.5.6-account-deletion}

For each account listed within the section “Current Users”, there shall be a button labeled “Delete”.

#### 2.2.5.7  Account Edit {#2.2.5.7-account-edit}

For each account listed within the section “Current Users”, there shall be a button labeled “Edit” which will allow the admin to edit the name, email, phone number, or other information.

#### 2.1.5.8 Admin Add a Filter {#2.1.5.8-admin-add-a-filter}

		There shall be a button on the admin page labeled “Add a Filter”. Which will allow admins to   
add a new filter option that organizations can apply to content that they upload.     
		

### 2.1.6	Contact Us Page {#2.1.6-contact-us-page}

#### 	**2.1.6.1** Name Field {#2.1.6.1-name-field}

		The website page shall have a section that allows users to add their names.

#### 2.1.6.2 Email Field {#2.1.6.2-email-field}

		The website page shall feature a field that allows the user to add their email address.

		**2.1.6.3 Message Field**  
		The website page shall feature a field that allows users to submit messages.

### 2.1.7   Logo Display {#2.1.7-logo-display}

#### 2.1.7.1 Name Field {#2.1.7.1-name-field}

There shall be a St. Mary’s College of MD  logo provided by the Research & Development team that is displayed on the bottom right side of every page.

## **2.2  Website Functionality** {#2.2-website-functionality}

### **2.2.1**  **User Upload Submission**  {#2.2.1-user-upload-submission}

##### 2.2.1.1  Title {#2.2.1.1-title}

The submission form shall require the user to enter a title.

##### 2.2.1.2 **Name** {#2.2.1.2-name}

The submission form shall require the user to enter a first name and last name for the person uploading. 

##### 2.2.1.3  **Location** {#2.2.1.3-location}

The submission form shall require the user to enter an address to be associated with the uploaded content. 

##### **2.2.1.**4 **Content Description**  {#2.2.1.4-content-description}

The submission form shall require the user to describe the content that is being submitted. 

##### 2.2.1.5  Audio/Visual Content {#2.2.1.5-audio/visual-content}

The submission shall allow the user to upload any audio visual content.

### 2.2.2  Map Functionality {#2.2.2-map-functionality}

#### 2.2.2.1  Submission Filter {#2.2.2.1-submission-filter}

Content on the website shall be organized by different tags/categories that allows the user to filter the pins shown on the map based on tags/categories chosen by the user.


#### 2.2.2.2  Filter Tab {#2.2.2.2-filter-tab}

The website shall filter projects by main project types which have the ability to filter by individual, organization projects, active projects, inactive projects, and finished projects. 

### 2.2.3  Administrator Features {#2.2.3-administrator-features}

#### 2.2.3.1  Upload Approval Process {#2.2.3.1-upload-approval-process}

The admin shall be able to approve the content to be uploaded to the map which will publish it to the site.

#### 2.2.3.2  Upload Approval Process Notification {#2.2.3.2-upload-approval-process-notification}

After an upload request is accepted, the person who attempted to upload the post shall receive an email that the post was approved. 

#### 2.2.3.3  Upload Rejection Process {#2.2.3.3-upload-rejection-process}

The admin shall be able to reject the content to be uploaded to the map which will not publish it to the site.

#### 2.2.3.4  Upload Rejection Process Notification {#2.2.3.4-upload-rejection-process-notification}

After an upload request is rejected, the person who attempted to upload the post shall receive an email that the post was rejected. 

#### 2.2.3.5  Account Search {#2.2.3.5-account-search}

Within the section “Current Users”, there shall be the option to search for a specific user by email or username.

#### 2.2.3.6  Account Deletion {#2.2.3.6-account-deletion}

The Admin shall double-click on the “delete” button to remove an account from the database.

### 2.2.4  Contributor Features {#2.2.4-contributor-features}

#### 2.2.4.1  Contributor Login Button {#2.2.4.1-contributor-login-button}

After double-clicking “Contributor Login” the user shall enter their username and password to log into the Contributor Account. 

#### 2.2.4.2  Contributor Sign up Button {#2.2.4.2-contributor-sign-up-button}

The user shall enter their username and password accompanied by a description of what it means to be a contributor after double clicking “Contributor Sign up”.

#### 2.2.4.3  Contributor Search Alphabet Display {#2.2.4.3-contributor-search-alphabet-display}

After clicking on the “Alphabet Display” function, the user shall be able to alphabetically navigate through the contributors of the page starting with the beginning letter of the contributor’s name.

#### 2.2.4.4  Contributor Search Bar Display {#2.2.4.4-contributor-search-bar-display}

		The user shall be able to navigate specific contributors by clicking on the search bar feature.

#### 

#### 2.2.4.5  Contributor List {#2.2.4.5-contributor-list}

The list of all contributors registered with the site including the name and mission statement shall be displayed to the user after searching.

#### 2.2.4.6  User Accessibility {#2.2.4.6-user-accessibility}

Users shall be able to access the platform from QR codes that could give them easier access to the site as well as access to upload information.

#### 2.2.4.7  User Submissions {#2.2.4.7-user-submissions}

Users shall be able to share information on the website that will aid in providing knowledge on environmental issues and concerns and other updates. Submission requirements would include the location, resource links, and written words that describe the message the user wants to share.

### 2.2.5  Integration Features {#2.2.5-integration-features}

#### 2.2.5.1  Integration with External Systems {#2.2.5.1-integration-with-external-systems}

The website shall be able to interact  and integrate with external systems or APIs.

### 2.2.6  Website Menu Taskbar {#2.2.6-website-menu-taskbar}

#### 2.2.6.1  Homepage Menu Display {#2.2.6.1-homepage-menu-display}

The system shall display a menu taskbar on the homepage including each of the pages: Home, About, Contributors, Help/Tutorial.

### 2.2.7  Project Display {#2.2.7-project-display}

#### 2.2.7.1 Project Selection {#2.2.7.1-project-selection}

The website shall display a box with a list of projects on the map with a map marker in the area in which the project exists when the user makes a selection.

### 2.2.8 Contact us Page {#2.2.8-contact-us-page}

#### 

#### 2.2.8.1 Name Field {#2.2.8.1-name-field}

The user shall be able to add their names to the featured section after clicking on the name field. 

#### 2.2.8.2 Email Field {#2.2.8.2-email-field}

The user shall be allowed to enter their email address to the featured field.

**2.2.8.3 Message Field**  
The user shall be allowed to send messages on the message field. 

**2.2.8.4 Send**   
The user shall be allowed left-click on the “send” button to send the message to the admin.  
                  

# **3\.  System Requirements** {#3.-system-requirements}

This section describes the required hardware and software necessary to run the website.

## **3.1  Hardware Requirements** {#3.1-hardware-requirements}

### 3.1.1  Compatibility With Computer Hardware {#3.1.1-compatibility-with-computer-hardware}

The software shall be compatible with standard laptop and desktop computers.

### 3.1.2  Compatibility With Mobile Hardware {#3.1.2-compatibility-with-mobile-hardware}

The software shall be compatible with standard smartphone devices.

### 3.1.3  Required Hardware for User Input {#3.1.3-required-hardware-for-user-input}

The software shall require a keyboard to submit the student and community comments, a mouse to navigate around the website and select options within it, and a monitor to view the website on a screen.

## **3.2  Software Requirements** {#3.2-software-requirements}

### 3.2.1  Computer Software Compatibility {#3.2.1-computer-software-compatibility}

The website must be compatible with Windows 10 and MacOS 14.0 for optimal user experience.

### 3.2.2  Mobile Software Compatibility {#3.2.2-mobile-software-compatibility}

The website must be compatible with Android 11 and Apple iOS 16 for optimal user experience.

# **4\. Interfaces** {#4.-interfaces}

## **4.1  Standalone Program** {#4.1-standalone-program}

The program shall run standalone, not interacting with a network in any manner.

# **5\. Performance** {#5.-performance}

The following requirements address the performance requirements of the Chesapeake Community Connection Website Software Application. 

# **6\. Delivery** {#6.-delivery}

The following requirements address the delivery of the Chesapeake Community Website.

## **6.1 Website Delivery**  {#6.1-website-delivery}

The Chesapeake Community Website shall be delivered by demonstration and use on Google Chrome. 

# **7\.  Miscellaneous** {#7.-miscellaneous}

No miscellaneous information at this time.