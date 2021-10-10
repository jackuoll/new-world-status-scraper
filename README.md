# New World - Status API (Scraper)

### What does this do?

This scrapes the site https://www.newworld.com/en-us/support/server-status and returns the status of each world in JSON format. 

Example format:

```
{
  "US East": {
    "Aarnivalkea": "up",
    "Adlivun": "full",
    ...
```

I wrote this so that I could write a bot to easily check when a world becomes free for character transfer/creation.

### How to run it?

Install the requirements and run `uvicorn main:app` to start a development server. If you want to productionise this properly you'll have to do it yourself. Personally I am just running it as a service on ubuntu as pure python.

The status page will be available on http://127.0.0.1:8000/
