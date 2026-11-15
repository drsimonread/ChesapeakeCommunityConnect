Checkers Computer Software Application Software Requirements Specification Version 2.0 

October 24, 2022 

The Systems Squad 

Team Members: 

Kylie Hall   
Brittany Brenneman   
Xan Weatherholtz  
**Checkers Computer Software Application**   
**Software Requirements Specification**   
**The Systems Squad** 

**Table of Contents** 

**1\. Introduction 4** 1.1 Purpose 4 1.2 Scope 4 1.3 Definitions, Acronyms, and Abbreviations 4 1.4 Document References 4 1.5 System Overview 5 

2\. Functional Description **5** 2.1 Game Display 5 2.1.1 Checkerboard Display 5 2.1.1.1 Checkerboard Outline 5 2.1.1.2 Checkerboard Pattern 5 2.1.1.3 Checkerboard Pattern Placement 5 2.1.1.4 Checkerboard Playing Piece Placement 6 2.1.1.5 Checkerboard Display 6 2.1.2 Game Display Menu 6 2.1.2.1 Display Menu 6 2.1.2.2 Restart in Menu 6 2.1.2.3 Undo in Menu 6 2.1.2.4 Quit from Menu 6 2.1.3 User Display Features 6 2.1.3.1 User Names 6 2.1.3.2 Highlight User Names 6 2.1.3.3 Display Score 6 2.1.3.4 Display Score Function 7 2.1.4 Pregame software display 7 2.1.4.1 Display First User Input of Name 7 2.1.4.2 Length of First User Name 7 2.1.4.3 Display Button to Allow Second User Input 7 2.1.4.4 Display Button to Allow Second User Input Functionality 7 2.1.4.5 Display Second User Input of Name 7 2.1.4.6 Length of Second User Name 7 2.1.4.7 Display User Input to Load Checkerboard Screen 7 2.1.4.8 Display User Input to Load Checkerboard Screen Functionality 7 2.1.5 Endgame software display 7 2.1.5.1 Endgame Winner Display 7 2.1.5.2 Display to Prompt User to Play Again or Quit 8 2.1.5.3 Losing Player Plays Black Pieces 8 

October 24, 2022 2 Version 2.0  
**Checkers Computer Software Application**   
**Software Requirements Specification**   
**The Systems Squad** 

2.2 Gameplay 8 2.2.1 Selection of Objects 8 2.2.2 User Requirements 8 2.2.3 Movements 8 2.2.4 Capture 9 

3\. System Requirements **10** 3.1 Hardware Requirements 10 3.2 Software Requirements 10 

4\. Interfaces **10** 4.1 Standalone Program 10 4.2 Use of Windows DLLs 11 4.3 Human Interfaces 11 

5\. Performance **11** 5.1 Launch Performance 11 5.2 Launch Checkerboard Screen 11 5.3 User Response 11 

6\. Delivery **11** 6.1 Software Delivery 11 

7\. Schedule **12** 8\. Miscellaneous **12** 

**Revision History** 

| Date  | Version  | Description  | Author(s) |
| ----- | ----- | ----- | ----- |
| September 26, 2022  | 1.0  | Initial Version  | Kylie Hall,  Brittany Brenneman, Xan  Weatherholtz, & Isabella  Woel-Popovich |
| October 24, 2022  | 2.0  | Revised from Initial Version  | Kylie Hall,  Brittany Brenneman, and Can Weatherholtz |
|  |  |  |  |

October 24, 2022 3 Version 2.0  
**Checkers Computer Software Application**   
**Software Requirements Specification**   
**The Systems Squad** 

**1\. Introduction** 

**1.1 Purpose** 

The purpose of this Software Requirements Specification (SRS) is to describe the software requirements of the Checkers Computer Software Application. This document provides detailed information of the functional and non-functional capabilities along with user interface requirements. 

**1.2 Scope** 

