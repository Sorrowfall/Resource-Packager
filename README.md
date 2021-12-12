# Resource-Packager

Generate Minecraft resource packs from multiple directories, to create multiple resource packs with shared resources but different artstyles.

## About

Resource Packager is a Github Action intended for Minecraft resource pack artists and server owners.

It provides an easy way to package resource packs, as well as combined share data with different assets, for different resolution / artsytle packs.

## Usage

**[Click Here](https://github.com/Sorrowfall/RP-Example/generate)** to create a new repository with the workflow already set up.
Rememember to edit `.github/workflows/build-packs.yml`

### Inputs

| Name | Description | Default |
| - | - | - |
| `filename` | What to name the built resource pack. | `None` |
| `items` | What folders / files to include in the resource pack. | `None` |
| `output-folder` | What directory to build files inside. | `'build/'` |
| `optimize-jsons` | Whether or not to optimize any .json (and .mcmeta json) files to lower their size. | `True` |
| `gen-sha1` | Whether or not to generate a `Sha1` hash of the built pack. Useful for Server Resource Packs. | `False` |

## Example Workflows

> If you want to generate multiple resource packs. just copy-paste the `Build resource pack` step.

Generate resource packs and push them to the `build` branch of your repository.

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
            32_res_textures
            data
          # What directory to output files in
          output-folder: build
          # Whether or not to optimize .json (and .mcmeta json) files
          optimize-json: true
          # Whether or not to generate a Sha1 hash of the built pack 
          # Useful for server resource packs
          # default: false
          gen-sha1: false
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
            32_res_textures
            data
          # What directory to output files in
          output-folder: build
          # Whether or not to optimize .json (and .mcmeta json) files
          optimize-json: true
          # Whether or not to generate a Sha1 hash of the built pack 
          # Useful for server resource packs
          # default: false
          gen-sha1: false
      - name: Publish
        uses: ncipollo/release-action@v1
        with:
          artifacts: "release.tar.gz,foo/*.txt"
          bodyFile: "body.md"
          token: ${{ secrets.GITHUB_TOKEN }}
          uses: github-actions-x/commit@v2.8
```
