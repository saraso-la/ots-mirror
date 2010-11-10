# ***** BEGIN LICENCE BLOCK *****
# This file is part of OTS
#
# Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
#
# Contact: Mikko Makinen <mikko.al.makinen@nokia.com>
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

import time

import StringIO

from zipfile import ZipFile
from zipfile import ZipInfo
from zipfile import ZIP_DEFLATED

from email import encoders
from email.mime.base import MIMEBase

##########################################
# PRIVATE METHODS
##########################################

def _zip_info(environment, name):
    """
    @type environment : C{str}
    @param environment : The environment name

    @type name : C{str}
    @param name : The name of the file

    @rtype : C{ZipInfo}
    @param : The Zip Info 
    """
    filename = "%s-%s" % (environment, name)
    info = ZipInfo(filename)
    info.date_time = time.localtime(time.time())[:6] #now
    info.external_attr = 0666 << 16L # read-write access to everyone
    info.compress_type = ZIP_DEFLATED
    return info    

def _zip_file(testrun_uuid, results_list):
    """
    @type testrun_uuid : C{str}
    @param testrun_uuid : The Testrun uuid

    @type results : C{list} of C{ots.common.dto.results}
    @param results : The results

    @rtype : C{StringIO}
    @param : The Zipped File
    """
    string_io = StringIO.StringIO()
    zip_file = ZipFile(string_io, 'w')
    for results in results_list:
        file = results.results_xml
        env = results.environment
        info = _zip_info(env.environment, results.results_xml.name)
        zip_file.writestr(info, file.read())
    zip_file.close()
    string_io.seek(0)
    return string_io

def _zip_name(testrun_uuid):
    """
    @type testrun_uuid : C{str}
    @param testrun_uuid : The Testrun uuid
    
    @rtype : C{str}
    @rparam : The name of the zipfile
    """
    return 'OTS_testrun_%s.zip' % testrun_uuid

#############################################
# ATTACHMENT
#############################################

def attachment(testrun_uuid, results_list):
    """
    Create a zip file containing result files
    
    @type testrun_uuid : C{str}
    @param testrun_uuid : The Testrun uuid

    @type results : C{list} of C{ots.common.dto.results}
    @param results : The results

    @rtype : C{MIMEBase}
    @param : The attachment
    """ 
    zipped_content = _zip_file(testrun_uuid, results_list).read()
    ctype = 'application/zip'
    maintype, subtype = ctype.split('/', 1)
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(zipped_content)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', 
                          filename = _zip_name(testrun_uuid))
    return attachment