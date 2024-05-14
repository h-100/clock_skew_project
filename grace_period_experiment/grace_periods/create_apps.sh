#!/bin/bash

#TODO: check for port already in use

num_apps=$1
desktop=$2


path_var='/home/hira/research/clock_skew_scripts/grace_period_experiment/grace_periods/apps'

password="gandalf287"


##delete all previous crt's and keys
##TODO: create separate folders for not before and not after
rm -rf "$path_var/time*"
rm -rf "/home/hira/research/clock_skew_scripts/grace_period_experiment/grace_periods/time*"

##remove any previous running apps
#echo $password | sudo killall python3


##remove previous entries of time-pecific domains from /etc/hosts file
echo $password | sed -i '/time/d' /etc/hosts

if (( $desktop == 1 ))
then

    ##add the Test Domain to the /etc/ file
    echo $password | sudo echo "127.0.0.1   time.securepki.org" >> /etc/hosts

    for((i=0;i<num_apps;i++))
    do
        j=$((i+2))
        domain_name_dir="time"$i"_securepki_org"
        domain_name="time"$i".securepki.org"
        path_to_dir="$path_var/$domain_name_dir/"
        cp -a "$path_var/subdomain1" "$path_var/$domain_name_dir"
        sed -i -e "s/time.securepki.org/time$i.securepki.org/g" "$path_var/$domain_name_dir/app.py"
        sed -i -e "s/127.0.0.1/127.0.0.$j/g" "$path_var/$domain_name_dir/app.py"
        cp -rfa "/home/hira/research/clock_skew_scripts/grace_period_experiment/grace_periods/$domain_name.key" $path_to_dir
        cp -rfa "/home/hira/research/clock_skew_scripts/grace_period_experiment/grace_periods/$domain_name.crt" $path_to_dir
        echo $password | sudo echo "127.0.0.$j   $domain_name" >> /etc/hosts
        echo $password | sudo echo "127.0.0.$j   www.$domain_name" >> /etc/hosts
        echo $password | sudo python3 "$path_var/$domain_name_dir/app.py" &
    done
else

    ##add an IP interface for the main domain and create an /etc/hosts file
    echo $password | sudo echo "10.42.1.1   time.securepki.org" >> /etc/hosts
    echo $password | sudo ip addr add 10.42.1.1/24 dev wlp3s0

    for((i=0;i<num_apps;i++))
    do
        domain_name_dir="time"$i"_securepki_org"
        domain_name="time"$i".securepki.org"
        path_to_dir="$path_var/$domain_name_dir/"
        cp -a "$path_var/subdomain1" "$path_var/$domain_name_dir"
        cp -rfa "/home/hira/research/clock_skew_scripts/grace_period_experiment/grace_periods/$domain_name.key" $path_to_dir
        cp -rfa "/home/hira/research/clock_skew_scripts/grace_period_experiment/grace_periods/$domain_name.crt" $path_to_dir
        num_addr=$((i+2))
        addr="10.42.$num_addr.1/24"
        sudo ip addr add $addr dev wlp3s0
        sed -i -e "s/time.securepki.org/time$i.securepki.org/g" "$path_var/$domain_name_dir/app.py"
        sed -i -e "s/127.0.0.1/10.42.$num_addr.1/g" "$path_var/$domain_name_dir/app.py"

        echo $password | sudo echo "10.42.$num_addr.1   $domain_name" >> /etc/hosts
        echo $password | sudo echo "10.42.$num_addr.1   www.$domain_name" >> /etc/hosts
        echo $password | sudo python3 "$path_var/$domain_name_dir/app.py" &
    done
fi



