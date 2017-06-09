# Dapperdox dockerized

[Dapperdox](http://dapperdox.io/) is beautiful, integrated, OpenAPI (Swagger) documentation generator
. This is source for its Dockerized image.

## Versions

I support only latest Dapperdox version (currently 1.1.1). It is published under both `bircow/dapperdox:latest` and `bircow/dapperdox:1.1.1`.

## About Dapperdox

_For in-depth documentation how to write a new content see [Dapperdox authoring content concepts](http://dapperdox.io/docs/author-concepts)._

Dapperdox is tool for documenting APIs. Every API documentation can contain

* textual guides in [GFM Markdown](https://guides.github.com/features/mastering-markdown/) 
* API reference in [OpenAPI](http://swagger.io/specification/) (formerly known as Swagger)

Dapperdox combines both into single documentation website.

Guides, themes and overlays are by default collectively called _"assets"_. Directory with `swagger.json` specification is called _"specdir"_.

## Recommended Dapperdox project organization and running

Default Dapperdox image configuration expects the following Dapperdox source file system organization:

    my_docs/
        assets/
            ...
        specs/
            swagger.yaml
        Dockerfile

Organization of assets dir is described in [authoring contepts](http://dapperdox.io/docs/author-concepts).
            
Most people usually author Swagger in YAML. Unfortunately Dapperdox supports only Swagger specification in JSON format. Fortunately Dapperdox image contains utility script that can converts `swagger.yaml` to `swagger.json` before running Dapperdox.

Recommended way how to run project is create your own Docker image containing assets and specs that derive from `bircow/dapperdox`. Start with `Dockerfile` in your root with these few lines:

    FROM bircow/dapperdox:1.1.1
    
    # Customize your assets or specs dir names
    COPY assets/ $ASSETS_DIR
    COPY specs/ $SPEC_DIR

    # If you write in YAML convert swagger.yaml to JSON
    RUN yaml_to_json.py $SPEC_DIR
    
    # Custom configuration comes here
    # ENV THEME my_own_theme
    
    # Launch Dapperdox on 0.0.0.0:3123
    CMD ["go-wrapper", "run"]
 
Build your image

    $ docker build -t my_docs .
    
To run, choose only free network port on your computer mapped to 3123 in container. Best is to use Dapperdox default port 3123. For example:

    $ docker run --rm --name my_docs \
            -p 3123:3123
            my_docs
            
Open http://localhost:3123 in your browser and enjoy!

## Running from bircow/dapperdox Docker image manually

Alternative to above method is running YAML to JSON and Dapperdox manually from `bircow/dapperdox` image.  

If you author Swagger file in YAML, execute the command similar to this to convert `swagger.yaml` to `swagger.json`:

    $ docker run --rm --name yaml_to_json.py \
            -v ~/path/to/my_docs/specs:/dapperdox/specs \
            bircow/dapperdox \
            yaml_to_json.py /dapperdox/specs

Where with `-v` you map your specdir with `swagger.yaml` to `/dapperdox/specs` inside container and pass this directory to the script. 

For the example above, the script will create (or override) `~/path/to/my_docs/specs/swagger.json`.

To run Dapperdox website from this image you must:

* choose host machine port - Dapperdox runs on 3123 and it's best to use the same on host
* map your Dapperdox sources (assets and specification) to `/dapperdox/` in container
* choose container meaningful name like 'developer-docs`

In words of commandline e.g.:

    $ docker run --rm --name developer-docs \
            -p 3123:3123 \
            -v ~/path/to/my_docs:/dapperdox \
            bircow/dapperdox

Then go to http://localhost:3123 in your web browser and enjoy!

### Configuration

By default specdir is set to `/dapperdox/specs` and assets to `/dapperdox/assets`. If you organize your Dapperdox sources to contain subfolders `specs` and `assets`, as recommended above, you don't have to modify these settings.

You can configure Dapperdox running inside container via environment variables. Equivalent variable names for commandline options is found in [Dapperdox configuration guide](http://dapperdox.io/docs/configuration-guide).

To override or change configuration, for example to change a theme, set environment variable `THEME` with ENV in your derived Dockerfile:
 
    ...
    ENV THEME my_theme
    ...

or, if running manually, with with `-e` parameter:

    $ docker run --rm --name developer-docs \
            -p 3123:3123 \
            -v ~/path/to/my_docs:/dapperdox \
            -e "THEME=my_theme" \
            bircow/dapperdox