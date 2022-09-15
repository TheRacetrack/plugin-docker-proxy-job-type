# Racetrack Plugin: Docker Proxy Job Type

A Racetrack plugin allowing to deploy Docker Proxy jobs (like Drupal) to
[Racetrack](https://github.com/TheRacetrack/racetrack)

## Setup
1. Make sure that current version of language wrapper docker image
  (provided by plugin) is pushed to your Docker registry,
  which is used by your Racetrack instance. 
  - Do it by pushing to public registry: `make push`  
  - or if you want to use private registry, run `make env-template`,
  fill in `.env` file and run `make push-private-registry`.
  - If you wish to work on that locally, also run `make push-local`.

2. [Install racetrack-plugin-bundler](https://github.com/TheRacetrack/racetrack/blob/master/utils/plugin_bundler/README.md)
  and generate ZIP plugin by running `make bundle`.

3. Activate the plugin in Racetrack Dashboard Admin page
  by uploading the zipped plugin file.

## Usage
You can deploy sample Drupal job by running:
```bash
racetrack deploy sample-drupal <RACETRACK_URL>
```

## How it works

This plugin extends Racetrack with `docker-proxy` job type,
which creates a Fatman composed of two containers:  
1. proxy container
2. custom docker container.

Custom docker container might be your Drupal site defined in [Dockerfile](./sample-drupal/Dockerfile) 
in your fatman directory by simply putting `FROM drupal:9` or anything else.

However, Drupal runs on root endpoint (`/` base URL) and it cannot be changed easily, 
while Fatmen are served at `/pub/fatman/<name>/<version>/` base URL.
That's why there is needed a proxy container which is a main entrypoint of a Fatman
and it receives traffic at `/pub/fatman/<name>/<version>/` 
and forwards it to your docker container,
rewriting URL (trimming the prefix).

Such rewriting URLs can be insidious as your docker container (Drupal) 
still thinks it is being served at root endpoint so it puts some URL addresses in HTML 
(eg. `/static/style.css`) as if it was really served at `/`.
That creates a lot of problems, cause when HTML gets rendered in your browser, 
your browser tries to access `/static/style.css` directly from Racetrack's PUB. 
That's not accessible as your fatman is being served at `/pub/fatman/<name>/<version>/`.
In other words, the proxy rewriting request paths isn't really transparent
and it can break some frontend applications.

On of the solutions to make it fully transparent is to do the following:  
Since the proxy rewrites URL (trims the prefix) when it receives the request, 
it should also transform URLs back (add the prefix) when the HTML response is being returned.

For instance, when Drupal returns `/static/style.css` URL, 
it should be transformed by the proxy to a valid address accessible by your 
browser from the outside, that is `/pub/fatman/<name>/<version>/static/style.css`

Now that the URL addresses can be located in different places in HTML of your Drupal site
and it may vary depending on the application,
you can customize the rewriting logic in a [proxy.py](./sample-drupal/proxy.py) file.
