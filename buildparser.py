__all__ = [
    "UnknownExtensionException",
    "Build",
    "Environment",
    "parse",
    "parse_directory",
    "parse_yaml",
    "parse_json",
    "parse_ini",
]
__version__ = "0.1.0"

import ConfigParser
import json
import os

import yaml
try:
    from yaml import CLoader as YamlLoader
except ImportError:
    from yaml import Loader as YamlLoader

PERMITTED_EXTENSIONS = ["yml", "yaml", "json", "ini", "cfg"]


class UnknownExtensionException(Exception):
    pass


class Environment(object):
    __slots__ = ["type", "options"]

    def __init__(self, type, options):
        self.type = type
        if not isinstance(options, list):
            options = str(options)
        self.options = options

    def __repr__(self):
        return "Environment(%r, %r)" % (self.type, self.options)

    def as_dict(self):
        return {
            self.type: self.options
        }

    def as_json(self):
        return json.dumps(self.as_dict())

    def as_yaml(self):
        return yaml.dump(self.as_dict())


class Script(object):
    __slots__ = ["commands"]

    def __init__(self, commands):
        if isinstance(commands, str):
            commands = [str]
        self.commands = commands

    def __repr__(self):
        return "Script(%r)" % (self.commands, )

    def as_list(self):
        return self.commands

    def as_json(self):
        return json.dumps(self.commands)

    def as_yaml(self):
        return yaml.dump(self.commands, default_flow_style=False)


class Build(object):
    __slots__ = ["env", "before_build", "build", "after_build", "after_success", "after_failure"]

    def __init__(self, env, before_build, build, after_build, after_success, after_failure):
        self.env = env
        self.before_build = before_build
        self.build = build
        self.after_build = after_build
        self.after_success = after_success
        self.after_failure = after_failure

    def __repr__(self):
        return "Build(%r, %r, %r, %r, %r, %r)" % (
            self.env, self.before_build, self.build, self.after_build, self.after_success, self.after_failure
        )

    def as_dict(self):
        return {
            "env": self.env.as_dict(),
            "before_build": self.before_build.commands,
            "build": self.build.commands,
            "after_build": self.after_build.commands,
            "after_success": self.after_success.commands,
            "after_failure": self.after_failure.commands,
        }

    def as_json(self):
        return json.dumps(self.as_dict())

    def as_yaml(self):
        return yaml.dump(self.as_dict(), default_flow_style=False)


def get_as_list(obj, key):
    value = obj.get(key, [])
    if not isinstance(value, list):
        value = [value]
    return value;


def split_string(value):
    if "\n" not in value:
        return [value]

    values = []
    for value in value.split("\n"):
        value = value.strip()
        if value:
            values.append(value)
    return values


def get_ext(file_name):
    _, ext = os.path.splitext(file_name)
    _, _, ext = ext.partition(".")
    return ext


def parse(directory=None, name="build"):
    if directory is None:
        directory = os.getcwd()
    else:
        directory = os.path.abspath(directory)

    dir_name = os.path.join(directory, ".%s" % (name, ))
    if os.path.exists(dir_name) and os.path.isdir(dir_name):
        return parse_directory(dir_name)

    for ext in PERMITTED_EXTENSIONS:
        file_name = os.path.join(directory, ".%s.%s" % (name, ext))
        if os.path.exists(file_name):
            return parse_file(file_name, ext)


def parse_directory(dir_name):
    builds = []
    for file_name in os.listdir(dir_name):
        file_name = os.path.join(dir_name, file_name)
        ext = get_ext(file_name)
        if ext in PERMITTED_EXTENSIONS:
            for build in parse_file(file_name):
                builds.append(build)
    return builds


def parse_file(file_name, ext=None):
    if ext is None:
        ext = get_ext(file_name)

    config = None
    if ext in ("yml", "yaml"):
        config = parse_yml(file_name)
    elif ext == "json":
        config = parse_json(file_name)
    elif ext in ("ini", "cfg"):
        config = parse_ini(file_name)
    else:
        raise UnknownExtensionException("Unknown File Extension %s on File %s" % (ext, file_name))

    return expand_build_configuration(config)


def parse_yml(file_name):
    config = None
    with open(file_name) as fp:
        config = yaml.load(fp, Loader=YamlLoader)
    return config


def parse_json(file_name):
    config = None
    with open(file_name) as fp:
        config = json.load(fp)
    return config


def parse_ini(file_name):
    config = None
    with open(file_name) as fp:
        config = ConfigParser.ConfigParser()
        config.readfp(fp)
    data = {}
    for section in config.sections():
        if section not in ("env", "post_build"):
            for key, value in config.items(section):
                data[key] = split_string(value)
        else:
            data[section] = {}
            for key, value in config.items(section):
                data[section][key] = split_string(value)
    return data


def expand_build_configuration(config):
    before_build = Script(get_as_list(config, "before_build"))
    build = Script(get_as_list(config, "build"))
    after_build = Script(get_as_list(config, "after_build"))
    after_success = Script(get_as_list(config, "after_success"))
    after_failure = Script(get_as_list(config, "after_failure"))
    env = config.get("env", {})
    if not isinstance(env, dict):
        env = {}
    for env_type, values in env.iteritems():
        if not isinstance(values, list):
            values = [values]
        for value in values:
            yield Build(Environment(env_type, value), before_build, build, after_build, after_success, after_failure)
