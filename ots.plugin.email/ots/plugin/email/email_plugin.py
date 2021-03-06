# ***** BEGIN LICENCE BLOCK *****
# This file is part of OTS
#
# Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
#
# Contact: meego-qa@lists.meego.com
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# version 2.1 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA
# ***** END LICENCE BLOCK *****

"""
The EmailPlugin is a Publisher 

That sends an email of the email of the Test Results.

Requires an SMTP server 
"""

import os
import logging
import smtplib
import configobj
import socket

#from ots.server.server_config_filename import server_config_filename
from ots.common.framework.api import PublisherPluginBase
from ots.plugin.email.mail_message import MailMessage 

DEFAULT_CONFIG_FILE = '/etc/ots/plugins/email.conf'
LOG = logging.getLogger(__name__)

ON = "on"

##############################
# EmailPlugin
##############################

class EmailPlugin(PublisherPluginBase):
    """
    Email Plugin is an OTS Publisher  

    Builds email message from templates
    and the results of a Testrun
    
    Sends the email to the `notify_list`
    """

    def __init__(self, request_id, testrun_uuid, sw_product, image,
                 email = None,
                 email_attachments = None,
                 build_url = None,
                 notify_list = None,
                 **kwargs):
        """
        @type request_id: C{str}
        @param request_id: An identifier for the request from the client

        @type testrun_uuid: C{str}
        @param testrun_uuid: The unique identifier for the testrun

        @type sw_product: C{str}
        @param sw_product: Name of the sw product this testrun belongs to

        @type image : C{str}
        @param image : The URL of the image
        
        @type email : C{str}
        @param email : str switch for email where `on` is True

        @type email_attachments : C{str}
        @param email_attachments : str switch for attachments where `on` is True

        @type build_url : C{str}
        @param build_url : The build url

        @type notify_list : C{list}
        @param notify_list : The list of email recipients to notify
        """
        self._request_id = request_id
        self.testrun_uuid = testrun_uuid
        self.sw_product = sw_product
        self.image = image
        self._build_url = build_url
        config_file = _config_filename()

        config = configobj.ConfigObj(config_file).get("ots.email_plugin")
        #
        self._email = email
        self._email_attachments = email_attachments
        #
        self._mail_message = None
        #
        self._source_uris = {}
        self._testrun_result = None
        self._results = None
        self._exception = None
        self._tested_packages = []
        self._notify_list = notify_list

        self._from_address = config["from_address"]
        self._message_body = config["message_body"]
        self._smtp_server = config["smtp_server"]
        self._message_subject = config["message_subject"]
        
        LOG.info("ots.plugin.email loaded")
        if config.as_bool("disabled"):   # If email plugin is disabled overwrite
            self._email = "off"          # option
        

    ##########################################
    # DEFAULTED PROPERTIES
    ##########################################

    @property
    def is_email_on(self):
        """
        Is the email switched on?
        @rtype: C{bool}
        """
        return self._email == ON

    @property
    def is_email_attachments_on(self):
        """
        Is the email attachment switched on?
        @rtype: C{bool}
        """
        return self._email_attachments == ON

    @property
    def build_url(self):
        """
        The build url
        @rtype: C{str}
        """
        if self._build_url is not None:
            return str(self._build_url)
        return '%s'
        
    @property
    def request_id(self):
        """
        The request_id
        @rtype: C{str}
        """
        if self._request_id is not None:
            return str(self._request_id)
        return ''

    @property 
    def notify_list(self):
        """
        The email notify list
        @rtype: C{list}
        """
        if self._notify_list is not None:
            return self._notify_list 
        return []

    ###############################################
    # MAIL MESSAGE
    ##############################################

    @property
    def mail_message(self):
        """
        Mail message
        @rtype: C{str}
        """
        if self._mail_message is None:
            self._mail_message = MailMessage(self._from_address,
                                             self._message_body,
                                             self._message_subject)
        message = self._mail_message.message(self.request_id, 
                                             self.testrun_uuid, 
                                             self.sw_product,
                                             self._testrun_result,  
                                             self._results, 
                                             self._exception, 
                                             self._tested_packages, 
                                             self._source_uris,
                                             self.notify_list, 
                                             self.is_email_attachments_on,
                                             self.build_url)
        return message.as_string()
        
      
    #################################################
    # OVERRIDES
    #################################################


    def set_all_publisher_uris(self, uris_dict):
        """
        @type uris_dict: C{dict} of C{str} : C{str}
        @param uris_dict: Uris of other reporting tools 
        """
        self._source_uris = uris_dict
    
    def set_testrun_result(self, testrun_result):
        """
        @type testrun_result: C{str}
        @param testrun_result: The testrun result
        """
        
        self._testrun_result = testrun_result

    def set_results(self, results):
        """
        @type results : C{list} of C{ots.common.dto.results}
        @param results : The Results
        """
        self._results = results

    def set_exception(self, exception):
        """
        @type exception: C{Exception}
        @param exception: The Exception
        """
        self._exception = exception

    def set_tested_packages(self, packages):
        """
        @type packages : C{ots.common.dto.packages}
        @param packages: The Test Packages that were run
        """
        self._tested_packages = packages

    def publish(self,):
        """
        Sends the email
        """
        if not self.is_email_on:
            LOG.info("email plugin disabled")
            return
        
        if type(self._notify_list) is list:
            failed_addresses = None
            mail_server = None
            server_url = self._smtp_server
            LOG.info( "Using smtp server: '%s'"%(server_url) )
            try:
                mail_server = smtplib.SMTP(server_url)
                failed_addresses = mail_server.sendmail(self._from_address,
                                                        self._notify_list, 
                                                        self.mail_message)
                LOG.info( "Email sent" )
            except smtplib.SMTPRecipientsRefused:
                LOG.error("SMTP refused error", exc_info=True)
                failed_addresses = self._notify_list
            except socket.gaierror:
                LOG.warning("Invalid or unknown SMTP host")
            finally:
                if mail_server is not None:
                    mail_server.close()
            if failed_addresses:
                LOG.warning("Error in sending mail to following addresses: %s"\
                                % failed_addresses)
        else:
            LOG.warning("No address list")

def _config_filename():
    """
    Returns the config file path.
    """
    if os.path.exists(DEFAULT_CONFIG_FILE):
        return DEFAULT_CONFIG_FILE
    
    distributor_dirname = os.path.dirname(os.path.abspath(__file__))
    distributor_config_filename = os.path.join(distributor_dirname,
                                               "email.conf")

    if not os.path.exists(distributor_config_filename):
        raise Exception("%s not found"%(distributor_config_filename))
    return distributor_config_filename

    #else:
    #    raise Exception("Email plugin configuration file %s not found"%(DEFAULT_CONFIG_FILE))

