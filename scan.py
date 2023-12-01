import json
import socket
import argparse
import aiohttp
import asyncio
import config


def generate_prompt():
    argumentParser = argparse.ArgumentParser()
    argumentParser.add_argument("--base-ip", default=socket.gethostbyname(socket.gethostname()),
                                help="base ip address, default local ip")
    argumentParser.add_argument("--mask", default=24, type=int, choices=[8, 16, 24],
                                help="subnet mask, could only be one of 8, 16, 24")
    argumentParser.add_argument("--output", default="machines.json", help="output file, default machines.json")
    return argumentParser.parse_args()


async def is_3d_printer(ip):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{ip}/api/v1/system/name", timeout=1) as response:
                if response.status != 200:
                    print(f"Invalid Ultimaker 3D printer at {ip}")
                    return False
                name = await response.text()
            async with session.get(f"http://{ip}/api/v1/system/variant", timeout=1) as response:
                if response.status != 200:
                    print(f"Invalid Ultimaker 3D printer at {ip}")
                    return False
                variant = await response.text()
            if name == "":
                name = 'Unknown'
            if variant == "":
                variant = 'Unknown'
            # remove " or ' from name and variant
            name = name.replace('"', '').replace("'", "")
            variant = variant.replace('"', '').replace("'", "")
            print(f"Found Ultimaker 3D printer at {ip}, name: {name}, variant: {variant}")
            return {"name": name, "ip_address": ip, "type": variant}
    except aiohttp.ClientError:
        if config.debug:
            print(f"Network error occurred while trying to connect to {ip}")
        return False
    except asyncio.TimeoutError:
        if config.debug:
            print(f"No printer response on {ip}")
        return False
    except json.JSONDecodeError:
        if config.debug:
            print(f"Error occurred while decoding JSON from {ip}")
        return False


def generate_ips(base_ip, mask=24):
    split = base_ip.split(".")
    assert len(split) == 4
    if mask == 8:
        print("Warning: mask 8 will generate 16,777,216 ips, this may take a while")
        return [f"{split[0]}.{i}.{j}.{k}" for i in range(256) for j in range(256) for k in range(256)]
    elif mask == 16:
        print("Warning: mask 16 will generate 65,536 ips, this may take a while")
        return [f"{split[0]}.{split[1]}.{i}.{j}" for i in range(256) for j in range(256)]
    elif mask == 24:
        print("Warning: mask 24 will generate 256 ips, this may take a while")
        return [f"{split[0]}.{split[1]}.{split[2]}.{i}" for i in range(256)]
    else:
        raise ValueError("mask should be one of 8, 16, 24")


async def scan_network(base_ip):
    ips = generate_ips(base_ip)
    tasks = [is_3d_printer(ip) for ip in ips]
    printers = await asyncio.gather(*tasks)
    printers = [printer for printer in printers if printer]
    return printers


def update_machines(base_ip, mask, output):
    ips = generate_ips(base_ip, mask)
    tasks = [is_3d_printer(ip) for ip in ips]
    loop = asyncio.get_event_loop()
    printers = loop.run_until_complete(asyncio.gather(*tasks))
    json.dump(printers, open(output, "w"))
    return printers


if __name__ == '__main__':
    args = generate_prompt()
    printers = asyncio.run(scan_network(args.base_ip))
    json.dump(printers, open(args.output, "w"))
    print(printers)
