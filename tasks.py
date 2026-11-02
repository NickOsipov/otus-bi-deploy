import json

from jinja2 import Template
from invoke import task, Context


@task
def create_vm(ctx: Context, name: str):
    """
    Create a virtual machine with the specified name.
    """
    ctx.run(f"bash infra/{name}/create-vm.sh")

@task
def create_all_vms(ctx: Context):
    """
    Create all virtual machines.
    """
    for name in ["clickhouse", "redash", "metabase"]:
        create_vm(ctx, name)

@task
def vm_list(ctx: Context):
    """
    List all virtual machines.
    """
    ctx.run("yc compute instance list")

@task
def get_external_ip(ctx: Context, name: str):
    """
    Get the external IP address of a virtual machine by its name.
    """
    ctx.run(f"yc compute instance list --format json | jq -r '.[] | select(.name == \"{name}\") | .network_interfaces[0].primary_v4_address.one_to_one_nat.address'")

@task
def ssh_connect(ctx: Context, name: str, key_path: str = "~/.ssh/yc"):
    """
    Print the SSH command to connect to a virtual machine by its name.
    """
    external_ip = ctx.run(f"invoke get-external-ip --name {name}", hide=True).stdout.strip()
    print(f"ssh -i {key_path} yc-user@{external_ip}")

@task
def clone_repo(ctx: Context):
    """
    Clone the repository on all Docker hosts.
    """
    ctx.run("ansible-playbook -i infra/ansible/inventory.yml infra/ansible/clone-repo.yml", pty=True)


@task
def generate_inventory(
    ctx: Context,
    template_path: str = "infra/ansible/inventory.yml.example",
    output_path: str = "infra/ansible/inventory.yml",
    ansible_user: str = "yc-user",
    ssh_key_path: str = "~/.ssh/yc",
):
    """
    Generate ansible inventory from Jinja template and external VM IPs from yc.
    """
    instances_raw = ctx.run("yc compute instance list --format json", hide=True).stdout
    instances = json.loads(instances_raw)

    external_ips = {}
    for instance in instances:
        try:
            ip_address = instance["network_interfaces"][0]["primary_v4_address"]["one_to_one_nat"]["address"]
        except (KeyError, IndexError, TypeError):
            continue

        instance_name = instance.get("name")
        if instance_name and ip_address:
            external_ips[instance_name] = ip_address

    with open(template_path, "r", encoding="utf-8") as template_file:
        template = Template(template_file.read())

    rendered = template.render(
        metabase_ip=external_ips.get("metabase-vm", ""),
        redash_ip=external_ips.get("redash-vm", ""),
        ansible_user=ansible_user,
        ssh_key_path=ssh_key_path,
    )

    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(rendered)

    missing_hosts = [
        host_name for host_name in ["metabase-vm", "redash-vm"] if host_name not in external_ips
    ]

    if missing_hosts:
        print(
            "Inventory generated, but no external IP found for: "
            + ", ".join(missing_hosts)
            + "."
        )
    else:
        print("Inventory generated successfully: infra/ansible/inventory.yml")

