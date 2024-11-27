set shell := ["nu", "-c"]

# List all the just commands
default:
    @just --list

new name:
  hugo new posts/{{name}}/index.md

reset-theme:
  git submodule foreach --recursive git clean -fxd
  git submodule foreach --recursive git reset --hard HEAD
  git submodule update --init
