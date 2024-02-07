import subprocess

# Install nfs-utils package
subprocess.run(['sudo', 'dnf', 'install', '-y', 'nfs-utils'])

# Enable and start NFS server and rpcbind
subprocess.run(['sudo', 'systemctl', 'enable', 'nfs-server', 'rpcbind'])
subprocess.run(['sudo', 'systemctl', 'start', 'nfs-server', 'rpcbind'])

# Ask for the directory to share
directory = input("Enter the directory to share (e.g., /var/nfsshare/registry): ")

# Set permissions and ownership for the shared directory
subprocess.run(['sudo', 'chmod', '-R', '777', directory])
subprocess.run(['sudo', 'chown', '-R', 'nobody:nobody', directory])

# Configure NFS exports
exports_config = f"{directory} *(rw,sync,no_subtree_check,no_root_squash,no_all_squash,insecure)"
with open('/etc/exports', 'a') as exports_file:
    exports_file.write(exports_config + '\n')

# Set SELinux boolean for NFS export
subprocess.run(['sudo', 'setsebool', '-P', 'nfs_export_all_rw', '1'])

# Restart NFS server
subprocess.run(['sudo', 'systemctl', 'restart', 'nfs-server'])

# Configure firewall rules
firewall_commands = [
    ['sudo', 'firewall-cmd', '--permanent', '--zone=public', '--add-service', 'mountd'],
    ['sudo', 'firewall-cmd', '--permanent', '--zone=public', '--add-service', 'rpc-bind'],
    ['sudo', 'firewall-cmd', '--permanent', '--zone=public', '--add-service', 'nfs'],
    ['sudo', 'firewall-cmd', '--reload']
]

for cmd in firewall_commands:
    subprocess.run(cmd)

# Refresh NFS exports and show mounted directories
subprocess.run(['sudo', 'exportfs', '-rav'])
subprocess.run(['sudo', 'showmount', '-e', 'localhost'])

print("NFS setup completed successfully.")

