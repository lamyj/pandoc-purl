import sys
import pandocfilters

from . import purl

def main():
    pandocfilters.toJSONFilters([purl])

if __name__ == "__main__":
    sys.exit(main())
