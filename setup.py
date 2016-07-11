from distutils.core import setup
setup(
  name = 'tolliver',
  packages = ['tolliver'],
  version = '0.1a',
  description = 'An application for dialing in CNC hole tolerances',
  author = 'CastIrony',
  author_email = 'bergamot@gmail.com',
  url = 'https://github.com/castirony/tolliver',
  download_url = 'https://github.com/castirony/tolliver/tarball/0.1a',
  keywords = ['cnc', 'tolerance'],
  requires = ['docopt', 'cerberus', 'ezdxf'],    
)
