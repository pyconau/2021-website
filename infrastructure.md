# Archive Infrastructure

This repo now lives as an archive of the original website without automation. 

For publishing updates, run the contents of the build steps in `netlify.yml`, then push the generated `public/` folder to the gh-pages branch: 

```
git subtree push --prefix public origin gh-pages
```

# Original Infrastructure

[Statik](https://github.com/thanethomson/statik) uses data models to assist in developing a staticly generated website.
 

## Models

A number of models are defined in this repo. For each model, there are multiple files separated into folders of like type: 

 * `views/`
   * defines a path, context (all elements of a model (below), or a single model instance), and a template (below). 
 * `templates/`
   * defined using jinja templating
 * `models/`
   * defines a model with various keys and datatypes, in yaml
 * `data/`
   * defintes instances of a model, using the model datatypes, in yaml
 
 
The currently defined models are: 
 
 * `Page`: Static pages (the most common for the structure of the wesbite)
 * `News`: posts in `/news`
 * `Person`: people, usually organisers or speakers
 * `Track`: a track of talks, with one or more organisers defined as a `Person`.
 * `Session`: a talk, with one or more speakers defined as a `Person`, and a track defined in `Track`.
 * `Sponsor`: a sponsor, which may have a workshop
 * `Workshop`: a sponsor workshop
 * `SpecialSponsor`: a node for additional listings on the Sponsor page. 


Full details are always more current in the code. 


## Infrastructure

There are some other folders of stuff: 

 * `assets/`:
   * `people/`: avatars of instances of `Person`
   * `sponsor-logos`: logos of instances of `Sponsor`
   * `diagrams/`, misc images
* `frontend/`: sass (high level CSS) and typescript (high level javascript) things that power the pretty. 


## Redirects and config as code

Some of these files are important. Of important note: 

* `_redirects`: defines domain for annual websites. 
* `.github`: defines GitHub actions
* `netlify.toml`: defines page redirects, and build commands
* `config.yaml`: the main page's `Page` definition.
* `package.json` and `yarn.lock`: defines JavaScript dependencies for the front end.
* `pyproject.toml` and `poetry.lock`: defines Python dependencies for the back end.
* `tsconfig.json`: configuration for typescript
* `.pre-commit-config.yaml` and `.prettierrc`: a precommit config to check for linting and other errors before committing (not automatically run)

   
## Local Infrastructure

If you are developing locally a number of other folders will appear. 

These are explicitly defined in `.gitignore` and *should not be committed to the repository*. 

* `node_modules/`: local JavaScript packages
* `public/`: the locally built version of the website
* `assets/build/`: compiled front-end bits
* `.cache/`: local cache
