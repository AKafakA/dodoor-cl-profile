#!/bin/bash

#!/bin/bash

# Update package list and install required packages

sudo chmod -R +rwx /users/asdwb
cd "$(/users/asdwb "$0")"

echo "Installing required packages..."
sudo apt update
echo y | sudo apt install python3-pip thrift-compiler stress openjdk-17-jdk openjdk-17-jre

# Install Python package
echo "Installing python package..."
pip install optparse-pretty

# Download and install Apache Maven
echo "Downloading and installing Apache Maven..."
wget https://downloads.apache.org/maven/maven-3/3.9.8/binaries/apache-maven-3.9.8-bin.tar.gz
sudo tar -zxvf apache-maven-3.9.8-bin.tar.gz
mv apache-maven-3.9.8 maven
sudo mv maven/ /opt/maven

# Set environment variables for Maven
echo "Setting up Maven environment variables..."
echo 'export M2_HOME=/opt/maven' >> .bashrc
echo 'export PATH=${M2_HOME}/bin:${PATH}' >> .bashrc
source .bashrc

# Clone the Git repository
echo "Cloning the dodoor repository..."
git clone https://github.com/AKafakA/dodoor.git

# Checkout the specific branch and rebuild
cd dodoor
echo "Checking out the exp branch and rebuilding..."
git checkout exp
sh rebuild.sh

# Run the configuration generator script
echo "Running the configuration generator script..."
python3 dodoor/deploy/python/scripts/config_generator.py -d dodoor/deploy/resources/host_addresses/cl_static_scheduler -n dodoor/deploy/resources/host_addresses/cl_static_node -s dodoor/deploy/host_addresses/cl_static_scheduler --replay_with_delay True --scheduler-ports 20503,20504

echo "Setup completed successfully!"