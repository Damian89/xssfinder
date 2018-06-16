# Tools for finding simple xss

Some simple helper scripts which I'm using frequently for finding xss - using those scripts I was able to find xss on some Netflix, Toyota and Starbucks subdomains.

## checkGivenParameters.py

__How to execute:__

```
python3 checkGivenParameters.py -url "http://victim/?param1=test&param2=test2&foo=bar" -payload '[XSS"]'
```

This script...
- searches for inputs, textareas, selects, buttons and uses their name/id values as additional get parameters
- replaces every get value with the given payload and checks if its reflected in the http body

Optional parameters:
- payload

### Hints
Using the default payload may result in a lot of false results.

## checkRandomParameters.py

__How to execute (Way 1):__

```
python3 checkRandomParameters.py -url "http://victim/" -payload '[XSS"]' -paramlist /path/to/params.txt -threads 10 -timeout 3600 --verbose --extended
```

This scripts...
- searches for inputs, textareas, selects, buttons and uses their name/id as additional get parameters
- takes every parameter (custom + wordlist) and appents it with the payload as value to the url and then checks, if the payload is reflected

Optional parameters:
- payload
- paramlist
- threads
- timeout
- verbose
- extended

__Extended mode__
Using the "--extended" flag will result in aditional checks if a parameter is found to be reflected.


### Hints
Some websites reflect the requested url this results in a lot false results WHEN the payload is something very simple like "abcdefg27sjs93" - see netflix.com or uber.com for instance. Thats why I'm not using the standard alphanumerical payload and instead choosing something like 'XSS">' or 'XSS"'. In that case I wouldnt also use the extended mode (because you basically doing extended search). If you have a victim where the request url is not reflected you should use the extended flag with a simple playload like the default one.

## Wordlist

Thanks to Daniel Miessler for the parameter wordlist: https://github.com/danielmiessler/SecLists
I added some custom parameters ;)