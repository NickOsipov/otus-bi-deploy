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
