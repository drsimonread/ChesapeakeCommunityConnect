# QA Fall 24/Spring 25:

## Test Log

This document will contain tests written for the CCC Site project. It will include the following:

1. Test Title  
2. Test Number  
3. Test Version  
4. Test Classification  
5. Test Author  
6. Test Purpose  
7. Date Ran  
8. Test Result  
9. Tester Notes  
10. Space for comments

Please create a new test version if a test is edited/updated. This will allow us to track any and all changes to tests. Any changes to another tester's documentation should be approved beforehand, or at the very least a comment left about the changes made.

If/when leaving a comment please include your name and the date that the comment was created.

Notes: While all tests are subject to requiring updates, those labeled “volatile” test areas that cover requirements that are more likely to change as the projects move forward.

**To Run CCC Tests (Windows):**  
		

* **Activate Virtual Environment**  
  * **.venv\\Scripts\\activate**  
  * **cd cccSite**  
* **Run tests**  
  * **Py manage.py test**

## CCC Tests:

Title: Test\_create\_message  
Number: CCC\_001  
Version: 01  
Classification: N/A  
Author: Philip Wade  
Date: 11/06/24  
Purpose: To test creating a message instance in the Models.py class.  
Result: Test passed with no errors.  
Notes:   
Comments:

Title: test\_string\_representation  
Number: CCC\_002  
Version: 01  
Classification: N/A  
Author: Philip Wade  
Purpose: To test the \_\_str\_\_ method in the Models.py class.  
Date: 11/06/24  
Result: Test Passed with no errors.  
Notes:  
Comments: 

Title: test\_email\_field\_validation  
Number: CCC\_003  
Version: 01  
Classification: Volatile  
Author: Philip Wade  
Purpose: To ensure an error is created when an invalid email format is entered.  
Date: 11/06/24  
Result: Test passed with no errors.   
Notes: The “email” string can be changed to a valid format (test@test.com) to make this test result in an error.  
Comments:

Title: test\_form\_valid\_data  
Number: CCC\_004  
Version: 01  
Classification: Volatile  
Author: Philip Wade  
Purpose: To test a form with valid data is accepted.  
Date: 11/06/24  
Result: Test passed with no errors.  
Notes:  
Comments:

Title: test\_form\_invalid\_email  
Number: CCC\_005  
Version: 01  
Classification: Volatile  
Author: Philip Wade  
Purpose: To test that a form with an invalid email format will not be accepted.  
Date: 11/06/24  
Result: Test passed with no errors  
Notes: As with prior email format tests, the email string can be edited to force an error on this test. Volatile due to R\&D team still working to ensure emails are validated, changes may affect this test.   
Comments:

Title: test\_form\_placeholder\_test  
Number: CCC\_006  
Version: 01  
Classification: Volatile  
Author: Philip Wade  
Purpose: To ensure that widgets have the correct placeholder text.  
Date: 11/06/24  
Result: Test passed with no errors.  
Notes: Labeled volatile because widget format may change. Changing any of the testing fields in the test itself will yield a failure, which is the correct result. Given that this test aims to pass rather than fail the condition it is testing.  
Comments:

Title: test\_create\_account  
Number: CCC\_007  
Version: 01  
Classification: Volatile  
Author: Kester Ebo	  
Purpose: To ensure that an account can be created.  
Date: 12/04/24  
Result: Test passed with no errors.  
Notes: Labeled volatile because an invalid email can be used to create an account (bob@realemail.bob)  
Comments:

Title: test\_create\_forum  
Number: CCC\_008  
Version: 01  
Classification: N/A  
Author: Kester Ebo  
Purpose: To ensure that a forum can be made  
Date: 12/04/24  
Result: Test passed with no errors.  
Notes: The forum appears in the pending forum section in “My forums”  
Comments:

Title: test\_report\_forum  
Number: CCC\_009  
Version: 01  
Classification: N/A  
Author: Kester Ebo  
Purpose: To ensure that a report on a forum can be made  
Date: 12/04/24  
Result: Test passed with no errors.  
Notes: A message displaying that the forum has been reported appeared  
Comments:

Title: test\_default\_view\_redirects\_if\_not\_signed\_in  
Number: CCC\_010  
Version: 01  
Classification: N/A  
Author: Philip Wade  
Purpose: Attempts to access the account page as a user who is not signed in.  
Date: 02/10/25  
Result: Test Passed with no errors.  
Notes: Should redirect to sign in page.  
Comments: 

Title: test\_default\_view\_shows\_account\_info  
Number: CCC\_011  
Version: 01  
Classification: N/A  
Author: Philip Wade  
Purpose: Simulate a signed in user attempting to access their account page.  
Date: 02/10/25  
Result: Test Passed with no errors.  
Notes:  
Comments: 

Title: test\_manage\_view\_redirects\_if\_not\_signed\_in  
Number: CCC\_012  
Version: 01  
Classification: N/A  
Author: Philip Wade  
Purpose: Simulates a user not signed in attempting to access account management  
Date: 02/10/25  
Result: Test Passed with no errors.  
Notes:  
Comments: 

Title: test\_manage\_view\_updates\_user\_info  
Number: CCC\_013  
Version: 01  
Classification:   
Author: Philip Wade  
Purpose: Tests that account management page updates user information.  
Date: 02/10/25  
Result: Test Passed with no errors.  
Notes: Updates information and ensures it is reflected on the page  
Comments: 

Title: test\_authG\_view\_invalid\_request  
Number: CCC\_014  
Version: 01  
Classification: N/A  
Author: Philip Wade  
Purpose: Checks that the authG view correctly handles GET requests  
Date: 02/10/25  
Result: Test Passed with no errors.  
Notes: Should redirect to account since authG only handles POST authentication requests.  
Comments: 

Title: test\_authG\_view\_invalid\_csrf  
Number: CCC\_015  
Version: 01  
Classification: N/A  
Author: Philip Wade  
Purpose: Tests that authG rejects requests with invalid CSRF tokens.  
Date: 02/10/25  
Result: Test Passed with no errors.  
Notes: Checks for response containing “Something went wrong, no CSRF cookie” from the view that handles that issue.  
Comments: 