import itertools, os
from tkinter import *
from tkinter import ttk
import threading, re

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")
style.use("dark_background")


#  CPU graph---------------
x_vals_cpu_util = []
y_vals_cpu_util = []
index_cpu_util = itertools.count()
f_cpu_util = Figure(figsize=(5,2))
a_cpu_util = f_cpu_util.add_subplot(111)
cpu_utilization_percent = 0

def animate_cpu(i):
    x_vals_cpu_util.append(next(index_cpu_util))
    y_vals_cpu_util.append(cpu_utilization_percent)

    a_cpu_util.cla()
    a_cpu_util.set_title("CPU Utilization in %")
    a_cpu_util.set_ylim(0, 100)
    a_cpu_util.set_xlim(left=i-50, right=i+50)
    # a_cpu_util.set_ylabel("Percentage")
    # a_cpu_util.set_xlabel("Time")
    a_cpu_util.set_xticklabels([])
    a_cpu_util.plot(x_vals_cpu_util, y_vals_cpu_util)

#  CPU graph end---------------


#  Mem graph---------------
x_vals_mem = []
y_vals_mem = []
index_mem = itertools.count()
f_mem = Figure(figsize=(2.95, 2))
a_mem = f_mem.add_subplot(111)
mem_utilization_percent = 0

def animate_mem(i):
    x_vals_mem.append(next(index_mem))
    y_vals_mem.append(mem_utilization_percent)

    a_mem.cla()
    a_mem.set_title("Memory Utilization in %")
    a_mem.set_ylim(0, 100)
    a_mem.set_xlim(left=i-50, right=i+50)
    # a_mem.set_ylabel("Percentage")
    # a_mem.set_xlabel("Time")
    a_mem.set_xticklabels([])
    a_mem.plot(x_vals_mem, y_vals_mem, color='purple')

#  Mem graph end---------------


#  Swap Mem graph---------------
x_vals_mem_swap = []
y_vals_mem_swap = []
index_mem_swap = itertools.count()
f_mem_swap = Figure(figsize=(2.95, 2))
a_mem_swap = f_mem_swap.add_subplot(111)
swap_mem_utilization_percent = 0

def animate_mem_swap(i):
    x_vals_mem_swap.append(next(index_mem_swap))
    y_vals_mem_swap.append(swap_mem_utilization_percent)

    a_mem_swap.cla()
    a_mem_swap.set_title("Swap Memory Utilization in %")
    a_mem_swap.set_ylim(0, 100)
    a_mem_swap.set_xlim(left=i-50, right=i+50)
    # a_mem_swap.set_ylabel("Percentage")
    # a_mem_swap.set_xlabel("Time")
    a_mem_swap.set_xticklabels([])
    a_mem_swap.plot(x_vals_mem_swap, y_vals_mem_swap, color='green')

#  Swap Mem graph end---------------


# utility
def get_cpu_list():

    cpu_list = []

    with open('/proc/stat', 'r') as f:
        data = f.readlines()

        for i in data:
            if not i.find('cpu'):
                cpu_list.append(i.strip())

    total_cpu_list = cpu_list.pop(0)
    total_cpu_list = total_cpu_list.split(" ")
    total_cpu_list[0] = "Total"
    total_cpu_list.pop(1)
    total_cpu_list = ' '.join(total_cpu_list)
    cpu_list.append(total_cpu_list)

    return cpu_list

def get_network_data():
    net_data = []
    with open("/proc/net/dev" , 'r') as f:
        data = f.readlines()
        # print(data)
        for i in data:
            net_data.append(i.strip())
        return net_data

def get_tcp_data():
    tcp = []
    with open('/proc/net/tcp', 'r')as f:
        data = f.readlines()
        for i in data:
            tcp.append(i.strip())
        return tcp

def get_udp_data():
    udp = []
    with open('/proc/net/udp', 'r')as f:
        data = f.readlines()
        for i in data:
            udp.append(i.strip())
        return udp

