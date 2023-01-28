import ipaddress
from netmiko import ConnectHandler

#Welcome user and gather input information 
print("Welcome to the routingloop.net static route generator for Cisco ios. The script is used to inject static routes for redistribution into other protocols. All static routes will be /32 length")
print(" ")
print("CAUTION: The next hop of all configured routes will be Null0. Be sure to enter an unused prefix to avoid traffic disruption")
print(" ")
deviceName = input("What device would you like to configure? ")
print(" ")
inputPrefix = input("Please enter an IPv4 prefix using CIDR notation. Host routes within the specified prefix will be configured: ")
print(" ")

#Determine /32s within supplied prefix 
ip_list = [str(ip) for ip in ipaddress.IPv4Network(inputPrefix)]

#Count number of entries in ip_list
ipListLen = len(ip_list)
ipListLen = ipListLen - 2
ipListLen = str(ipListLen)
print("This tool will configure " + ipListLen + " /32 routes.")
ipListLen = int(ipListLen) 
ipListLen = ipListLen + 1

continueVar = input("Would you like to continue? (Y/N) ")

#Define Device Vars
net_connect = ConnectHandler(device_type='cisco_ios', host=deviceName, username='username', password='password', secret='password') 
net_connect.enable()

if continueVar == "y" or continueVar == "Y" or continueVar == "yes" or continueVar == "Yes" or continueVar == "YES":

    while ipListLen > 1:
        # Looping logic to iterate through routes
        ipListLen = ipListLen - 1
        routeIn = ip_list[0]
        ip_list.pop(0)
        routeDest = ip_list[0]

        print(ipListLen)

        configureRoutes = ["ip route " + routeDest + " 255.255.255.255 " + "null0"]
        configureRoutesSend= net_connect.send_config_set(configureRoutes)

else:
   print("Abandoning job")   
