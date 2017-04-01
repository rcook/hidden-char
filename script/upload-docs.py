#!/usr/bin/env python
############################################################
#
# upload-docs.py
# Copyright (C) 2017, Richard Cook
# Released under MIT License
# https://github.com/rcook/hidden-char
#
############################################################

from __future__ import print_function
import argparse
import fnmatch
import json
import os
from pyprelude.file_system import make_path
from pyprelude.process import execute
from pyprelude.temp_util import temp_cwd, temp_dir
from pyprelude.util import unpack_args
import re
import shutil
import tarfile

_NAME_PATTERN = re.compile("^name\s*:\s*(?P<name>.*)$")
_VERSION_PATTERN = re.compile("^version\s*:\s*(?P<version>.*)$")

def _get_credentials(path):
    obj = json.load(open(path, "rt"))
    return obj["username"], obj["password"]

def _get_cabal_path(project_dir):
    paths = fnmatch.filter(os.listdir(project_dir), "*.cabal")
    if len(paths) == 0:
        raise RuntimeError("Could not find a .cabal file")
    if len(paths) > 1:
        raise RuntimeError("Found more than one .cabal file")
    return make_path(project_dir, paths[0])

def _get_stack_yaml_path(project_dir):
    path = make_path(project_dir, "stack.yaml")
    if not os.path.isfile(path):
        raise RuntimeError("Could not find a stack.yaml file")
    return path

def _get_package_info(cabal_path):
    name = None
    version = None
    with open(cabal_path, "rt") as f:
        for line in f.readlines():
            if name is not None and version is not None:
                break;

            l = line.strip()
            m = _NAME_PATTERN.match(l)
            if m:
                name = m.groups("name")[0]
            m = _VERSION_PATTERN.match(l)
            if m:
                version = m.groups("version")[0]

    if name is not None and version is not None:
        return name, version

    raise RuntimeError("Could not parse name and version from {}".format(cabal_path))

def _system(*args):
    command_fragments = unpack_args(*args)
    command = " ".join(command_fragments)
    status = os.system(command)
    if status != 0:
        raise RuntimeError()

def _generate_docs(project_dir):
    with temp_cwd(project_dir):
        _system("stack", "build", "--haddock")

def _get_doc_root(project_dir):
    return execute("stack", "path", "--local-doc-root").strip()

def _copy_docs(temp_dir, project_dir, package_name, package_version):
    doc_root = _get_doc_root(project_dir)
    base_name = "{}-{}".format(package_name, package_version)
    doc_dir = make_path(temp_dir, "{}-docs".format(base_name))
    shutil.copytree(make_path(doc_root, base_name), doc_dir)
    return doc_dir

def _munge_file(path):
    output = re.sub("href=\"\\.\\.\/([^/]*)\/", "href=\"../../\\1/docs/", open(path, "rt").read())
    open(path, "wt").write(output)

def _munge_docs(doc_dir):
    for d, _, file_names in os.walk(doc_dir):
        for file_name in file_names:
            p = make_path(d, file_name)
            ext = os.path.splitext(p)[1]
            if ext == ".html":
                _munge_file(p)

def _create_archive(project_dir, doc_dir):
    parent_dir = os.path.dirname(doc_dir)
    subdir = os.path.basename(doc_dir)
    tar_path = "{}.tar.gz".format(doc_dir)
    with tarfile.open(tar_path, "w:gz", format=tarfile.USTAR_FORMAT) as tf:
        for d, _, file_names in os.walk(doc_dir):
            for file_name in file_names:
                p = make_path(d, file_name)
                arc_name = os.path.join(subdir, os.path.relpath(p, doc_dir))
                ti = tf.gettarinfo(p, arc_name)
                ti.uid = 0
                ti.gid = 0
                tf.addfile(ti, file(p))
    return tar_path

def _upload_archive(user_name, password, tar_path, package_name, package_version):
    command = [
        "curl",
        "-X",
        "PUT",
        "-H",
        "Content-Type: application/x-tar",
        "-H",
        "Content-Encoding: gzip",
        "-u",
        "{}:{}".format(user_name, password),
        "--data-binary",
        "@{}".format(tar_path),
        "https://hackage.haskell.org/package/{}-{}/docs".format(package_name, package_version)]
    output = execute(command)
    print(output)

def _main_inner(args):
    user_name, password = _get_credentials(args.credentials_path)
    stack_yaml_path = _get_stack_yaml_path(args.project_dir)
    cabal_path = _get_cabal_path(args.project_dir)
    package_name, package_version = _get_package_info(cabal_path)
    _generate_docs(args.project_dir)

    with temp_dir() as d:
        doc_dir = _copy_docs(d, args.project_dir, package_name, package_version)
        _munge_docs(doc_dir)
        tar_path = _create_archive(args.project_dir, doc_dir)
        _upload_archive(user_name, password, tar_path, package_name, package_version)

def _parse_path(x):
    return make_path(os.path.expanduser(x))

def _parse_file_must_exist(path):
    path = _parse_path(path)
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError("File {} does not exist".format(path))
    return path

def _parse_dir_must_exist(path):
    path = _parse_path(path)
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError("Directory {} does not exist".format(path))
    return path

def _main():
    script_dir = make_path(os.path.dirname(__file__))
    parser = argparse.ArgumentParser(description="Generate Haddocks and upload to Hackage")
    parser.add_argument(
        "--creds",
        "-c",
        metavar="CREDENTIALSPATH",
        dest="credentials_path",
        default=_parse_path("~/.stack/upload/credentials.json"),
        type=_parse_file_must_exist,
        help="path to Stack credentials file")
    parser.add_argument(
        "--project-dir",
        "-p",
        metavar="PROJECTDIR",
        dest="project_dir",
        default=_parse_path(make_path(script_dir, "..")),
        type=_parse_dir_must_exist,
        help="path to project")
    args = parser.parse_args()
    _main_inner(args)

if __name__ == "__main__":
    _main()
