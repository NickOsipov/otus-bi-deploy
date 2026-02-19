from invoke import task, Context


@task
def create_vm(ctx: Context, name: str):
    ctx.run(f"bash infra/{name}/create-vm.sh")

@task
def vm_list(ctx: Context):
    ctx.run("yc compute instance list")

@task
def get_external_ip(ctx: Context, name: str):
    ctx.run(f"yc compute instance list --format json | jq -r '.[] | select(.name == \"{name}\") | .network_interfaces[0].primary_v4_address.one_to_one_nat.address'")

@task
def ssh_connect(ctx: Context, name: str, key_path: str = "~/.ssh/yc"):
    external_ip = ctx.run(f"invoke get-external-ip --name {name}", hide=True).stdout.strip()
    print(f"ssh -i {key_path} yc-user@{external_ip}")