This Software Requirements Specification (SRS) establishes a thoroughly detailed overall description for the software requirements, testing, deployment, and qualifications for the Checkers Computer Software Application. This SRS is organized into a total of seven sections. Excluding the first section being the introduction, the remaining six sections individually cover the software functional capabilities (Section 2), system requirements (Section 3), external interfaces (Section 4), performance specifications (Section 5), delivery method of the software (Section 6), and software delivery schedule (Section 7\) which go into detail pertaining to the information necessary to reference for the duration of development accurately. The approaches encompassed within this SRS document are contingent on the product requirements provided by the client’s description as they were comprehended at the time of writing. 

**1.3 Definitions, Acronyms, and Abbreviations** 

| Acronym  |
| :---: |
| DLL  |
| SDP  |
| SRS  |

**Meaning** 

Dynamic Link Library 

Software Development Plan Software Requirements Specification 

**1.4 Document References** 

| Document Title  | Version Date Author(s) |
| ----- | ----- |
| Software Development Plan  | 1.0 September 14,  Kylie Hall,  2022  Brittany Brenneman, Xan  Weatherholtz, & Isabella  Woel-Popovich |
| Software Requirements Specification  | 1.0 September 26,  Kylie Hall, 2022  |

October 24, 2022 4 Version 2.0  
**Checkers Computer Software Application**   
**Software Requirements Specification**   
**The Systems Squad** 

|  | Brittany Brenneman, Xan  Weatherholtz, & Isabella  Woel-Popovich |
| :---- | ----: |

**1.5 System Overview** 

The customer requires a software-based application which runs on a desktop computer running the Windows operating system to allow two users to play the game of checkers on the same computer. The software will include specifications of the checkers game made by the customer to perform a full game of checkers with options to undo a movement made, quit the application, and to restart the game. The application will be delivered on a flash drive where no installation is required. 

**2\. Functional Description** 

The software requirements described in this document reflect the conditions required by the customer’s description of the Checkers Game Application. The statements stated in this document shall include non-requirements/desirements and requirements. Desirement statements contain the phrase “should” to indicate this statement is a desired feature in the software that are not absolute requirements. Requirement statements contain the verb “shall” to indicate this statement is an absolute requirement in the software. The specific wording used for non-requirement and requirement statements will be used separately to promote a clear understanding of what is expected in the software in regards to what will be required and desired. 

**2.1 Game Display** 

**2.1.1 Checkerboard Display** 

2.1.1.1 **Checkerboard Outline** 

The system shall display an 8x8 square in the middle of the screen with a total of 64 squares displayed within the square to act as the checkerboard. 

2.1.1.2 **Checkerboard Pattern** 

The system shall display a checkerboard color pattern of 2 alternating colors of dark gray and light gray on the 64 square board where the dark and light gray only touch in rows and columns and the same color square only touch diagonally. 

2.1.1.3 **Checkerboard Pattern Placement** 

The system must display the order of this checkerboard pattern by having the light gray square begin at the top left-most corner of the board and the right bottom-most corner, and the dark gray shall be at the top right-most corner and left bottom-most corner. 

October 24, 2022 5 Version 2.0  
**Checkers Computer Software Application**   
**Software Requirements Specification**   
**The Systems Squad** 

2.1.1.4 **Checkerboard Playing Piece Placement** 

Before the game begins, the system shall display 12 disk-shaped black pieces the size to fit in one square at the bottom of the board only on the dark gray squares and 12 red, disk-shaped checker pieces with the size to fit in one square at the top of the board only placed on the dark gray squares where the middle two rows in the middle of the board must have no pieces placed at the start of the game. 

2.1.1.5 **Checkerboard Display** 

The system shall display a yellow star on any checker piece that travels to the other side of the board during a game, becoming a king, to allow both users to visually see which piece is a king; more information on the mechanics of this shall be provided in section *2.2.3 Movements.* 

**2.1.2 Game Display Menu** 

2.1.2.1 **Display Menu** 

The system shall display a menu on the checkerboard game screen 

2.1.2.2 **Restart in Menu** 

The system shall allow the user to restart the game at any point after the step of inputting player names. 2.1.2.3 **Undo in Menu** 

The system shall allow a user to undo the last movement made in the game. 

2.1.2.4 **Quit from Menu** 

The system shall allow a user to select a quit menu option that allows the user to close the application. 

**2.1.3 User Display Features** 

2.1.3.1 **User Names** 

The system shall display both of the player’s names on the checkerboard game screen. 2.1.3.2 **Highlight User Names** 

