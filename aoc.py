#!/usr/bin/env python3

import os
import sys
import re
import requests

year = 2023
# also, remember to authenticate on the site and put the value of
# the "session" cookie in your environment as AOC_SESSION_TOKEN


def main():
    if len(sys.argv) != 2:
        print("usage: aoc.py <day>")
        sys.exit(1)
    else:
        day = sys.argv[1]

    directory = f"day{int(day):02}"
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"created {directory} directory")
    
    path = f"{directory}/aoc_util.py"
    if not os.path.exists(path):
        os.symlink("../aoc_util.py", path)
        print(f"created {path} symlink")

    base_url = f"https://adventofcode.com/{year}/day/{day}"
    headers = {"Cookie": f"session={os.environ['AOC_SESSION_TOKEN']}"}

    input_filenames = []

    # Fetch the day's puzzle input
    input_url = f"{base_url}/input"
    response = requests.get(input_url, headers=headers)
    if response.status_code == 200:
        path = uniquify(f"{directory}/input.txt")
        input_filenames.append(path.split("/")[-1])
        with open(path, "wb") as file:
            file.write(response.content)
            print(f"wrote {path}")
    else:
        print(f"Failed to fetch input: {response.status_code} {response.reason}")

    # Fetch the day's description and strip out likely example inputs
    description_url = base_url
    response = requests.get(description_url, headers=headers)
    if response.status_code == 200:
        examples = extract_examples(response.text)
        for idx, example in enumerate(examples):
            path = uniquify(f"{directory}/example{idx}.txt")
            input_filenames.append(path.split("/")[-1])
            with open(path, "w") as file:
                file.write(example)
                print(f"wrote {path}")
    else:
        print(f"Failed to fetch example(s): {response.status_code} {response.reason}")

    # Create a simple starter part1.py program template
    path = uniquify(f"{directory}/part1.py")
    with open(path, "w") as file:
        # rotating input_filenames one to the left to make the real input.txt last
        file.write(starter_template(input_filenames[1:] + input_filenames[:1]))
        os.chmod(path, 0o755)
        print(f"wrote {path}")


def uniquify(path):
    while os.path.exists(path):
        parts = re.match(r"^(.*?)(\((\d+)\))?(\.[^.]*)$", path)
        version = int(parts.group(3) or 0) + 1
        path = f"{parts.group(1)}({version}){parts.group(4)}"

    return path


def starter_template(input_filenames):
    return f"""#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames={input_filenames})

print(lines)
"""


def extract_examples(text):
    matches = re.findall(r"<pre><code>(.*?)</code></pre>", text, re.DOTALL)
    return list(map(lambda s: s.replace("<em>", "").replace("</em>", ""), matches))


if __name__ == "__main__":
    main()
