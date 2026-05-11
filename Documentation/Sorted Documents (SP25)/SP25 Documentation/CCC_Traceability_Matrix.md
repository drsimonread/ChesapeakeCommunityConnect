## Revision History

| Date       | Version | Description           | Author(s)                                                                 |
|------------|---------|----------------------|---------------------------------------------------------------------------|
| 1/13/2024  | 1.0     | Traceability Matrix  | Daniel Reina, John Heinig, Kendahl Toft, Alexander Ochman, Malik Hill, Gavin McDonald, Michael Shively |
| 1/24/2024  | 1.1     | Traceability Matrix  | Daniel Reina, John Heinig, Kendahl Toft, Alexander Ochman, Malik Hill, Gavin McDonald, Michael Shively |
| 2/17/2025  | 1.2     | Traceability Matrix  | Benjamin Roberts                                                          |

# 1. Introduction

## 1.1 Purpose
The purpose of this document is to keep track of the development of the Chesapeake Connect Community website and ensure the completeness and transparency of the program. This document will provide a list of requirements that have to be fulfilled.

## 1.2 Scope
This Traceability Matrix is to make sure that as a project team, we follow the guidelines provided for us. With these guidelines, we’ll be able to list goals, future tests, and guidelines needed in order to make sure the system works properly.

## 1.3 Definitions, Acronyms, and Abbreviations

| Acronym | Meaning                          |
|---------|----------------------------------|
| SDP     | Software Development Plan        |
| SRS     | Software Requirements Specification |
| TM      | Traceability Matrix              |

## 1.4 Document References
SDP: Software Development Plan; The purpose of the Software Development Plan (SDP) is to present all information necessary to control the execution of the project. It describes the approach to the development of the software and is the top-level plan generated and used by managers to direct the development effort.  

SRS: Software Requirements Specification; The purpose of the Software Requirements Specification (SRS) is to describe the software requirements of the Chesapeake Community Connection website. The SRS document provides detailed information of the functional and non-functional capabilities along with user interface requirements. The SRS is a guideline to attempt to create a website with a positive atmosphere involving environmental justice.

## 1.5 System Overview
The Chesapeake Community Connection website serves as a hub for improving connections and knowledge exchange within the Chesapeake Community. Its core function is to encourage users to share their environmental stories in audiovisual formats; specifically, the website shall focus on community solutions and the current innovation involved in finding solutions to environmental conflicts. The platform features an accessible user interface accompanied with a designated page explaining the user interface and its capabilities, content submission capabilities, admin oversight for safety, a filtering system for efficient content discovery, and an interactive map system highlighting community-related locations. It ensures seamless access on both mobile and desktop devices through the Google Chrome browser, facilitating widespread community engagement and knowledge sharing.

# 2. Traceability

## 2.1 Requirements List

| Requirement Number | SRS Section Number | SRS Section Title                         |
|-------------------|-------------------|-------------------------------------------|
| R1  | 2.1.1 | Homepage |
| R2  | 2.1.2 | Contributor Page Display |
| R3  | 2.1.3 | Help/Tutorial Page |
| R4  | 2.1.4 | About Page Display |
| R5  | 2.1.5 | Admin Page |
| R6  | 2.1.6 / 2.2.8 | Contact Us Page |
| R7  | 2.1.7 | Logo Display |
| R8  | 2.2.1 | User Upload Submission |
| R9  | 2.2.2 | Map Functionality |
| R10 | 2.2.3 | Administrator Features |
| R11 | 2.2.4 | Contributor Features |
| R12 | 2.2.5 | Integration Features |
| R13 | 2.2.6 | Website Menu Taskbar |
| R14 | 2.2.7 | Project Display |
| R15 | 3.1.1 | Compatibility With Computer Hardware |
| R16 | 3.1.2 | Compatibility With Mobile Hardware |
| R17 | 3.1.3 | Required Hardware for User Input |
| R18 | 3.2.1 | Computer Software Compatibility |
| R19 | 3.2.2 | Mobile Software Compatibility |

## 2.2 Aspects List

| Aspect Number | Aspect (Subsystem) Description        |
|---------------|--------------------------------------|
| A1  | Google Maps |
| A2  | Google Sign-In |
| A3  | Home Screen Map |
| A4  | Home Screen Header |
| A5  | Home Screen Filter |
| A6  | Home Screen Bottom/News |
| A7  | Log-In Functionality |
| A8  | Sign Up Functionality |
| A9  | Log-Out Functionality |
| A10 | Content Upload |
| A11 | Contributor Search Bar |
| A12 | Contributor Information Display |
| A13 | Forgot Password Functionality |
| A14 | User Account Information Display |
| A15 | Username Change |
| A16 | User Password Change |
| A17 | User Profile Picture Change |
| A18 | User Submission Listing |
| A19 | Help Page Display |
| A20 | About Website/Contributor Display |
| A21 | Frequently Asked Questions Listings |
| A22 | Map Tutorial |
| A23 | Website Tutorial |
| A24 | Contact Information Display |
| A25 | Administrator Submission Approval |
| A26 | Administrator Account Search |
| A27 | Administrator Account Editing |
| A28 | Device Compatibility |

## 2.3 Traceability Table

|   | A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8 | A9 | A10 | A11 | A12 | A13 | A14 | A15 | A16 | A17 | A18 | A19 | A20 | A21 | A22 | A23 | A24 | A25 | A26 | A27 | A28 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **R1** | **X** |  | **X** | **X** | **X** |  |  |  |  | **X** |  |  |  |  |  |  |  | **X** |  |  |  |  |  |  |  |  |  |
| **R2** |  |  |  |  |  |  | **X** | **X** |  |  | **X** | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **R3** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** |  | **X** | **X** |  |  |  |  |  |
| **R4** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** |  |  |  |  |  |  |  |
| **R5** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** | **X** | **X** |  |
| **R6** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** |  |  |  |  |
| **R7** |  |  |  | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **R8** |  |  |  |  |  |  |  |  |  | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **R9** | **X** |  | **X** |  | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **R10** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** | **X** | **X** |  |
| **R11** |  |  |  |  |  |  | **X** | **X** |  | **X** | **X** | **X** |  |  |  |  |  | **X** |  |  |  |  |  |  |  |  |  |
| **R12** | **X** | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **R13** |  |  |  | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **R14** | **X** |  | **X** |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** |  |  |  |  |  |  |  |  |  |
| **R15** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** |
| **R16** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** |
| **R17** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** |
| **R18** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** |
| **R19** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | **X** |


3\. Miscellaneous No miscellaneous information at this time. | | ----- |
