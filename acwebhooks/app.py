"""
Grab the sample HTML for how Central webhooks are formatted.
Useful for writing scripts against webhooks sent from Aruba Central
"""
import os
import json
import logging
import requests

from bs4 import BeautifulSoup
# from rich.pretty import pprint

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# TODO Need to add Central versions
alerts_urls = {
    "AP_ALERTS_URL": [
        "AP",
        "https://help.central.arubanetworks.com/2.5.4/documentation/online_help/content/nms/api/webhook-ap-alerts.htm"
    ],
    "SW_ALERTS_URL": [
        "SWITCH",
        "https://help.central.arubanetworks.com/2.5.4/documentation/online_help/content/nms/api/webhook-switch-alerts.htm"
    ],
    "GW_ALERTS_URL": [
        "GATEWAY",
        "https://help.central.arubanetworks.com/2.5.4/documentation/online_help/content/nms/api/webhook-gateway-alerts.htm"
    ],
    "MISC_ALERTS_URL": [
        "MISC",
        "https://help.central.arubanetworks.com/2.5.4/documentation/online_help/content/nms/api/webhook-misc-alerts.htm"
    ]
}

def convert_to_json(title_element, textdata):
    """Fix broken JSON. This will add a missing "]" to the sample JSON provided by Aruba Central docs

    Args:
        textdata ([type]): [description]

    Returns:
        [type]: [description]
    """
    try:
        log.info("Attempting to convert item to JSON:  %s", title_element.text)
        jdict = json.loads(textdata.replace('\r\n', ''))
    except json.decoder.JSONDecodeError as err:
        # raise SystemExit(err) from err
        if "Expecting" in str(err):
            log.warning('%s: is missing trailing "]". Adding it manually to make it valid JSON. '
                'This is why you never paste JSON as raw text without validating it first.', title_element.text)
            jdict = json.loads(textdata.replace('\r\n', '') + "}")
        elif "Unterminated" in str(err):
            print(":::::", title_element.text)
            # print(textdata.replace('Priority 20480', 'Priority 20480"') + "]")
            log.warning('%s: is missing trailing \". Adding it manually to make it valid JSON. '
                'This is why you never paste JSON as raw text without validating it first.', title_element.text)
            if textdata.endswith('20480}'):
                updated = textdata[:-2] + '"}'
                jdict = json.loads(updated)

        else:
            log.error('%s broke the conversion', title_element.text)
            raise SystemExit(err) from err
    return jdict

def get_alerts(alerts):
    """Get HTML file with sample webhook JSON from Central

    Args:
        alerts ([list]): List of URLs to parse

    Returns:
        [dict]: Dict of sample webhook data (JSON)
    """
    device_type, alerts_url = alerts[0], alerts[1]
    log.info("Getting URL: %s", alerts_url)
    hookdata = {}
    page = requests.get(alerts_url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="contentBody")
    job_elements = results.find_all("div", class_="MCDropDown MCDropDown_Closed dropDown")
    for job_element in job_elements:
        title_element = job_element.find("a", class_="MCDropDownHotSpot dropDownHotspot MCDropDownHotSpot_ MCHotSpotImage")
        json_element = job_element.find("p", class_="CLI")
        jsonraw = json_element.text
        jsondata = convert_to_json(title_element, jsonraw.replace('\r\n', ''))
        hookdata[title_element.text] = jsondata
        hookdata['DEVICE_TYPE'] = device_type
    return hookdata

def writefiles(cver, fdata, DEBUG=None):
    """write JSON files

    Args:
        cver ([str]): Central Version
        fdata ([type]): Data to be writen to JSON file
        DEBUG ([int], optional): Set DEBUG for testing. This will NOT write files. Defaults to None.
    """
    PATH = "../" + cver
    isdir = os.path.isdir(PATH)
    if isdir is False:
        os.mkdir(PATH)
    for key, value in fdata.items():
        # fdir is file directory to create
        # prepend device type to the name (AP, SWITCH, GATEWAY, MISC)
        # replace spaces with _ for the file name, then append .json
        device_type = fdata["DEVICE_TYPE"]
        replacefslash = key.replace('\\', '_')
        replaceslash = replacefslash.replace("/", "_")
        fdir = PATH + "/" + device_type + "-" + replaceslash.replace(" ", "_") + ".json"
        log.info("Created :%s", fdir)
        if not DEBUG:
            with open(fdir, "w", encoding='utf-8' ) as f_json:
                json.dump(value, f_json)
        else:
            print(value)

if __name__ == "__main__":
    for alert_name, alert_url,  in alerts_urls.items():
        # pprint(get_alerts(alert_url), expand_all=True)
        get_alerts(alert_url)
        writefiles("2.5.4", get_alerts(alert_url))
