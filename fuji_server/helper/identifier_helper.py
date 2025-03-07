# MIT License
#
# Copyright (c) 2020 PANGAEA (https://www.pangaea.de/)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import idutils
import re

from fuji_server.helper.metadata_mapper import Mapper

from fuji_server.helper.preprocessor import Preprocessor

class IdentifierHelper:
    IDENTIFIERS_ORG_DATA = Preprocessor.get_identifiers_org_data()
    identifier_schemes=[]
    preferred_schema = None # the preferred schema
    identifier_url = None
    identifier = None
    method = 'idutils'
    is_persistent = False

    def __init__(self, idstring):
        self.identifier = idstring
        self.normalized_id = self.identifier
        if len(self.identifier) > 4 and not self.identifier.isnumeric():
            generic_identifiers_org_pattern = '^([a-z0-9\._]+):(.+)'
            # idutils check
            self.identifier_schemes = idutils.detect_identifier_schemes(self.identifier)
            # identifiers.org check
            if not self.identifier_schemes:
                self.method = 'identifiers.org'
                idmatch = re.search(generic_identifiers_org_pattern, self.identifier)
                if idmatch:
                    found_prefix = idmatch[1]
                    found_suffix = idmatch[2]
                    if found_prefix in self.IDENTIFIERS_ORG_DATA.keys():
                        if (re.search(self.IDENTIFIERS_ORG_DATA[found_prefix]['pattern'], found_suffix)):
                            self.identifier_schemes = [found_prefix, 'identifiers_org']
                            self.preferred_schema = found_prefix
                        self.identifier_url = str(self.IDENTIFIERS_ORG_DATA[found_prefix]['url_pattern']).replace('{$id}', found_suffix)
                        self.normalized_id = found_prefix.lower()+':'+found_suffix
            else:
                # preferred schema
                if len(self.identifier_schemes) > 0:
                    if len(self.identifier_schemes) > 1:
                        if 'url' in self.identifier_schemes:  # ['doi', 'url']
                            self.identifier_schemes.remove('url')
                    self.preferred_schema = self.identifier_schemes[0]
                    self.normalized_id = idutils.normalize_pid(self.identifier,self.preferred_schema)
                self.identifier_url = idutils.to_url(self.identifier,self.preferred_schema)
            if self.preferred_schema in Mapper.VALID_PIDS.value or self.preferred_schema in self.IDENTIFIERS_ORG_DATA.keys():
                self.is_persistent = True

    def get_preferred_schema(self):
        return self.preferred_schema

    def get_identifier_schemes(self):
        return self.identifier_schemes

    def get_identifier_url(self):
        return self.identifier_url

    def get_normalized_id(self):
        return self.normalized_id