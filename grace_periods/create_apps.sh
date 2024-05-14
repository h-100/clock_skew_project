#!/bin/bash

#TODO: check for port already in use

num_apps=$1
path_var='/home/hira/research/clock_skew_scripts/grace_periods/apps'

password="gandalf287"


##delete all previous crt's and keys
##TODO: create separate folders for not before and not after
rm -rf "$path_var/time*"
rm -rf "/home/hira/research/clock_skew_scripts/grace_periods/time*"

##remove any previous running apps
#echo $password | sudo killall python3


##remove previous entries of time
echo $password | sed -i '/time/d' /etc/hosts

#add entry for main page and deploy it
echo $password | sudo echo "127.0.0.1   time.securepki.org" >> /etc/hosts
#echo $password | sudo python3 /home/hira/research/flask_app/main_page/main_page.py &

for((i=0;i<num_apps;i++))
do
    j=$((i+2))
    domain_name_dir="time"$i"_securepki_org"
    domain_name="time"$i".securepki.org"
    path_to_dir="$path_var/$domain_name_dir/"
    cp -a "$path_var/subdomain1" "$path_var/$domain_name_dir"
    sed -i -e "s/time.securepki.org/time$i.securepki.org/g" "$path_var/$domain_name_dir/app.py"
    sed -i -e "s/127.0.0.1/127.0.0.$j/g" "$path_var/$domain_name_dir/app.py"
    cp -rfa "/home/hira/research/clock_skew_scripts/grace_periods/$domain_name.key" $path_to_dir
    cp -rfa "/home/hira/research/clock_skew_scripts/grace_periods/$domain_name.crt" $path_to_dir
    echo $password | sudo echo "127.0.0.$j   $domain_name" >> /etc/hosts 
    echo $password | sudo echo "127.0.0.$j   www.$domain_name" >> /etc/hosts   
    echo $password | sudo python3 "$path_var/$domain_name_dir/app.py" &
done
##deploy apps
