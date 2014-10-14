BuildParser
===========

A [specification](SPECIFICATION.md) and parser for project build configuration.

## Setup

### pip
```bash
pip install buildparser
````

### git
```bash
git clone git://github.com/brettlangdon/buildparser.git
cd ./buildparser
python setup.py install
```

## Basic Usage

```python
import buildparser

builds = buildparser.parse("./path/to/project")
for build in builds:
    print build.env
    print build.before_build
    print build.build
    print build.after_build
    print build.after_success
    print build.after_failure
```

## API

### Environment(object)
#### Properties
* `type` - string
* `options` - mixed

#### Methods
* `__init__(self, type, options)`
* `__repr__(self)`
* `as_dict(self)`
* `as_json(self)`
* `as_yaml(self)`

### Script(object)
#### Properties
* `commands` - list

#### Methods
* `__init__(self, commands)`
* `__repr__(self)`
* `as_dict(self)`
* `as_json(self)`
* `as_yaml(self)`

### Build(object)
#### Properties
* `env` - Environment
* `before_build` - Script
* `build` - Script
* `after_build` - Script
* `after_success` - Script
* `after_failure` - Script

#### Methods
* `__init__(self, env, before_build, build, after_build, after_success, after_failure)`
* `__repr__(self)`
* `as_dict(self)`
* `as_json(self)`
* `as_yaml(self)`

## UnknownExtensionException(Exception)

## parse(directory, name="build")
*returns*: list

Look for an appropriate `name` file or directory in the directory `directory`
and parse all possible build configurations found.

`parse` defaults to looking for the following files:
* `.build.yml`
* `.build.yaml`
* `.build.json`
* `.build.ini`
* `.build.cfg`

or for the directory `.build` which contains one or many configuration files
(name doesn't have to be "build").

## parse_directory(dir_name)
*returns*: list

Look for all appropriate files inside of `dir_name` and parse configurations found.

## parse_file(file_name)
*returns*: list

Parse any available build configurations from `file_name`

## parse_yaml(file_name)
*returns*: list

Parse any available build configurations from `file_name` as though it was yaml.

## parse_json(file_name)
*returns*: list

Parse any available build configurations from `file_name` as though it was json.

## parse_ini(file_name)
*returns*: list

Parse any available build configurations from `file_name` as though it was an ini file.
