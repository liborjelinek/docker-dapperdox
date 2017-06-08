# Dapperdox dockerized

[Dapperdox](http://dapperdox.io/) is OpenAPI (formerly known as Swagger) document generator. This is source for its Docker image.

## About Dapperdox

_For in-depth documentation how to write a new content see [Dapperdox authoring content concepts](http://dapperdox.io/docs/author-concepts)._

Dapperdox is tool for documenting APIs. Every API documentation can contain

* textual guides in [GFM Markdown](https://guides.github.com/features/mastering-markdown/) 
* API reference in [OpenAPI](http://swagger.io/specification/) (formerly known as Swagger)

Dapperdox combines both into single documentation website.

Guides, themes and overlays are by default collectively called "assets". Directory with `swagger.json` specification is called "specdir".

## Dapperdox sources organization

By default image expects the following Dapperdox source file system organization:

    my_docs/
        assets/
            ...
        specs/
            swagger.yaml
            
Organization of assets dir is described in [authoring contepts](http://dapperdox.io/docs/author-concepts)

## Convert swagger.yaml to swagger.json

Dapperdox can read only OpenAPI spec in JSON (`swagger.json`) but most people prefer YAML (`swagger.yaml`) which is easier for humans.
 
This image contains Python script to convert YAML to JSON that convert `swagger.json` to `swagger.yaml` in your specdir. To call it, execute command similar to this:

    $ docker run --rm --name yaml_to_json.py \
            -v ~/path/to/my/specdir:/dapperdox/specs \
            bircow/dapperdox \
            yaml_to_json.py /dapperdox/specs

Where with `-v` you map your specdir with `swagger.yaml` to `/dapperdox/specs` inside container and pass this directory to the script. 

Script will override `swagger.json` if it already exists!

## Running
 
To run Dapperdox website from this image you must:

* choose host machine port - Dapperdox runs on 3123 and it's best to use the same on host
* map your Dapperdox sources (assets and specification) to `/dapperdox/` in container
* choose container meaningful name like 'developer-docs`

In words of commandline e.g.:

    $ docker run --rm --name developer-docs \
            -p 3123:3123 \
            -v ~/git/developer-docs/:/dapperdox \
            bircow/dapperdox

Then go to http://localhost:3123 in your web browser and enjoy!

## Configuration

By default specdir is set to `/dapperdox/specs` and assets to `/dapperdox/assets`. If you organize your Dapperdox sources to contain subfolders `specs` and `assets`, as recommended above, you don't have to modify these settings.

You can configure Dapperdox running inside container via environment variables. Equivalent variable names for commandline options is found in [Dapperdox configuration guide](http://dapperdox.io/docs/configuration-guide).

To override or change configuration, for example to change a theme, set environment variable `THEME` with `-e`:

    $ docker run --rm --name developer-docs \
            -p 3123:3123 \
            -v ~/git/developer-docs/:/dapperdox \
            -e "THEME=my_theme" \
            bircow/dapperdox