# PyConline AU 2021 website

This website is generated using [statik](https://github.com/thanethomson/statik) with automatic deployments by [Netlify](https://www.netlify.com/)

For more information, see [infrastructure.md](infrastructure.md)

## Submitting changes

Pull requests submitted to this repo automatically generate change previews using [Netlify](https://www.netlify.com/). Click the "**deploy/netlify**" check link to see your preview. 

## Local development

If your change is larger and you require a local development environment you will require a number of programs. 

Links provided favour macOS using [Homebrew](https://brew.sh/), but will refer to general download information as well. 

* **[Python 3.7](https://www.python.org/downloads/)** minimum
  * we recommend installing via [pyenv](https://github.com/pyenv/pyenv) ([brew](https://formulae.brew.sh/formula/pyenv) or [download](https://github.com/pyenv/pyenv#installation))
* **[Node.js](https://nodejs.org/en/)** ([brew](https://formulae.brew.sh/formula/node) or [download](https://nodejs.org/en/download/))
* **[Poetry](https://python-poetry.org)** ([brew](https://formulae.brew.sh/formula/poetry) or [downoad](https://python-poetry.org/docs/#installation))

Once installed, fork this repo and clone, then to install this codebase's dependencies:

```shell
poetry install   # python dependencies, creates virtualenv for you
yarn install     # javascript dependencies
```

Finally, start the local webserver: 

```shell
poetry run supervisord
```

## Changes from previous years

2021 is running with a home timezone of "+10:00". It still uses some of the [timezone hacks](https://github.com/pyconau/2020-website#timezones) from 2020, but without the half hour offset. 

However, all times should still be written as completely as possible. 

```
<time datetime="2021-07-16T08:00+10:00">
	Friday 16 July, 8:00am AEST
</time>
```

The site has some JavaScript that will pick this up, and if the user's timezone differs from the one in the timestamp, append the local time. (For instance, they might see _Friday 16 July, 8:00am AEST (10:00am NZST)_ or _Friday 16 July, 8:00am ACST (Thurs, 7:00pm ET)_.)

This works in HTML and Markdown (since Markdown can have arbitrary HTML in most places).

Note that the colon between the offset hours and minutes **must be present** (e.g. `+1000` won't work)!

## Issues with local development

### macOS issues with `API_UNAVAILABLE`

If you are running macOS Catalina and getting hundreds of `API_UNAVAILABLE`/`clang` issues when running `poetry install`, try [this tip](https://github.com/gorakhargosh/watchdog/issues/628#issuecomment-581480649):

- Check how many SDKs you have installed: 

  ```
  ls /Library/Developer/CommandLineTools/SDKs
  ```
- If you have both `MacOSX10.14.sdk` and `MacOSX10.15.sdk`, remove the older version:

  ```
  rm -rf /Library/Developer/CommandLineTools/SDKs/MacOSX10.14.sdk
  ```

- Then try `poetry install` again.
