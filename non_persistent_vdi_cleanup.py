# This example script should be run on a recurring basis (suggest 1X daily)
# using a scheduling tool of your choice. It queries the server for devices,
# then iterates through them and finds ones that match your defined criteria
# for identifying offline non-persistent VDI devices which are consuming a
# license. When matches are found, it then requests an uninstall of those
# devices. This results in the Deployment Status on those devices moving to
# Pending Uninstall, which immediately releases the license(s) consumed and
# hides the devices from the Dashboard and any views or queries that display
# only devices with an activated license.

import deepinstinct3 as di, datetime

# Server configuration
di.fqdn = 'FOO.customers.deepinstinctweb.com'
di.key = 'BAR'

# Get device data from DI server
devices = di.get_devices(include_deactivated=False)

# Get current time and store as variable
now = datetime.datetime.utcnow()

# Define a list to store devices which meet criteria to be removed
devices_to_remove = []

# Inspect device data and build list of devices to be removed
# In the nested if blocks below, only devices which meet ALL criteria will be removed.
# You'll need to adjust this area of the code to match your specific use case(s).
# Open https://{fqdn}/api/v1/ in a web browser and reference the specification for
# the 'DeviceList' model to see all available fields and possible values.
for device in devices:
    if 'tag' in device:   #needed to avoid KeyError for devices with no tag
        if device['tag'] == 'Your VDI Device Tag': #substitute actual device tag that you use for VDI devices
            if device['group_name'] == 'Your VDI Device Group Name':  #substitute actual group name for your VDI devices
                if device['connectivity_status'] == 'OFFLINE': #only include offline devices
                    if device['deployment_status'] == 'REGISTERED': #filtering on registered avoids duplicate requests
                        #convert last_contact form server to a Python datetime object
                        last_contact = datetime.datetime.fromisoformat(device['last_contact'].replace('Z',''))
                        #check if device's last_contact is long enough ago to meet criteria
                        #you can customize the timedelta below (default 12 hours)
                        if (now - last_contact) > datetime.timedelta(hours=12):
                            #all criteria above were met, therefore adding current device to the removal list
                            devices_to_remove.append(device)

# Process the list of devices which were identified for removal
for device in devices_to_remove:
    
    print('Requesting uninstall of device', device['id'], device['hostname'])
    di.remove_device(device)
    
    #NOTE: Uncomment the lines below to also archive (hide from GUI and REST API) the devices
    #print('Archiving device', device['id'], device['hostname'])
    #di.archive_device(device)