The system shall highlight a player’s name with a bright color when it is their turn to move a piece. 2.1.3.3 **Display Score** 

The system shall display the number of games won by each user (the score) on the checkerboard playing screen. 

October 24, 2022 6 Version 2.0  
**Checkers Computer Software Application**   
**Software Requirements Specification**   
**The Systems Squad** 

2.1.3.4 **Display Score Function** 

The system shall update the score every time a user wins a round of checkers. 

**2.1.4 Pregame software display** 

2.1.4.1 **Display First User Input of Name** 

The system shall display an option prompting the first player to enter their name with a text box. 2.1.4.2 **Length of First User Name** 

The system shall allow the first player to enter up to 20 characters into the text box. 

2.1.4.3 **Display Button to Allow Second User Input** 

The system shall provide a button next to the textbox that the first user can click when finished entering their name labeled “next”. 

2.1.4.4 **Display Button to Allow Second User Input Functionality** 

The system shall allow the first user button to then load the text box prompting for the input of the second user’s name. 

2.1.4.5 **Display Second User Input of Name** 

The system shall display an option prompting the second player to enter their name with a text box. 2.1.4.6 **Length of Second User Name** 

The system shall allow the second player to enter up to 20 characters into the text box. 2.1.4.7 **Display User Input to Load Checkerboard Screen** 

The system shall provide a button the second user can click on when finished typing their name labeled “finished”. 

2.1.4.8 **Display User Input to Load Checkerboard Screen Functionality** 

The system shall allow the second user button to then load the main checkerboard screen to begin the checkers game. 

**2.1.5 Endgame software display** 

2.1.5.1 **Endgame Winner Display** 

At the end of the game, the software shall display if player one or player two has won on the screen. October 24, 2022 7 Version 2.0  
**Checkers Computer Software Application**   
**Software Requirements Specification**   
**The Systems Squad** 

2.1.5.2 **Display to Prompt User to Play Again or Quit** 

The system shall provide a text box the user can view on the endgame screen displaying “Use the Menu to play again or quit\!” 

2.1.5.3 **Losing Player Plays Black Pieces** 

The system shall allow the loser of the previous game to play the black pieces and to move first if the players decide to play again. 

**2.2 Gameplay** 

**2.2.1 Selection of Objects** 

2.2.1.1 **Selection of Checker Piece and Checker Square** 

When the system is ready for the user to make the first move in the game, the system shall allow the first player to use a mouse to left-click on a playable black checker piece and then follow by left-clicking on a playable square on the board. 

**2.2.2 User Requirements** 

2.2.2.1 **Number of Users** 

The system shall only allow a multiplayer mode where the computer can not be a player; two users are required to play the software. 

2.2.2.2 **First Player Color of Pieces** 

The system shall allow the first player to play the black pieces. 

2.2.2.3 **Second Player Color of Pieces** 

The system shall allow the second player to play the red pieces. 

**2.2.3 Movements** 

2.2.3.1 **Checkerboard Square Boundaries** 

The system shall only allow the game pieces to be moved on the dark gray squares. 

2.2.3.2 **Allowed Movement of Non-King Checker Pieces** 

The system shall have the user move their selected single piece, that is not a king, diagonally forward toward their opponent’s side to an open square. 

October 24, 2022 8 Version 2.0  
**Checkers Computer Software Application**   
**Software Requirements Specification**   
**The Systems Squad** 

2.2.3.3 **Allowed Movement Without Capture** 

The system shall only move a piece to one open square in the diagonally forward direction toward their opponent’s side if the user is moving a single piece without capturing an opponent's piece. 

2.2.3.4 **Alternating Gameplay** 

The system must allow the first user playing the black pieces to move first and then alternating turns with the second user who plays the white pieces. 

2.2.3.5 **Movement of King Piece** 

The system shall only allow pieces to move in the direction opposite of their other pieces, or the same direction as the opponent, if they have gained a king piece by traveling to the first row of the opponent's side of the board. 

2.2.3.6 **Invalid Movement** 

The system shall recognize an invalid move when the user attempts to move a piece either out of bounds from the checkerboard or in a non-playable square. 

