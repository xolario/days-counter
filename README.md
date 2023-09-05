# Installation

- You need python3 installed
- You need `pyyaml` package installed

To instal `pyyaml` run the following command:

```bash
pip3 install pyyaml
```

# Usage

You have two ways to use this script:

1. display summary

To display summary you need you run the following command specifying your current country:

```bash
python main.py summary -c <current-country>
python main.py summary --current <current-country>
```

Example:

```bash
python main.py summary -c Serbia
python main.py summary --current Serbia
```

2. add new flight

```bash
python main.py add -d <yyyy-mm-dd> -f <from-country>
python main.py add --date <yyyy-mm-dd> --from <from-country>
```

