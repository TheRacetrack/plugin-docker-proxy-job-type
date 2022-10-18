# Racetrack Plugin: Docker HTTP Job Type

This is a plugin for [Racetrack](https://github.com/TheRacetrack/racetrack)
which extends it with Dockerfile-based Job Type.

Dockerfile jobs should be used as a last resort. You should rather use job types
specifically dedicated to your language if possible.

"docker-http" job type is intended to handle the calls to your Web server written 
in any programming language, enclosed in a docker image by Dockerfile recipe.

## Setup
1. Make sure you have cloned the racetrack submodule. If not run: `make init`

2. Install `racetrack` client and generate ZIP plugin by running `make bundle`.

3. Activate the plugin in Racetrack Dashboard Admin page
  by uploading the zipped plugin file.

## Usage
You can deploy sample Dockerfile job by running:
```bash
racetrack deploy sample/docker-golang-http <RACETRACK_URL>
```

# Development
Setup & activate Python venv (this is required for local development):

```bash
# in a project-root directory
make setup
. venv/bin/activate
```

# Releasing a new version
1. Make sure you're ready to go with `make init` and `. venv/bin/activate`
2. Change the current version (`TAG`) in a [Makefile](./Makefile)
3. Update latest racetrack submodule: `make update-racetrack-submodule`
4. Create ZIP plugin: `make bundle`