2.2.3.7 **Invalid Movement** 

The system shall alert the user of an invalid move with an alert in a text box labeled with the alternating phrases “My piece can’t move backwards unless it’s a king\!”, “My piece can only move sideways, forward, and diagonally\!”, and “My pieces need to stay on the board\!” 

**2.2.4 Capture** 

2.2.4.1 **User Capture** 

The system shall allow the user to capture other players pieces or disc-shaped tokens when they are able to jump over the opponents token and successfully land in the immediate open dark gray square in line with the captured piece on the other side. 

2.2.4.2 **Capture Removal** 

The system shall remove the captured piece from the game board for every capture. 

2.2.4.3 **Recording User Capture** 

The system shall keep track of the captured pieces for both users and display them on the checkerboard screen next to the user's names. 

**2.2.5 Game Assistance** 

2.2.5.1 **Playable Movement Assistance** 

October 24, 2022 9 Version 2.0  
**Checkers Computer Software Application**   
**Software Requirements Specification**   
**The Systems Squad** 

The system shall write to the user through a message on the screen describing basic rules of the game if the user isn’t selecting playable moves to help guide the user to play a valid move. 

**2.2.6 End of the Game** 

2.2.6.1 **Winner Declaration** 

The system shall declare a winner of the round if a user has captured 12 opponent pieces, which is recorded throughout the game, or if the user has no open squares to move a piece where the player is blocked in with no moves to execute. 

2.2.6.2 **Draw** 

The system shall declare a tie if each player has one piece left on the board. 

**3\. System Requirements** 

This section describes the required hardware and software necessary to run the software. **3.1 Hardware Requirements** 

**3.1.1 Compatibility With Computer Hardware** 

The software shall be compatible with standard classroom Dell XPS desktop computers. **3.1.2 Required Hardware for User Input** 

The software shall require a keyboard to submit the user gameplay names, a mouse to open the software and select options within it, and a monitor to view the software on a screen. 

**3.2 Software Requirements** 

**3.2.1 Software Compatibility** 

The Checkers Game Application must be compatible with Windows 10 operating system software. 

**4\. Interfaces** 

In this section, all external interfaces utilized by the software will be described. 

**4.1 Standalone Program** 

The program shall run standalone, not interacting with a network in any manner. 

October 24, 2022 10 Version 2.0  
**Checkers Computer Software Application**   
**Software Requirements Specification**   
**The Systems Squad** 

**4.2 Use of Windows DLLs** 

The program shall be self-sufficient, using only standard Windows DLLs. 

**4.3 Human Interfaces** 

The system shall only need a mouse interface and keyboard interface as user input to interact with the software in a series of input and output such as submitting player names with a keyboard and selecting which checker piece to move with a mouse. 

**5\. Performance** 

The following requirements address the performance requirements of the Checkers Computer Software Application. 

**5.1 Launch Performance** 

The Checkers Computer Software Application shall launch the software within 5.0 seconds. **5.2 Launch Checkerboard Screen** 

The Checkers Computer Software Application shall launch the checkerboard screen from the user input player name screen within 3.0 seconds. 

**5.3 User Response** 

The Checkers Computer Software Application user interface shall respond to inputs by a user within 0.5 seconds. 

**6\. Delivery** 

The following requirements address the delivery of the Checkers Computer Software Application. **6.1 Software Delivery** 

The Checkers Game Application shall be delivered on a flash drive containing the application on it that can be transferred and downloaded to any windows computer that fits the hardware and software requirements. 

October 24, 2022 11 Version 2.0  
**Checkers Computer Software Application**   
**Software Requirements Specification**   
**The Systems Squad** 

**7\. Schedule** 

Delivery of the following products shall occur on the following dates: 

| Artifact Delivery Date |
| ----- |
| Software Requirements Specification September 26, 2022 |
| Top-Level C\# Prototype October 12, 2022 |
| Revision of Top-Level Prototype, 2nd-Level  November 2, 2022 Prototype  |
| Revision of Pre-Release Software November 20, 2022 |
| Final Completed Software December 5, 2022 |

**8\. Miscellaneous** 

There are no miscellaneous items at this time. 

October 24, 2022 12 Version 2.0