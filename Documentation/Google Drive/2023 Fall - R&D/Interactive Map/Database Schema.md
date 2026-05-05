Entities and Their Attributes:

Users:

* UserID (Primary Key)  
* Origin (third-party source, e.g., Google, Facebook, Apple, etc.)  
* Email  
* OrgID

Ecological Events:

* EventID (Primary Key)  
* Title  
* Description  
* EventDate  
* EventTag (e.g., Marine Science, Fossil, Agriculture, etc.)  
* UserID (Foreign Key, referring to the user who reported the event)  
* LocationID (Foreign Key, referring to the location of the event)

Organization:

* OrgID  
* OrgName  
* OrgLocation


Locations:

* LocationID (Primary Key)  
* Name  
* Latitude  
* Longitude  
* Country  
* Other location-related attributes (e.g., ecosystem type, altitude, etc.)

Comments:

* CommentID (Primary Key)  
* Text  
* CommentDate  
* UserID (Foreign Key, referring to the user who posted the comment)  
* EventID (Foreign Key, referring to the event the comment is related to)

Media Files (Images, Videos, etc.):

* MediaID (Primary Key)  
* FileType (e.g., image, video, etc.)  
* FileName  
* FilePath  
* UploadDate  
* UserID (Foreign Key, referring to the user who uploaded the media)  
* EventID (Foreign Key, referring to the event the media is related to)

Tags:

* TagID (Primary Key)  
* TagName  
* Description

Event-Tag Association (Many-to-Many):

* EventTagID (Primary Key)  
* EventID (Foreign Key, referring to the event)  
* TagID (Foreign Key, referring to the tag)

Sessions:

* SessionID (Primary Key), granted to user via a cookie  
* SignedIn (boolean, defaults to false, set to true when the user has authenticated)  
* UserID (Foreign Key, referring to the user associated with the session)  
* Rank  
* First Name  
* Last Name