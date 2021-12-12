# Minecraft Resource Pack Builder

Generate Minecraft resource packs from multiple directories, to create multiple resource packs with shared resources but different artstyles.

## About

Resource Packager is a Github Action mainly for resource pack artists and server owners.

It provides an easy way to create different resource packs with different artstyles / resolutions but with shared data.

## Usage

**[Click Here](https://github.com/Sorrowfall/RP-Example/generate)** to create a new repository with the workflow already set up.
Rememember to edit `.github/workflows/build-packs.yml`

### Inputs

| Name | Description | Default |
| - | - | - |
| `filename` | The name of the built pack | none |
| `items` | The folders / files to be built into the pack | none |
| `configuration-path` | Whether or not to generate a Sha1 hash of the built pack | `false` |
| `output-folder` | The directory to output files in | `build` |

## Example Workflows

Generate resource packs and push them to the `build` branch of your repository

```yaml
name: build-resource-pack
on: [push]
jobs:
  check-bats-version:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repo
        uses: actions/checkout@v2
      # copy-paste this part for however many packs you want to build
      - name: Build resource pack
        uses: Sorrowfall/Resource-Packager@main
        with:
          # The name of the built pack
          filename: MyPack
          # The directories / files to be built into the pack
          # Directories take priority as they go down the list, replacing any files from the above directories
          items: |
            folder1
            folder2
          # Whether or not to generate a Sha1 hash of the built pack 
          # Useful for server resource packs
          # default: false
          gen-sha1: false
          # The directory to output files in
          output-folder: build
      - name: Publish
        uses: github-actions-x/commit@v2.8
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          push-branch: 'build'
          commit-message: 'build packs'
          name: Builder[bot]
          email: my.github@email.com 
```

Generate resource packs and make a new release

```yaml
name: build-resource-pack
on: [push]
jobs:
  check-bats-version:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repo
        uses: actions/checkout@v2
      # copy-paste this part for however many packs you want to build
      - name: Build resource pack
        uses: Sorrowfall/Resource-Packager@main
        with:
          # The name of the built pack
          filename: MyPack
          # The directories / files to be built into the pack
          # Directories take priority as they go down the list, replacing any files from the above directories
          items: |
            folder1
            folder2
          # Whether or not to generate a Sha1 hash of the built pack 
          # Useful for server resource packs
          # default: false
          gen-sha1: false
          # The directory to output files in
          output-folder: build
      - name: Publish
        uses: ncipollo/release-action@v1
        with:
          artifacts: "release.tar.gz,foo/*.txt"
          bodyFile: "body.md"
          token: ${{ secrets.GITHUB_TOKEN }}
          uses: github-actions-x/commit@v2.8
```
