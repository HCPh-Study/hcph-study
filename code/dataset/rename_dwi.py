# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# Copyright 2023 The Axon Lab <theaxonlab@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# We support and encourage derived works from this project, please read
# about our expectations at
#
#     https://www.nipreps.org/community/licensing/
"""Update the stim_file column with the mundaka clip reference."""

from pathlib import Path
import pandas as pd

OLDNAME = "highres"
NEWNAME = "standard"
DATATYPE = "dwi"
ENTITY = "acq"

scans_files = (
    sorted(Path('sub-001').glob('ses-2*/*_scans.tsv'))
    # + sorted(Path('sub-001').glob('ses-excl0*/*_scans.tsv'))
)

# scans_files = (
#     sorted(Path('sub-001').glob('ses-pilot0*/*_scans.tsv'))
# )

for scans_file in scans_files:
    content = pd.read_csv(scans_file, sep='\t', index_col=None)
    content["filename-old"] = content.filename
    content["filename"] = content["filename"].str.replace(
        f"{ENTITY}-{OLDNAME}_", f"{ENTITY}-{NEWNAME}_"
    )

    to_rename = content.loc[
        content.filename.str.contains(f"{ENTITY}-{NEWNAME}_"), ["filename-old", "filename"]
    ]
    for run in to_rename.values:
        # NIfTI files
        old = scans_file.parent / run[0]
        new = scans_file.parent / run[1]

        if not new.exists():
            print(f"Renaming {old} -> {new}")
            old.rename(new)
        elif not old.exists():
            print(f"WARNING: Neither {old} nor {new} exist.")

    # Rename the remainder of the files
    for old in scans_file.parent.glob(f"{DATATYPE}/*_{ENTITY}-{OLDNAME}_*"):
        new = old.parent / old.name.replace(f"_{ENTITY}-{OLDNAME}_", f"_{ENTITY}-{NEWNAME}_")

        if not new.exists():
            print(f"Renaming {old} -> {new}")
            old.rename(new)
        elif not old.exists():
            print(f"WARNING: Neither {old} nor {new} exist.")
        else:
            print(f"WARNING: Both {old} and {new} exist.")

    content = content.drop(columns=["operator", "filename-old"], errors="ignore")
    print(f"Updating {scans_file}.")
    content.to_csv(scans_file, sep='\t', index=None)
