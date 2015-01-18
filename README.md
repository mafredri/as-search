# Search usign ASUSTOR Searchlight

This simple python script allows you to use ASUSTOR Searchlight (part of ADM) to search files on your NAS and get the
resulting output in JSON.

## Instructions

Copy config.ini.sample to config.ini and fill in:
* Host (the hostname or IP to your NAS)
* Account (your username on ADM)
* Passport OR Password (please look below if you would like to use Passport)

Then it's just a matter of running the script

```
python /path/to/as-search/search.py Hello world
```

### Using passport for authentication

If you would like to find out your ADM passport you need to log in to the NAS and select "Stay signed in".
After you have logged in, you can open up a javascript console in the webpage and type in the following command.

```
AS.util.cookie.get("as_passport")
```

## Disclaimer

Be careful if you have entered the wrong login details and enabled defender in ADM, too many incorrect attempt might
get you banned from your own NAS :)...
