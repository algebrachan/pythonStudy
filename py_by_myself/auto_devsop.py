import os

install_list=[
  'build-essential',
  'libncurses5-dev',
  'libssl-dev',
  'm4',
  'unixodbc unixodbc-dev',
  'freeglut3-dev libwxgtk3.0-dev',
  'xsltproc',
  'fop',
  'tk8.5',
  'openjdk-8-jdk'
]

erlang_list = [
  'erlang-base',
  'erlang-base-hipe',
  'erlang-dev',
  'erlang-appmon',
  'erlang-asn1',
  'erlang-common-test',
  'erlang-crypto',
  'erlang-debugger',
  'erlang-dialyzer',
  'erlang-diameter',
  'erlang-edoc',
  'erlang-eldap',
  'erlang-erl-docgen',
  'erlang-et',
  'erlang-eunit',
  'erlang-ftp',
  'erlang-gs',
  'erlang-ic',
  'erlang-inets',
  'erlang-inviso',
  'erlang-megaco',
  'erlang-mnesia',
  'erlang-observer',
  'erlang-odbc',
  'erlang-os-mon',
  'erlang-parsetools',
  'erlang-percept',
  'erlang-pman',
  'erlang-public-key',
  'erlang-reltool',
  'erlang-runtime-tools',
  'erlang-snmp',
  'erlang-ssh',
  'erlang-ss',
  'erlang-syntax-tools',
  'erlang-test-server',
  'erlang-tftp',
  'erlang-toolbar',
  'erlang-tools',
  'erlang-tv',
  'erlang-typer',
  'erlang-wx',
  'erlang-xmerl',
]


def download(list):
  for filename in list:
    print(f"download: {filename}")
    print(os.popen(f"apt download {filename}").read())
    
def offline_install(list):
  for filename in list:
    print(f"download: {filename}")
    print(os.popen(f"sudo dpkg -i {filename}").read())

def online_install(list):
  for filename in list:
    print(f"install: {filename}")
    print(os.popen(f"sudo apt install {filename}").read())

if __name__ == '__main__':
    download(erlang_list)
    