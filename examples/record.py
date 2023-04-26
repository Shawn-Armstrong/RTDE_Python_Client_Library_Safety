#!/usr/bin/env python
# Copyright (c) 2020-2022, Universal Robots A/S,
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Universal Robots A/S nor the names of its
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL UNIVERSAL ROBOTS A/S BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import argparse
import logging
import sys

sys.path.append("..")
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
import EmailSender as es
import datetime

# Put your information here; this is all you need to do.
# Check email-sender README.md.
email_sender = es.EmailSender(
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    username='<SENDER_EMAIL>@gmail.com',
    token_password='<YOUR_APP_PASSWORD>', # NOT your ordinary sign-in password; look at email-sender README.md.
    recipients=["recipient2@example.com", "recipient2@example.com"]
)


def safety_status_bits_to_dict(value):
    
    safety_conditions = [
        "Is normal mode",
        "Is reduced mode",
        "Is protective stopped",
        "Is recovery mode",
        "Is safeguard stopped",
        "Is system emergency stopped",
        "Is robot emergency stopped",
        "Is emergency stopped",
        "Is violation",
        "Is fault",
        "Is stopped due to safety"
    ]
    
    safety_dict = {}
    for i, condition in enumerate(safety_conditions):
        safety_dict[condition] = bool(value & (1 << i))
    
    return safety_dict

def safety_dict_to_html(safety_dict):

    html_lines = []

    for key, value in safety_dict.items():
        html_lines.append(f"<p>{key}: {value}</p>")
    return "\n".join(html_lines)


def send_safety_notification(safety_data, email_sender):
    safety_dict_html = safety_dict_to_html(safety_data)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = email_sender.create_message(
                        subject=f"RTDE NOTIFICATION: {current_time}", 
                        html_content= f'''
                        <h1>ROBOT RTDE WARNING</h1>
                        <p>A safety related stop has occurred.
                        {safety_dict_html}</p>
                        ''')
    email_sender.send_email(message)

    print("Notification sent.")


# parameters
parser = argparse.ArgumentParser()
parser.add_argument(
    "--host", default="localhost", help="name of host to connect to (localhost)"
)
parser.add_argument("--port", type=int, default=30004, help="port number (30004)")
parser.add_argument(
    "--frequency", type=int, default=125, help="the sampling frequency in Herz"
)
parser.add_argument(
    "--config",
    default="record_configuration.xml",
    help="data configuration file to use (record_configuration.xml)",
)
parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
parser.add_argument(
    "--buffered",
    help="Use buffered receive which doesn't skip data",
    action="store_true",
)
parser.add_argument(
    "--binary", help="save the data in binary format", action="store_true"
)
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.INFO)

conf = rtde_config.ConfigFile(args.config)
output_names, output_types = conf.get_recipe("out")

con = rtde.RTDE(args.host, args.port)
con.connect()

# get controller version
con.get_controller_version()

# setup recipes
if not con.send_output_setup(output_names, output_types, frequency=args.frequency):
    logging.error("Unable to configure output")
    sys.exit()

# start data synchronization
if not con.send_start():
    logging.error("Unable to start synchronization")
    sys.exit()

is_running = True
while is_running:

    try:
        if args.buffered:
            state = con.receive_buffered(args.binary)
        else:
            state = con.receive(args.binary)

        # Extract safety bits
        safety_data = safety_status_bits_to_dict(state.safety_status_bits)
        
        # Ensure robot is nominal; otherwise, send email.
        if safety_data["Is normal mode"] == False:
            send_safety_notification(safety_data, email_sender)
            sys.exit() 

    except KeyboardInterrupt:
        is_running = False
    except rtde.RTDEException:
        con.disconnect()
        sys.exit()

con.send_pause()
con.disconnect()
