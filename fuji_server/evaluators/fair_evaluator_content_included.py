# -*- coding: utf-8 -*-

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
from fuji_server.evaluators.fair_evaluator import FAIREvaluator
from fuji_server.models.identifier_included import IdentifierIncluded
from fuji_server.models.identifier_included_output import IdentifierIncludedOutput
from fuji_server.models.identifier_included_output_inner import IdentifierIncludedOutputInner
import urllib

class FAIREvaluatorContentIncluded(FAIREvaluator):
    def evaluate(self):
        self.result = IdentifierIncluded(id=self.metric_number, metric_identifier=self.metric_identifier, metric_name=self.metric_name)
        self.output = IdentifierIncludedOutput()

        id_object = self.fuji.metadata_merged.get('object_identifier')
        self.output.object_identifier_included = id_object
        contents = self.fuji.metadata_merged.get('object_content_identifier')
        if id_object is not None:
            self.logger.info('FsF-F3-01M : Object identifier specified -: {}'.format(id_object))
        score = 0
        content_list = []
        if contents:
            if isinstance(contents, dict):
                contents = [contents]
            contents = [c for c in contents if c]
            number_of_contents = len(contents)
            self.logger.log(self.fuji.LOG_SUCCESS,'FsF-F3-01M : Number of object content identifier found -: {}'.format(number_of_contents))
            self.maturity = 1
            score = 0.5
            self.setEvaluationCriteriumScore('FsF-F3-01M-1', 0.5, 'pass')
            if number_of_contents >= self.fuji.FILES_LIMIT:
                self.logger.info(
                    'FsF-F3-01M : The total number of object (content) specified is above threshold, so use the first -: {} content identifiers'.format(
                        self.fuji.FILES_LIMIT))
                contents = contents[:self.fuji.FILES_LIMIT]

            for content_link in contents:
                if content_link.get('url'):
                    # self.logger.info('FsF-F3-01M : Object content identifier included {}'.format(content_link.get('url')))
                    did_output_content = IdentifierIncludedOutputInner()
                    did_output_content.content_identifier_included = content_link
                    self.fuji.content_identifier.append(content_link)
                    try:
                        # only check the status, do not download the content
                        response = urllib.request.urlopen(content_link.get('url'))
                        content_link['header_content_type'] = response.getheader('Content-Type')
                        content_link['header_content_type'] = str(content_link['header_content_type']).split(';')[0]
                        content_link['header_content_length'] = response.getheader('Content-Length')
                        if content_link['header_content_type'] != content_link.get('type'):
                            self.logger.warning('FsF-F3-01M : Content type given in metadata differs from content type given in Header response -: (' + str(content_link.get(
                                'type')) + ') vs. (' + str(
                                content_link['header_content_type']) + ')')
                            self.logger.info(
                                'FsF-F3-01M : Replacing metadata content type with content type from Header response -: ' + str(
                                    content_link['header_content_type']))
                            content_link['type'] = content_link['header_content_type']
                        # will pass even if the url cannot be accessed which is OK
                        # did_result.test_status = "pass"
                        # did_score.earned=1

                        did_output_content.content_identifier_active = False
                        #content_list.append(did_output_content)
                    except urllib.error.HTTPError as e:
                        self.logger.warning('FsF-F3-01M : Content identifier inaccessible -: {0} , HTTPError code {1} '.format(
                                content_link.get('url'), e.code))
                    except urllib.error.URLError as e:
                        self.logger.exception(e.reason)
                    except:
                        self.logger.warning('FsF-F3-01M : Could not access the resource')
                    else:  # will be executed if there is no exception
                        #self.fuji.content_identifier.append(content_link)
                        did_output_content.content_identifier_active = True

                    content_list.append(did_output_content)
                else:
                    self.logger.warning('FsF-F3-01M : Object (content) url is empty -: {}'.format(content_link))
        else:
            self.logger.warning('FsF-F3-01M : Data (content) identifier is missing.')

        if content_list:
            self.maturity = 3
            score = 1
            self.setEvaluationCriteriumScore('FsF-F3-01M-1', 0.5, 'pass')
            self.setEvaluationCriteriumScore('FsF-F3-01M-2', 0.5, 'pass')
        self.score.earned = score
        if score > 0.5:
            self.result.test_status = "pass"
        self.result.metric_tests = self.metric_tests
        self.output.content = content_list
        self.result.output = self.output
        self.result.maturity = self.maturity_levels.get(self.maturity)
        self.result.score = self.score
