"""
Copyright 2010 – 2024 Rocket Software, Inc. or its affiliates. 
This software may be used, modified, and distributed
(provided this notice is included without modification)
solely for internal demonstration purposes with other
Rocket® products, and is otherwise subject to the EULA at
https://www.rocketsoftware.com/company/trust/agreements.

THIS SOFTWARE IS PROVIDED "AS IS" AND ALL IMPLIED
WARRANTIES, INCLUDING THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE,
SHALL NOT APPLY.
TO THE EXTENT PERMITTED BY LAW, IN NO EVENT WILL
ROCKET SOFTWARE HAVE ANY LIABILITY WHATSOEVER IN CONNECTION
WITH THIS SOFTWARE.

Description:  Functions for configuration of MFDS lists on the server region.
"""

MFDS_CONFIG_ENDPOINT = 'server/v1/config/mfds'

def check_mfds_list(session):
    """ Check the MFDS list of a region server. """
    res = session.get(MFDS_CONFIG_ENDPOINT, 'Unable to complete Check MFDS API request.')
    return res

def add_mfds_to_list(session, mfds_host, mfds_port, mfds_description):
    """ Add an MFDS to a region server. """
    req_body = {
        'MfdsHost': mfds_host,
        'MfdsPort': mfds_port,
        'MfdsIdentifier': mfds_host,
        'MfdsDescription': mfds_description
    }
    res = session.post(MFDS_CONFIG_ENDPOINT, req_body, 'Unable to complete Add MFDS API request.')
    return res