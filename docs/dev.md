---
toc: true
---

This document is for the core dev team of JHU.

## Linux

Setup development environment.

```bash
function ue4editor {
  ~/UnrealEngine/Engine/Binaries/Linux/UE4Editor `pwd`/$1
}

function generate_project {
  ~/UnrealEngine/GenerateProjectFiles.sh -project="`pwd`/$1" \
    -game -engine -vscode -makefile
}
```

## Package the binary

Use `bash package.sh` to build a linux binary. The packaged binary will be output to `unrealcv_binary` folder.

Zip and scp to `gradx.cs.jhu.edu` to release binaries. Use datetime as version number and track updates in `version.md`.

Use `package_win.sh` to package windows binary.