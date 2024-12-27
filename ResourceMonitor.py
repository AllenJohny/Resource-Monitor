import psutil
import time
import platform
from prettytable import PrettyTable
from tabulate import tabulate
from datetime import datetime, timedelta



def get_cpu_times():
    times =  psutil.cpu_times()
    msg = "\n{CPU times}\n"+f"USER: {times[0]} s    SYSTEM: {times[1]} s     IDLE: {times[2]} s\n"
    print(msg)

def current_cpu_util_percent():
    util = psutil.cpu_percent(interval=1, percpu=True)
    num_of_cores = len(util)
    
    print("\n{CPU cores utilization percents}\n")
    for i in range(100, 0, -5):
        msg = (f"|{i}%").ljust(5, ' ')+"|"      ## ljust used for padding
        for core in range(num_of_cores):
            if util[core] >= i:
                msg = msg + " █ "
            else:
                msg = msg + "   "

        print(msg)
    print("+"+"-"*num_of_cores*5)
    msg_2 = ("|Core").ljust(7, ' ')
    for i in range(num_of_cores):
        msg_2 = msg_2 + str(i+1) +"  "
    
    print(msg_2)
    print("+"+"-"*num_of_cores*5)
    
    print("\n")
    for i in range (0, num_of_cores, 2):
            msg = f"Core {i+1}: {util[i]}%".ljust(16, ' ')  
            msg = msg + f"Core {i+2}: {util[i+1]}%".ljust(16, ' ') 
            print(msg)
    print("\n")


def cpu_cores():
    num_of_cores = psutil.cpu_count(logical=False)
    num_of_logi_cores = psutil.cpu_count()
    print(f"\nPhysical cores: {num_of_cores}      Logical cores: {num_of_logi_cores}\n")


def cpu_freq():
    freq = psutil.cpu_freq(percpu=True)
    display_message = "[ "
    i=0
    ## display for each cpu
    for per_cpu in freq:
        i=i+1  
        print(f"--CPU", i)      
        print("CPU frequency: ", per_cpu[0])
        print("Min frequency: ", per_cpu[1])
        print("Max frequency: ", per_cpu[2])
        percent_val = per_cpu[0]/(per_cpu[2]-per_cpu[1])*100
        for step in range(0,100,5):
            if percent_val>step:
                display_message = display_message + "█"
            else:
                display_message = display_message + ". "
        display_message = display_message + " ] " + f"{per_cpu[0]}/{per_cpu[2]}"
        print(display_message + "\n")



def cpu_load():
    ## requires windup time
    ## not working
    load = psutil.getloadavg()
    time.sleep(6)
    load = psutil.getloadavg()
    print("Current average CPU load: ", load[0]/psutil.cpu_count()*100)


def disk_partiitions_and_use():
    deets = psutil.disk_partitions()
    print("\nCurrent number of partitions: ", len(deets), "\n")
    print("DEVICE".ljust(13, ' ') + "MOUNTPOINT".ljust(17, ' ') + "FSTYPE".ljust(13, ' ') + "OPTS".ljust(13, ' ') + "SIZE".ljust(13, ' ') + "PERCENT UTILIZED".ljust(18, ' '))
    for part in deets:
        msg = f"{part[0]}".ljust(13, ' ') + f"{part[1]}".ljust(17, ' ') + f"{part[2]}".ljust(13, ' ') + f"{part[3]}".ljust(13, ' ')
        use = psutil.disk_usage(part[1])
        msg = msg + (str(round(use[0]/(10**9), 2)) +" GB").ljust(13, ' ') + (str(use[3])+" %").ljust(18, ' ')
        print(msg)
    print("\n")


def disk_IO():
    print("DISK I/O:")
    print(psutil.disk_io_counters(perdisk=True, nowrap=True))
    print("\n")


def print_with_merged_header(header, data):
    table = tabulate(data, headers="firstrow", tablefmt="grid")
    table_width = len(table.splitlines()[0])
    print(header.center(table_width))
    print(table)

def get_memory():
    memory=psutil.virtual_memory()
    swap=psutil.swap_memory()
    memory_data = [  
        ['total', f'{memory.total} Bytes'],  
        ['available', f'{memory.available} Bytes'],
        ['percent', f'{memory.percent} %'],
        ['used', f'{memory.used} Bytes'],
        ['free', f'{memory.free} Bytes'],
    ]
    print_with_merged_header("Memory", memory_data)
    used_bar = int(50 * memory.percent/100)
    available_bar = 50 - used_bar

    bar = f"Used Memory: [{'█' * used_bar}{'.' * available_bar}]\n"
    print(bar)

    swap_data = [
        ['total', f'{swap.total} Bytes'],  
        ['used', f'{swap.used} Bytes'],
        ['free', f'{swap.free} Bytes'],
        ['percent', f'{swap.percent} %'], 
    ]
    print_with_merged_header("swap memory", swap_data)
    print (f"the number of bytes the system has swapped in from disk: {swap.sin} Bytes") 
    print (f"the number of bytes the system has swapped out from disk: {swap.sout} Bytes")

