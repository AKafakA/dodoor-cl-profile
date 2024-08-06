"""This is a trivial example of a gitrepo-based profile; The profile source code and other software, documentation, etc. are stored in in a publicly accessible GIT repository (say, github.com). When you instantiate this profile, the repository is cloned to all of the nodes in your experiment, to `/local/repository`. 

This particular profile is a simple example of using a single raw PC. It can be instantiated on any cluster; the node will boot the default operating system, which is typically a recent version of Ubuntu.

Instructions:
Wait for the profile instance to start, then click on the node in the topology and choose the `shell` menu item. 
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg

# Create a portal context.
pc = portal.Context()
user_name = "asdwb"
num_scheduler_datastore = 1
num_nodes = 100
node_deployment_command = ("cd /users/{} && nohup java -cp dodoor/target/dodoor-1.0-SNAPSHOT.jar "
                           "edu.cam.dodoor.ServiceDaemon"
                           " -c ~/dodoor/config.conf -d false -s false -n true  &"
                           .format(user_name))

scheduler_deployment_command = ("cd /users/{} && nohup java -cp dodoor/target/dodoor-1.0-SNAPSHOT.jar "
                                "edu.cam.dodoor.ServiceDaemon"
                                " -c ~/dodoor/config.conf -d true -s true -n false &"
                                .format(user_name))
# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Add a raw PC to the request.
executor_hardware_type = "m400"
scheduler_hardware_type = "d6515"

link = request.Link()
num_node_in_link = 35
links = [link]
executor_nodes = []
NETMASK = "255.255.255.0"
IP_PREFIX = "10.10.1."

for i in range(num_scheduler_datastore, num_nodes + num_scheduler_datastore):
    node = request.RawPC("node" + str(i))
    node.hardware_type = executor_hardware_type
    node.addService(pg.Execute(shell="sh", command="sudo ./local/repository/setup.sh {}".format(num_nodes)))
    iface = node.addInterface("if" + str(i))
    iface.addAddress(pg.IPv4Address(IP_PREFIX + str(i), NETMASK))
    link.addInterface(iface)
    executor_nodes.append(node)
    if i % num_node_in_link == 0 and i != num_nodes + num_scheduler_datastore - 1:
        link = request.Link()
        links.append(link)


for i in range(0, num_scheduler_datastore):
    scheduler_node = request.RawPC("node" + str(i))
    scheduler_node.hardware_type = scheduler_hardware_type
    scheduler_node.addService(pg.Execute(shell="sh", command="sudo ./local/repository/setup.sh {}".format(num_nodes)))
    for j in range(len(links)):
        iface = scheduler_node.addInterface("sif" + str(i) + str(j))
        iface.addAddress(pg.IPv4Address(IP_PREFIX + str(i), NETMASK))
        links[j].addInterface(iface)

# for i in range(0, num_nodes):
#     executor_nodes[i].addService(pg.Execute(shell="sh", command=node_deployment_command))

pc.printRequestRSpec(request)
