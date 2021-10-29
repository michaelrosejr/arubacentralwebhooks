# Aruba Central Webhook sample files in JSON

This repo is a simple storage location for the output that Aruba Central's webhooks output. It is generated from the samples from the Aruba Central home page. These files can be used to import into your tool to parse the webhooks received from Aruba Central. 

There are number of JSON errors in the documentation as well. This script attempts to fix those JSON errors.Please see the output.log for any JSON errors that were generated and alerts that may have been skipped due to those errors.

## Installation

The JSON files are located in the version number that they were created for, which was 2.5.4 at the time of this documentation. Search for your Central version, and within the folder should be the files for your version of Central.


## Links
[Aruba Central 2.5.4 Webhook Documentation](https://help.central.arubanetworks.com/latest/documentation/online_help/content/nms/api/api_webhook.htm?Highlight=webhooks)

## Updates

This repo will automatically update when it detects a new version of Central and/or an update to the documents, assuming it doesn't generate an error. As you'll see in the code, this is parsing HTML as Aruba Central doesn't document the all the webhook outputs, even though they're already in JSON.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)