# Resource-Packager

## About

**Resource-Packager** is a CLI tool and a Github Workflow action used to make Minecraft Resource Packs out of multiple different directories.

This tool is intended to be used by Resource Pack creators who are working with multiple art styles or resolutions, but with a common set of data like sounds or language files.

## Usage - CLI

To use Resource-Packager as a CLI tool, you first have to download it using `pip install git+https://github.com/Sorrowfall/Resource-Packager`

After it is installed, use `python -m resource-packager -h` to view how to use the tool.

## Usage - Github Workflow

> Click [here](https://github.com/Sorrowfall/RP-Example/generate) to create a new repository with the workflow already set up.
Rememember to edit `.github/workflows/build-packs.yml` to set up Resource-Packager correctly for your pack.

To automatically generate Resource Packs inside of your repository, you first have to make a new file named `resource-pack-gen.yml` inside of the `.github/workflows/` directory.


### Example File
`resource-pack.gen.yml`
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
      - name: Build Pack
        uses: Sorrowfall/Resource-Packager@main
        with:
          items: | # A list of directories to create the Resource Pack with
            pack_data/
            pack_textures/
            # Directories take priority as they go down the list, replacing any files from the above directories
          name: MyPack # The name of the Resource Pack
          output-directory: build # What directory to save the Resource Pack in
          optimize-jsons: true # Whether or not to optimize JSON file
      # copy-paste down to here
      - name: Publish
        uses: EndBug/add-and-commit@v7
        with:
          author_name: Builder[bot]
          author_email: mail@unmail.com
          branch: 'build'
          branch_mode: create
          message: 'Build pack(s)'
```

> If you want to generate multiple resource packs. just copy-paste the `Build resource pack` step.

> You can also create a new Github release of the Resource Pack by adding another step: 

```yaml
    - name: Create Release
      uses: meeDamian/github-release@2.0
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        name: ${{ github.event.head_commit.message }}
        tag: test
        gzip: false
        files: >
          build/MyPack.zip
```

### Inputs

| Name | Description | Default |
| - | - | - |
| `items` | What folders / files to include in the resource pack. | `None` |
| `name` | What to name the built resource pack. | `'pack'` |
| `output-directory` | What directory to build files inside. | `'build/'` |
| `optimize-jsons` | Whether or not to optimize any .json (and .mcmeta json) files to lower their size. | `True` |

This saves the created resource pack on a new `build` branch of the repository.