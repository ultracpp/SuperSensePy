/*
 * C RB Hash Map - Hash Map Implementation in C Language
 * Copyright (c) 2024 Eungsuk Jeon
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
import numpy as np
import rrcf


class MyRRCF:

    def __init__(self, n_estimators=40, window_size=10, max_depth=256):
        self.n_estimators = n_estimators
        self.window_size = window_size
        self.max_depth = max_depth

        self.forest = []
        self.idx = 0
        self.total_codisp = {}

        self.create_forest()

    def create_forest(self):
        for _ in range(self.n_estimators):
            tree = rrcf.RCTree(random_state=1)
            self.forest.append(tree)

    def anomaly_detection(self, data):
        if not self.forest:
            raise ValueError("Forest not initialized. Call create_forest() before anomaly_detection().")

        for tree in self.forest:
            if len(tree.leaves) > self.max_depth:
                try:
                    tree.forget_point(self.idx - self.max_depth)
                except Exception as e:
                    print(f"Error forgetting point in tree: {e}")

            tree.insert_point(data, index=self.idx)

            if self.idx not in self.total_codisp:
                self.total_codisp[self.idx] = 0

            self.total_codisp[self.idx] += tree.codisp(self.idx) / self.n_estimators

        mean = np.mean(list(self.total_codisp.values()))
        std = np.std(list(self.total_codisp.values()), ddof=1)  # Use ddof=1 for sample std deviation

        if std == 0:
            z = np.inf
        else:
            z = (self.total_codisp[self.idx] - mean) / std

        self.idx += 1

        return z
