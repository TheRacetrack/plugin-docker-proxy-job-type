# Racetrack Plugin: Docker Proxy Job Type

This is a plugin for [Racetrack](https://github.com/TheRacetrack/racetrack)
which extends it with Dockerfile-based Job Type.

With Dockerfiles you can deploy any image to Racetrack
as long as it handles HTTP calls and adheres to few rules.
"docker-proxy" job type is intended to handle the HTTP calls to your Web server written 
in any programming language, enclosed in a docker image by Dockerfile recipe.

Racetrack requires compliance with a few principles that public Docker images don't meet out of the box.
That's why this job type comes with a proxy server that adheres to the Racetrack requirements and forwards the requests to the actual Docker container.

Dockerfile jobs should be used as a last resort. You should rather use job types
specifically dedicated to your language, if possible.

## Setup
1. Install `racetrack` client and generate ZIP plugin by running `make bundle`.

2. Activate the plugin in Racetrack Dashboard Admin page
  by uploading the zipped plugin file.

## Usage
You can deploy sample Dockerfile job by running:
```bash
racetrack deploy sample/docker-golang-http
```

See [how to use Dockerfile job type](./docs/job_docker.md).

# Development
Setup & activate Python venv (this is required for local development):

```bash
# in a project-root directory
make setup
. venv/bin/activate
```

# Releasing a new version
1. Make sure you have latest `racetrack` client.
2. Change the current version in a [plugin-manifest.yaml](./src/plugin-manifest.yaml)
3. Create ZIP plugin: `make bundle`

# Proxy modes
This plugin extends Racetrack with `docker-proxy` job type,
which creates a Job composed of two containers:  

1. proxy container - forwarding requests to your user-module, serving SwaggerUI and metrics,
2. user-module docker container - originating from a Dockerfile provided by you.

Now, some of your applications may run only on a root HTTP base path
and requires rewriting prefixes beforehand.
The others might work well with the original path.
Thus, there are 2 proxy modes of operation:

- **Forward** - Keeps original paths, forwards requests only to `/api/v1/*`,
  SwaggerUI served at root path.
- **Rewrite** - Trims prefixes from paths, proxy all requests (including root),
  can rewrite responses in customized manner.

"rewrite proxy" mode handles specific cases,
where you need to rewrite request path before forwarding it to your Docker container.

You can setup a configurable proxy, rewriting paths in responses (turning absolute paths into relative),
It allows to operate with Docker jobs like Drupal or Sphinx.

## How it works

Custom docker container might be your Drupal site defined in [Dockerfile](./sample-drupal/Dockerfile) 
in your job directory by simply putting `FROM drupal:9` or anything else.

However, Drupal runs on root endpoint (`/` base URL) and it cannot be changed easily, 
while Jobs are served at `/pub/job/<name>/<version>/` base URL.
That's why there is needed a proxy container which is a main entrypoint of a Job
and it receives traffic at `/pub/job/<name>/<version>/` 
and forwards it to your docker container,
rewriting URL (trimming the prefix).

Such rewrited URLs can be insidious as your docker container (Drupal) 
still thinks it is being served at root endpoint so it puts some URL addresses in HTML 
(eg. `/static/style.css`) as if it was really served at `/`.
That creates a lot of problems, cause when HTML gets rendered in your browser, 
your browser tries to access `/static/style.css` directly from Racetrack's PUB. 
That's not accessible as your job is being served at `/pub/job/<name>/<version>/`.
In other words, the proxy rewriting request paths isn't really transparent
and it can break some frontend applications.

On of the solutions to make it fully transparent is to do the following:  
Since the proxy rewrites URL (trims the prefix) when it receives the request, 
it should also transform URLs back (add the prefix) when the HTML response is being returned.

For instance, when Drupal returns `/static/style.css` URL, 
it should be transformed by the proxy to a valid address accessible by your 
browser from the outside, that is `/pub/job/<name>/<version>/static/style.css`

Now that the URL addresses can be located in different places in HTML of your Drupal site
and it may vary depending on the application,
you can customize the rewriting logic in a [proxy.py](./sample-drupal/proxy.py) file.