def remove_blank(val):
    if val != '':
        return val
    else:
        return 0


class GUI(Tk):
    
    # Initialize the gui
    def __init__(self):
        super().__init__()
        self.title("Task Manager")
        self.geometry("582x655")
        
        notebook = ttk.Notebook(self)
        notebook.grid(row=0, column=0)

        self.cpu = Frame(notebook)
        self.cpu.grid(row=0, column=0)

        self.cpu_tab = Frame(self.cpu, borderwidth=1, relief=SOLID)
        self.cpu_tab.grid(row=0, column=0, ipadx=5, padx=10, pady=10)

        self.memory = Frame(notebook)
        self.memory.grid(row=0, column=0)
        
        self.memory_tab = Frame(self.memory, borderwidth=1, relief=SOLID)
        self.memory_tab.grid(row=0, column=0, ipadx=5, padx=10, pady=10, sticky='nw')

        self.io = Frame(notebook)
        self.io.grid(row=0, column=0)

        self.io_tab = Frame(self.io, borderwidth=1, relief=SOLID)
        self.io_tab.grid(row=0, column=0, ipadx=5, padx=10, pady=10, sticky='nw')

        self.net = Frame(notebook)
        self.net.grid(row=0, column=0)

        self.net_tab = Frame(self.net, borderwidth=1, relief=SOLID)
        self.net_tab.grid(row=0, column=0, ipadx=5, padx=10, pady=10, sticky='nw')

        notebook.add(self.cpu, text="CPU")
        notebook.add(self.memory, text="Memory")
        notebook.add(self.io, text="I/O")
        notebook.add(self.net, text="Network")

        self.last_idle_time = self.last_total_time = 0


        # ----- CPU layout-------
        c1= Label(self.cpu_tab, text='CPU')
        c1.grid(row=0, column=0, padx=20, pady=5)
        c2= Label(self.cpu_tab, text='User_time')
        c2.grid(row=0, column=1, padx=20, pady=5)
        c3= Label(self.cpu_tab, text='System_time')
        c3.grid(row=0, column=2, padx=20, pady=5)
        c4= Label(self.cpu_tab, text='Idle_time')
        c4.grid(row=0, column=3, padx=20, pady=5)
        c5= Label(self.cpu_tab, text='Total')
        c5.grid(row=0, column=4, padx=20, pady=5)

        self.cpu_util_frame_1 = Frame(self.cpu, relief=SOLID, borderwidth=1)
        self.cpu_util_frame_1.grid(row=2, column=0, padx=10, pady=10, ipadx=5, sticky='w')

        self.cpu_util_frame_2 = Frame(self.cpu, relief=SOLID, borderwidth=1)
        self.cpu_util_frame_2.grid(row=3, column=0, padx=10, pady=10, ipadx=5, sticky='w')

        #  cpu utilization layout
        utilization_label = Label(self.cpu_util_frame_1, text= "Utilization")
        utilization_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.utilization_val = Label(self.cpu_util_frame_1, text="")
        self.utilization_val.grid(row=0, column=1)

        # context and interrupt layout
        cpu_tab_2 = Frame(self.cpu, relief=SOLID, borderwidth=1)
        cpu_tab_2.grid(row=1, column=0, padx=10, pady=10, ipadx=5, sticky='w')
        
        context_sw = Label(cpu_tab_2, text="Context Switches")
        context_sw.grid(row=0, column=0, pady=5, padx=5, sticky='w')
        self.con_sw_val = Label(cpu_tab_2, text="")
        self.con_sw_val.grid(row=0, column=1)
        
        interrupt_sw = Label(cpu_tab_2, text="Interrupts")
        interrupt_sw.grid(row=1, column=0, pady=5, padx=5, sticky='w')
        self.intr_val = Label(cpu_tab_2, text="")
        self.intr_val.grid(row=1, column=1)


        cpu_list = get_cpu_list()
        self.c0_list = []
        self.c1_list = []
        self.c2_list = []
        self.c3_list = []
        self.c4_list = []

        for i in range(len(cpu_list)):
            c0 = Label(self.cpu_tab, text="")
            c0.grid(row=i, column=0, padx=20, pady=10)
            self.c0_list.append(c0)
        
            c1 = Label(self.cpu_tab, text="")
            c1.grid(row=i, column=1, padx=20, pady=10)
            self.c1_list.append(c1)

            c2 = Label(self.cpu_tab, text="")
            c2.grid(row=i, column=2, padx=20, pady=10)
            self.c2_list.append(c2)

            c3 = Label(self.cpu_tab, text="")
            c3.grid(row=i, column=3, padx=20, pady=10)
            self.c3_list.append(c3)

            c4 = Label(self.cpu_tab, text="")
            c4.grid(row=i, column=4, padx=20, pady=10)
            self.c4_list.append(c4)

        # self.update_cpu()
        self.thread_cpu()


        # # add figure canvas here
        canvas_cpu_util = FigureCanvasTkAgg(f_cpu_util,  self.cpu_util_frame_2)
        canvas_cpu_util.draw()
        canvas_cpu_util.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        # #  ----- Memory Layout----- 
        self.memory_tab_2 = Frame(self.memory, borderwidth=1, relief=SOLID)
        self.memory_tab_2.grid(row=1, column=0, ipadx=5, padx=10, pady=10, sticky="nw")

        self.mem_frame_1 = Frame(self.memory, relief=SOLID, borderwidth=1)
        self.mem_frame_1.grid(row=0, column=1, padx=5, pady=5, sticky='nw')

        self.mem_frame_2 = Frame(self.memory, relief=SOLID, borderwidth=1)
        self.mem_frame_2.grid(row=1, column=1, padx=5, pady=5, sticky='nw')
        
        # self.update_mem()
        self.thread_mem()

        # # add figure canvas here 
        canvas_mem_util = FigureCanvasTkAgg(f_mem,  self.mem_frame_1)
        canvas_mem_util.draw()
        canvas_mem_util.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        # add figure canvas here 
        canvas_mem_swap_util = FigureCanvasTkAgg(f_mem_swap,  self.mem_frame_2)
        canvas_mem_swap_util.draw()
        canvas_mem_swap_util.get_tk_widget().grid(row=1, column=0, padx=5, pady=10, sticky='nsew')


        # #  --------- Network layout ---------------
        net_data = get_network_data()

        # received
        interface_net = Label(self.net_tab, text="Interfaces")
        interface_net.grid(row=0, column=0)

        r_label = Label(self.net_tab, text="Received")
        r_label.grid(row=0, column=1)

        for counter,n in enumerate(net_data[2:]):
            counter += 1
            intf_name = n.split(":")[0]
            Label(self.net_tab, text=intf_name).grid(row=counter+1, column=0, sticky='w')

        received_heading = []
        transmit_heading = []

        for i in net_data[1].split("|")[1].split(" ") :
            if i != '':
                received_heading.append(i)
        
        for i in net_data[1].split("|")[2].split(" ") :
            if i != '':
                transmit_heading.append(i)


        for counter,i in enumerate(received_heading):
            Label(self.net_tab, text=i).grid(row=1, column=counter+1, sticky='w', padx=5, pady=5)
        
        
        # # transmit
        self.net_tab_2 = Frame(self.net, borderwidth=1, relief=SOLID)
        self.net_tab_2.grid(row=1, column=0, ipadx=5, padx=10, pady=10, sticky='nw')

        interface_net = Label(self.net_tab_2, text="Interfaces")
        interface_net.grid(row=0, column=0)

        t_label = Label(self.net_tab_2, text="Transmit")
        t_label.grid(row=0, column=1)


        # # print(":Transmit heading = ", transmit_heading)

        for counter,n in enumerate(net_data[2:]):
            counter += 1
            intf_name = n.split(":")[0]
            # print(intf_name)
            Label(self.net_tab_2, text=intf_name).grid(row=counter+1, column=0, sticky='w')
    
        for counter,i in enumerate(transmit_heading):
            Label(self.net_tab_2, text=i).grid(row=1, column=counter+1, sticky='w', padx=5, pady=5)

        # # ------ network received and transmit data input ----------

        r_data = []
        self.r_data_widgets = []

        t_data = []
        self.t_data_widgets = []

        for counter,n in enumerate(net_data[2:]):
            counter += 1
            data = n.split(":")[1].split(" ")
            removed_blanks = list(filter(remove_blank, data))
            r_data = removed_blanks[:8]
            t_data = removed_blanks[8:]
            
            for inner_counter, i in enumerate(r_data):
                rd = Label(self.net_tab, text=i)
                rd.grid(row=counter+1, column=inner_counter+1, sticky='n')
                self.r_data_widgets.append(rd)

            for inner_counter, i in enumerate(t_data):
                td = Label(self.net_tab_2, text=i)
                td.grid(row=counter+1, column=inner_counter+1, sticky='n')
                self.t_data_widgets.append(td)


        # TCP and UDP connections----------------------------
        # TCP 
        self.tcp_frame = Frame(self.net, borderwidth=1, relief=SOLID)
        self.tcp_frame.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        l_tcp = Label(self.tcp_frame, text='TCP')
        l_tcp.grid(row=0, column=0)

        tcp_data = get_tcp_data()
        tcp_labels = tcp_data[0]

        removed_blanks = list(filter(remove_blank, tcp_labels.split(" ")))
        # print(removed_blanks)

        for counter,i in enumerate(removed_blanks):
            l = Label(self.tcp_frame, text = i)
            l.grid(row=1, column=counter, padx=5, pady=5)
        
        # UDP
        self.udp_frame = Frame(self.net, borderwidth=1, relief=SOLID)
        self.udp_frame.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        l_udp = Label(self.udp_frame, text='UDP')
        l_udp.grid(row=0, column=0)

        udp_data = get_udp_data()
        udp_labels = udp_data[0]

        removed_blanks = list(filter(remove_blank, udp_labels.split(" ")))
        # print(removed_blanks)

        for counter,i in enumerate(removed_blanks):
            l = Label(self.udp_frame, text = i)
            l.grid(row=1, column=counter, padx=5, pady=5)


        # self.update_net()
        self.thread_net()

        # # ----------- IO layout-----------------
        
        io_labels = ["1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "10",
                    "11",
                    "12"]

        for counter,i in enumerate(io_labels):
            io_lab = Label(self.io_tab, text=i)
            io_lab.grid(row=counter, column=0, sticky='nw', padx=5, pady=5)

        self.io_vars = []

        with open("/proc/diskstats", 'r')as f:
            data = f.readlines()

            loop_count = 0

            for i in data:
                if "sda" in i:
                    loop_count += 1
                    line = i.strip().split(" ")
                    filtered = list(filter(remove_blank, line))

                    for inner_counter, each_i in enumerate(filtered[2:14]):
                        io_lab = Label(self.io_tab, text=each_i)
                        io_lab.grid(row=inner_counter, column=loop_count)
                        self.io_vars.append(io_lab)

                elif "nvme0n" in i:
                    print(i)
                    loop_count += 1
                    line = i.strip().split(" ")
                    filtered = list(filter(remove_blank, line))

                    for inner_counter, each_i in enumerate(filtered[2:14]):
                        io_lab = Label(self.io_tab, text=each_i)
                        io_lab.grid(row=inner_counter, column=loop_count)
                        self.io_vars.append(io_lab)

        self.update_io_disk()
            

    # ---------------------- CPU -------------------
    def update_cpu(self):
        global cpu_utilization_percent
        
        cpu_list = []
        context_switch = None
        interrupt_val = None

        user_time = system_time = idle_time = total_time = 0

        with open('/proc/stat', 'r') as f:
            data = f.readlines()

            for i in data:
                if not i.find('cpu'):
                    cpu_list.append(i.strip())
                elif not i.find("ctxt"):
                    context_switch = i.strip()
                elif not i.find("intr"):
                    interrupt_val = i.strip()

        total_cpu_list = cpu_list.pop(0)
        total_cpu_list = total_cpu_list.split(" ")
        total_cpu_list[0] = "Total"
        total_cpu_list.pop(1)
        total_cpu_list = ' '.join(total_cpu_list)
        cpu_list.append(total_cpu_list)

        context_switch = context_switch.split(" ")[1]
        interrupt_val = interrupt_val.split(" ")[1]

        # ------ update cpu values------ 

        for counter, i in enumerate(self.c0_list):
            for counter_inner, j in enumerate(cpu_list):
                if counter == counter_inner:
                    data = j.split(' ')
                    i.config(text=data[0])
                    # i.config(text="SAUNVID")
                    i.grid(row=counter+1)
        
        for counter, i in enumerate(self.c1_list):
            for counter_inner, j in enumerate(cpu_list):
                if counter == counter_inner:
                    data = j.split(' ')
                    user_time = round(int(data[1])/100, 2)
                    user= f"{user_time} s"
                    i.config(text=user)
                    i.grid(row=counter+1)
        
        for counter, i in enumerate(self.c2_list):
            for counter_inner, j in enumerate(cpu_list):
                if counter == counter_inner:
                    data = j.split(' ')
                    system_time = round(int(data[3])/100, 2)
                    system = f"{system_time} s"
                    i.config(text=system)
                    i.grid(row=counter+1)
        
        for counter, i in enumerate(self.c3_list):
            for counter_inner, j in enumerate(cpu_list):
                if counter == counter_inner:
                    data = j.split(' ')
                    idle_time = round(int(data[4])/100, 2)
                    idle = f"{idle_time} s"
                    i.config(text=idle)
                    i.grid(row=counter+1)

        for counter, i in enumerate(self.c4_list):
            for counter_inner, j in enumerate(cpu_list):
                if counter == counter_inner:
                    data = j.split(' ')
                    total_time = round(user_time + system_time + idle_time, 2)
                    total_cpu = f"{total_time} s"
                    i.config(text=total_cpu)
                    i.grid(row=counter+1)
        
        # ------- update  cpu utilization ------
        for counter, i in enumerate(cpu_list):
            if counter == (len(cpu_list) - 1):
                idle_delta = idle_time - self.last_idle_time

                total_delta =total_time - self.last_total_time

                self.last_idle_time, self.last_total_time = idle_time, total_time

                utilisation = 100.0 * (1.0 - idle_delta / total_delta)

                cpu_utilization_percent = utilisation
                self.utilization_val.config(text=f"{round(utilisation,2)} %")

        # ------- udpate context and interrupts -----
        self.con_sw_val.config(text=context_switch)
        self.intr_val.config(text=interrupt_val)

        self.after(1200, self.update_cpu)
        
    # --------------------- Memory -----------------
    def update_mem(self):
        global mem_utilization_percent, swap_mem_utilization_percent

        mem_list = []

        total_mem = free_mem = available_mem = buffer_mem = cached_mem = swap_mem_cache = swap_mem_total = swap_mem_free = 0

        with open('/proc/meminfo', 'r') as f:
            data = f.readlines()
            for i in data:
                if not i.find("Mem"):
                    mem_list.append(i.strip())
                elif not i.find("Swap"):
                    mem_list.append(i.strip())
                elif not i.find("Buffer"):
                    mem_list.append(i.strip())
                elif not i.find("Cache"):
                    mem_list.append(i.strip())

        for counter,i in enumerate(mem_list):
            data = i.split(":")
            if "mem" in data[0].lower() or "buffer" in data[0].lower() or ("cached" in data[0].lower() and not "swap" in data[0].lower()):
                m = Label(self.memory_tab, text=data[0].strip())
                m.grid(row=counter, column=0, sticky='w', padx=5, pady=5)

                data_in_kb = int(data[1].strip().split(" ")[0])
                converted_to_gb = round(data_in_kb/1000000, 3)
                converted_to_gb = f"{converted_to_gb} Gb"

                m = Label(self.memory_tab, text=converted_to_gb)
                m.grid(row=counter, column=1, sticky='w', padx=5, pady=5)

                # calculate utilization of Memory
                if counter == 0:
                    total_mem = int(data[1].strip().split(" ")[0])
                    total_mem = round(total_mem/1000000, 3)
                elif counter == 1:
                    free_mem = int(data[1].strip().split(" ")[0])
                    free_mem = round(free_mem/1000000, 3)
                elif counter == 2:
                    available_mem = int(data[1].strip().split(" ")[0])
                    available_mem = round(available_mem/1000000, 3)
                elif counter == 3:
                    buffer_mem = int(data[1].strip().split(" ")[0])
                    buffer_mem = round(buffer_mem/1000000, 3)
                elif counter == 4:
                    cached_mem = int(data[1].strip().split(" ")[0])
                    cached_mem = round(cached_mem/1000000, 3)


            else:
                m = Label(self.memory_tab_2, text=data[0].strip())
                m.grid(row=counter, column=0, sticky='w', padx=5, pady=5)

                data_in_kb = int(data[1].strip().split(" ")[0])
                converted_to_gb = round(data_in_kb/1000000, 3)
                converted_to_gb = f"{converted_to_gb} Gb"

                m = Label(self.memory_tab_2, text=converted_to_gb)
                m.grid(row=counter, column=1, sticky='w', padx=5, pady=5)

                if counter == 5:
                    swap_mem_cache = int(data[1].strip().split(" ")[0])
                    swap_mem_cache = round(swap_mem_cache/1000000, 3)

                elif counter == 6:
                    swap_mem_total = int(data[1].strip().split(" ")[0])
                    swap_mem_total = round(swap_mem_total/1000000, 3)

                elif counter == 7:
                    swap_mem_free = int(data[1].strip().split(" ")[0])
                    swap_mem_free = round(swap_mem_free/1000000, 3)

        # Memory utilization 
        used_mem = total_mem - free_mem - available_mem
        percent_mem_util = round((used_mem/total_mem) * 100.0, 2)
        mem_utilization_percent = percent_mem_util

        # swap memory utilization
        used_swap_mem = swap_mem_total - swap_mem_free - swap_mem_cache
        percent_swap_mem_util = round((used_swap_mem/swap_mem_total) * 100.0, 2)
        swap_mem_utilization_percent = percent_swap_mem_util

        self.after(1200, self.update_mem)

    # --------------------- Network ----------------
    def update_net(self):
        # print(self.r_data_widgets, self.t_data_widgets)

        with open('/proc/net/dev', 'r') as f :
            data = f.readlines()

            # received-------------
            total_r_vals = []

            for i in data[2:]:
                byte_data = i.strip().split(":")[1].split(" ")
                removed_blanks = list(filter(remove_blank, byte_data))
                for i in removed_blanks[:8]:
                    total_r_vals.append(i)

            for counter, i in enumerate(zip(self.r_data_widgets, total_r_vals)):

                if counter%8 == 0:
                    byte_converted = f"{round(int(i[1])/1000000, 2)} Mb/s"
                    i[0].config(text=byte_converted)
                else:
                    i[0].config(text=i[1])
            
            # transmit---------------
            total_t_vals = []
            for i in data[2:]:
                byte_data = i.strip().split(":")[1].split(" ")
                removed_blanks = list(filter(remove_blank, byte_data))
                for i in removed_blanks[8:]:
                    total_t_vals.append(i)
            
            for counter, i in enumerate(zip(self.t_data_widgets, total_t_vals)):
                if counter%8 == 0:
                    byte_converted = f"{round(int(i[1])/1000000, 2)} Mb/s"
                    i[0].config(text=byte_converted)
                else:
                    i[0].config(text=i[1])


        # tcp --------
        tcp_data = get_tcp_data()
        tcp_data = tcp_data[1:]
        replaced_tcp = []

        for i in tcp_data:
            # print(counter, i)
            ind = i.find(":")
            sl_val = i[:ind]
            other_data = i[ind+1:]
            other_data = sl_val + other_data

            pos_of_char = [m.start() for m in re.finditer(r":",other_data)][2:]

            beginning = other_data[:pos_of_char[0]]
            middle = other_data[pos_of_char[0]+1 : pos_of_char[1]]
            ending = other_data[pos_of_char[1]+1 :]
            other_data = beginning + " " + middle + " " + ending

            other_data = other_data.split(" ")
            removed_blank_tcp = list(filter(remove_blank, other_data))
            replaced_tcp.append(removed_blank_tcp)

        from_row = 2
        for counter, i in enumerate(replaced_tcp):
            for inner_counter, j in enumerate(i[:12]):
                l1 = Label(self.tcp_frame, text = j)
                l1.grid(row=from_row, column=inner_counter)

            from_row += 1
            

        # udp--------------
        udp_data = get_udp_data()
        udp_data = udp_data[1:]
        replaced_udp = []
        for i in  udp_data:
            ind = i.find(":")
            sl_val = i[:ind]
            other_data = i[ind+1:]
            other_data = sl_val + other_data

            pos_of_char = [m.start() for m in re.finditer(r":",other_data)][2:]

            beginning = other_data[:pos_of_char[0]]
            middle = other_data[pos_of_char[0]+1 : pos_of_char[1]]
            ending = other_data[pos_of_char[1]+1 :]
            other_data = beginning + " " + middle + " " + ending

            other_data = other_data.split(" ")
            removed_blank_udp = list(filter(remove_blank, other_data))
            replaced_udp.append(removed_blank_udp)

        from_row = 2

        for counter, i in enumerate(replaced_udp):
            for inner_counter, j in enumerate(i[:15]):
                l1 = Label(self.udp_frame, text = j)
                l1.grid(row=from_row, column=inner_counter)

            from_row += 1

        self.after(2200, self.update_net)

    # ----------------------io stat ----------------
    def update_io_disk(self):

        current_io_vals = []

        with open("/proc/diskstats", 'r')as f:
            data = f.readlines()

            loop_count = 0
            
            for i in data:
                if "sda" in i:
                    loop_count += 1
                    line = i.strip().split(" ")
                    filtered = list(filter(remove_blank, line))

                    for inner_counter, each_i in enumerate(filtered[2:14]):
                        current_io_vals.append(each_i)
                        
                elif "nvme0n" in i:
                    loop_count += 1
                    line = i.strip().split(" ")
                    filtered = list(filter(remove_blank, line))

                    for inner_counter, each_i in enumerate(filtered[2:14]):
                        current_io_vals.append(each_i)

        for val in zip(self.io_vars, current_io_vals):
            val[0].config(text=val[1])

        self.after(1200, self.update_io_disk)


    def thread_net(self):
        t = threading.Thread(target=self.update_net)
        t.start()
    def thread_cpu(self):
        t = threading.Thread(target=self.update_cpu)
        t.start()
    def thread_mem(self):
        t = threading.Thread(target=self.update_mem)
        t.start()


if __name__ == "__main__":
    win = GUI()
    ani_cpu = animation.FuncAnimation(f_cpu_util, animate_cpu, 1000)
    ani_mem = animation.FuncAnimation(f_mem, animate_mem, 1000)
    ani_mem_swap = animation.FuncAnimation(f_mem_swap, animate_mem_swap, 1000)
    win.mainloop()



