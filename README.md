# Freckle CLI: A Command-Line Interface for Freckle Time Tracking
Provides a command-line timer for http://www.letsfreckle.com
 
## Configuration File
freckle.py depends on a short config file named `.freckle`.  It should reside in the same folder as freckle.py.

### Example config file
    [freckle_credentials] 
    base_url = https://yoursubdomain.letsfreckle.com/api
    api_key  = keygeneratedbyfreckle
    user     = user@account.com

For help on getting your API key, check out the [Freckle docs](http://letsfreckle.com/help/#faq_40)                                                                                          
## Running the script
Simply call `python freckle.py` from the folder the script resides in. If authentication succeeded, you'll be presented with an options menu. Current functionality includes: a utility that outputs hours you've logged today and an interactive timer.

Choose your project and enter 'start' to start the timer. When you're done with that time entry, enter 'stop' and your time will be updated in Freckle. 