def get_counter_info():
    network_counters=psutil.net_io_counters(pernic=False, nowrap=True)
    memory_data = [  
            ['total number of errors while receiving', f'{network_counters.errin}'],  
            ['total number of errors while sending', f'{network_counters.errout}'],
            ['total number of incoming packets which were dropped', f'{network_counters.dropin}'],
            ['total number of outgoing packets which were dropped ', f'{network_counters.dropout}'],
        ]

    print("\nNetwork ↹ :")
    print(f"↑↑ {network_counters.bytes_sent*(1024**-2)} MB / {network_counters.packets_sent} packets (Sent)")
    print(f"↓↓ {network_counters.bytes_recv*(1024**-2)} MB / {network_counters.packets_recv} packets (Received)")
    print(tabulate(memory_data, tablefmt="tsv"))
    print("\n")

def get_connection_info():
    network_connections=psutil.net_connections(kind='inet')
    connection_data=[]
    for connection in network_connections:
        connection_data.append([
            connection.fd,
            connection.family.name,  
            connection.type.name,    
            f"{connection.laddr.ip}:{connection.laddr.port}",  
            f"{connection.raddr.ip}:{connection.raddr.port}" if connection.raddr else '',  
            connection.status,
            connection.pid
        ])
    headers = ['FD', 'Family', 'Type', 'Local Address', 'Remote Address', 'Status', 'PID']
    print("Connection information:")
    print(tabulate(connection_data, headers=headers, tablefmt="grid"))

def get_network_interfaces_address():
    network_interface_address = psutil.net_if_addrs()
    
    NIC_add_data = []
    for interface, addresses in network_interface_address.items():
        for addr in addresses:
            NIC_add_data.append([
                interface,
                addr.family.name,  
                addr.address,      
                addr.netmask,      
                addr.broadcast,    
                addr.ptp           
            ])
    
    headers = ["Interface", "Family", "Address", "Netmask", "Broadcast", "P2P"]  
    print("\n")  
    print("network interfaces address:")
    print(tabulate(NIC_add_data, headers=headers, tablefmt="grid"))
    print("\n")

def get_network_interfaces_states():
    network_interfaces_states=psutil.net_if_stats()
    NIC_stats_data = []
    for interface, stats in network_interfaces_states.items():
        NIC_stats_data.append([
            interface,
            "Up" if stats.isup else "Down", 
            "Full Duplex" if stats.duplex == psutil.NIC_DUPLEX_FULL else
            "Half Duplex" if stats.duplex == psutil.NIC_DUPLEX_HALF else
            "Unknown",
            f"{stats.speed} Mbps" if stats.speed > 0 else "Unknown", 
            stats.mtu,  
            stats.flags  
        ])
    
    headers = ["Interface", "isup", "duplex", "speed", "mtu", "flags"]  
    print("\n")  
    print("network interfaces stats:")
    print(tabulate(NIC_stats_data, headers=headers, tablefmt="grid"))
    print("\n")


def format_uptime(create_time):
    """Convert process creation time to uptime in HH:MM:SS format."""
    elapsed_time = datetime.now() - datetime.fromtimestamp(create_time)
    hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def display_process_table():
    """Display the processes in a sorted table."""
    table = PrettyTable()
    table.field_names = ["PID", "PPID", "Name", "CPU %", "Memory %", "Uptime (HH:MM:SS)"]

    processes = []
    for proc in psutil.process_iter(['pid', 'ppid', 'name', 'cpu_percent', 'memory_percent', 'create_time']):
        try:
            pid = proc.info['pid']
            ppid = proc.info['ppid']
            name = proc.info['name']
            cpu_percent = proc.info['cpu_percent'] if proc.info['cpu_percent'] is not None else 0.00
            memory_percent = proc.info['memory_percent'] if proc.info['memory_percent'] is not None else 0.00
            uptime = format_uptime(proc.info['create_time'])
            
            processes.append((pid, ppid, name, cpu_percent, memory_percent, uptime))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processes.sort(key=lambda x: (x[3], x[4]), reverse=True)

    for proc in processes:
        table.add_row([proc[0], proc[1], proc[2], f"{proc[3]:.2f}%", f"{proc[4]:.2f}%", proc[5]])

    print(table)


