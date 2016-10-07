#!/bin/bash -e

if [[ $EUID -ne 0 ]]; then
    echo "You are NOT running this script as root."
    echo "You should."
    echo "Really."
    exit 1
fi

if [[ ! -x $(which lsb_release 2>/dev/null) ]]; then
  echo "ERROR: lsb_release is not installed"
  echo "Cannot evaluate the platform"
  echo "Please install lsb_release and retry"
  echo "Red Hat based Systems : yum install redhat-lsb-core"
  echo "Debian based Systems : apt-get install lsb-release"
  exit 1
fi

# GET OS VENDOR
os_VENDOR=$(lsb_release -i -s)
# GET OS MAJOR VERSION
os_VERSION=$(lsb_release  -r  -s | cut -d. -f 1)

echo "*** Detected Linux $os_VENDOR $os_VERSION ***"

if ansible --version &> /dev/null ; then
  echo "Ansible is already installed."
else
  if [[ "Debian" =~ $os_VENDOR || "Raspbian" =~ $os_VENDOR ]]; then
    apt-get update
    apt-get install -y ansible
  elif [[ "Ubuntu" =~ $os_VENDOR || "LinuxMint" =~ $os_VENDOR ]]; then
    add-apt-repository -y ppa:ansible/ansible
    apt-get update
    apt-get install -y ansible
  else
    echo "*** Unsupported platform ${os_VENDOR}: ${os_VERSION} ***"
    echo "*** Please send a pull-request or open an issue ***"
    echo "*** on https://github.com/ceph/ceph-ansible/ ***"
    exit 1
  fi

  if ( ansible --version &> /dev/null ); then
    echo "*** $(ansible --version | head -n1) installed successfully ***"
  else
    echo "Something went wrong, please have a look at the script output"
    exit 1
  fi
fi

ansible-playbook -i "localhost", -c local playbooks/setup-pmm.yml

set +x
echo "Installation completed."