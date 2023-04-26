# RTDE client library, safety

### Overview
- This repository is forked from the official [RTDE repository](https://github.com/UniversalRobots/RTDE_Python_Client_Library). 
- This repository modifies `../examples/record.py` to monitor the safety status of the robot. When the robot leaves normal mode, a notification email containing data is sent to a recipient. 

### Demo
- E-mail sent after protective stop was set. 

## Setup

### Requirements
- Python
- Gmail account _(If using email sender)_

### Instructions

1. Clone this repository into a directory of your choice with the following command:
     
   ```Console
   https://github.com/Shawn-Armstrong/RTDE_Python_Client_Library_Safety.git
   ```

2. Follow these [instructions](https://github.com/Shawn-Armstrong/Email_Sender#requirements) to setup a gmail account that can send emails. Add your information in `../record.py`. 

  ```Python
  email_sender = es.EmailSender(
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    username='<SENDER_EMAIL>@gmail.com',
    password='<YOUR_APP_PASSWORD>', # NOT your ordinary sign-in password; look at email-sender README.md.
    recipients=["recipient2@example.com", "recipient2@example.com"]
  )
  ```

3. Run the program with the following command using your robot's IPv4:
   
   ```Console
   cd RTDE_Python_Client_Library_Safety\examples
   python record.py --host YOUR_IPv4_GOES_HERE --frequency 10
   ```
