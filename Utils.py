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
import os
import random
import string


def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


'''def random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))'''


def get_path(file):
    path = os.path.dirname(os.path.abspath(__file__))
    file_path = path + os.path.sep + file
    print(file_path)
    return file_path


def get_conf_path(conf):
    path = os.path.dirname(os.path.abspath(__file__))
    conf_path = path + os.path.sep + "conf" + os.path.sep + conf + ".conf"
    print(conf_path)
    return conf_path
