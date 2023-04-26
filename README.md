# RTDE client library, safety

### Overview
- This repository is forked from the official [RTDE repository](https://github.com/UniversalRobots/RTDE_Python_Client_Library). 
- This repository modifies `../examples/record.py` to monitor the safety status of the robot. When the robot leaves normal mode, a notification email containing data is sent to a recipient(s). 

### Demo
- E-mail sent after protective stop was set.
    
  <kbd>![ezgif com-gif-maker (10)](https://user-images.githubusercontent.com/80125540/234635518-7c9786df-d0c0-4dee-b254-bef8ffe7eff3.gif)</kbd>

## Setup

### Requirements
- Python
- Gmail account

### Instructions

1. [Enable and setup 2-factor authentication for the sending Google account.](https://myaccount.google.com/signinoptions/two-step-verification)

2. [Create an app password token.](https://myaccount.google.com/apppasswords?pli=1&rapt=AEjHL4MUYHZvt52WlayzzitgwWff42mz649CZMzznXsuSbqr8xPTUlvmQQmUKFvaSg3IhN5hKn58CiCKryu8XoAGkx9C8sRDPA) 
      
    <kbd>![app_password](https://user-images.githubusercontent.com/80125540/229267297-c92fa7cc-6fe9-4484-8c3e-b547b92b6d2d.gif)</kbd>

3. Clone this repository into a directory of your choice with the following command:
     
   ```Console
   https://github.com/Shawn-Armstrong/RTDE_Python_Client_Library_Safety.git
   ```
   
4. In `../examples/record.py` at the top, add your email related information.
   
   _Looks like this_
   ```Python
   email_sender = es.EmailSender(
        smtp_host="smtp.gmail.com",
        smtp_port=587,
        username='<SENDER_EMAIL>@gmail.com',
        token_password='<YOUR_APP_PASSWORD>', # NOT your ordinary sign-in password; look at email-sender README.md.
        recipients=["recipient2@example.com", "recipient2@example.com"]
    )
   ```


5. Run the program with the following command using your robot's IPv4:
   
   ```Console
   cd RTDE_Python_Client_Library_Safety\examples
   python record.py --host YOUR_IPv4_GOES_HERE --frequency 10
   ```
   
## Summary
- This setup monitors the robot's safety status. You can easily modify the conditional in `record.py` to do something other then send an email.
