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
import numpy as np
import pandas as pd

# files = sorted(Path('sub-001').glob('ses-0*/func/sub-excl*_task-rest_*_events.tsv'))
files = sorted(Path('sub-001').glob('ses-0*/func/sub-*_task-rest_*_events.tsv'))

for f in files:
    content = pd.read_csv(f, sep='\t', index_col=None)
    if 'stim_file' in content.columns:
        print(f"{f}: NO-ACTION")
        continue

    content['stim_file'] = 'n/a'
    if np.any(movie_row := content.trial_type == 'movie'):
        content.loc[movie_row, ['stim_file']] = 'mundaka-clip.mp4'
        content.to_csv(f, index=None, sep='\t')
        print(f"{f}: UPDATED")
    else:
        print(f"{f}: FAILED")
