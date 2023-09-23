import json
import subprocess
import unittest

import pandocfilters

import pandoc_purl

class PurlTest(unittest.TestCase):
    def _purl(self, source):
        document = subprocess.run(
                ["pandoc", "-f", "markdown", "-t", "json"],
                input=source.encode(), stdout=subprocess.PIPE
            ).stdout
        
        altered = pandocfilters.applyJSONFilters([pandoc_purl.purl], document)
        return json.loads(altered)
