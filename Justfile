
reset-theme:
  git submodule foreach --recursive git clean -fxd
  git submodule foreach --recursive git reset --hard HEAD
  git submodule update --init