def get_system_info():
    # Create table for system info
    sys_info = PrettyTable()
    sys_info.field_names = ["System Info", "Details"]
    sys_info.add_row(["System", f"{platform.system()} {platform.release()} ({platform.machine()})"])
    sys_info.add_row(["Processor", platform.processor()])
    sys_info.add_row(["CPU Cores", f"{psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical"])
    sys_info.add_row(["Memory", f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB"])
    sys_info.add_row(["Disk", f"{psutil.disk_usage('/').total / (1024 ** 3):.2f} GB"])

    print("System Information:")
    print(sys_info)

    # Battery Info (if available)
    print("\nBattery Info (if available):")
    battery = psutil.sensors_battery()
    if battery:
        print(f"Battery: {battery.percent}% remaining")
        print(f"Charging: {battery.power_plugged}")
    else:
        print("No battery info available.")

    # Temperature Info (if available)
    print("\nTemperature (if available):")
    try:
        temperatures = psutil.sensors_temperatures()
        for name, entries in temperatures.items():
            temp_table = PrettyTable()
            temp_table.field_names = ["Sensor", "Temperature (°C)"]
            for entry in entries:
                temp_table.add_row([entry.label or 'N/A', f"{entry.current}°C"])
            print(f"{name} Sensors:")
            print(temp_table)
    except AttributeError:
        print("No temperature sensor data available.")


def user_start():
    print("\n--------------------------------------------WELCOME TO RESOURCE MONITOR----------------------------------------------")
    
    while True:
        print("Please enter the number corresponding to the resource you wish to see and hit ENTER: ")
        print("[1] CPU                  [2] MEMORY              [3] DISK\n[4] NETWORK              [5] SENSORS             [6] PROCESSES\n[X] EXIT\n")
        option = input("Enter option: ")
        print("\033c", end="")
        if option == '1':
            while True:
                print("\033c", end="")
                get_cpu_times()
                current_cpu_util_percent()
                cpu_freq()
                cpu_cores()
                
                exit_option = input("[X]: EXIT      [R]: REFRESH       [T]: RETURN\nInput: ")
                if exit_option == "X" or exit_option == "x":
                    exit()
                elif exit_option == "T" or exit_option== "t":
                    print("\033c", end="")
                    break
                elif exit_option == "R" or exit_option == "r":
                    continue

        elif option == '2':
            while True:
                print("\033c", end="")
                get_memory()

                exit_option = input("[X]: EXIT      [R]: REFRESH       [T]: RETURN\nInput: ")
                if exit_option == "X" or exit_option == "x":
                    exit()
                elif exit_option == "T" or exit_option== "t":
                    print("\033c", end="")
                    break
                elif exit_option == "R" or exit_option == "r":
                    continue

        elif option == '3':
            while True:
                print("\033c", end="")
                disk_partiitions_and_use()
                disk_IO()

                exit_option = input("[X]: EXIT      [R]: REFRESH       [T]: RETURN\nInput: ")
                if exit_option == "X" or exit_option == "x":
                    exit()
                elif exit_option == "T" or exit_option== "t":
                    print("\033c", end="")
                    break
                elif exit_option == "R" or exit_option == "r":
                    continue      

        elif option == '4':
            while True:
                print("\033c", end="")
                get_counter_info()
                get_connection_info()
                get_network_interfaces_address()
                get_network_interfaces_states()

                exit_option = input("[X]: EXIT      [R]: REFRESH       [T]: RETURN\nInput: ")
                if exit_option == "X" or exit_option == "x":
                    exit()
                elif exit_option == "T" or exit_option== "t":
                    print("\033c", end="")
                    break
                elif exit_option == "R" or exit_option == "r":
                    continue

        elif option == '5':
            while True:
                print("\033c", end="")
                get_system_info()

                exit_option = input("[X]: EXIT      [R]: REFRESH       [T]: RETURN\nInput: ")
                if exit_option == "X" or exit_option == "x":
                    exit()
                elif exit_option == "T" or exit_option== "t":
                    print("\033c", end="")
                    break
                elif exit_option == "R" or exit_option == "r":
                    continue

        elif option == '6':
            while True:
                print("\033c", end="")
                display_process_table()

                exit_option = input("[X]: EXIT      [R]: REFRESH       [T]: RETURN\nInput: ")
                if exit_option == "X" or exit_option == "x":
                    exit()
                elif exit_option == "T" or exit_option== "t":
                    print("\033c", end="")
                    break
                elif exit_option == "R" or exit_option == "r":
                    continue
        
        elif option == 'X' or option =='x':
            exit()
        
        else:
            print("Incorrect input\n")


if __name__=="__main__":

    print("\033c", end="")
    user_start()
    
