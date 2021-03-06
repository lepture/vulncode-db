# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sqlalchemy import Column, String

from data.utils import populate_models
from data.models.base import MainBase


class User(MainBase):
    email = Column(String(256), unique=True)
    full_name = Column(String(256))
    profile_picture = Column(String(256))

    @property
    def name(self):
        return self.email.split("@", 1)[0]

    def to_json(self):
        """Serialize object properties as dict."""
        # TODO: Refactor how we will surface this.
        return {'username': 'anonymous'}


# must be set after all definitions
__all__ = populate_models(__name__)
